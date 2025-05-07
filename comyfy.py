import urllib
import uuid
from typing import Dict, Any, List

import httpx
import logging
import websockets
from PIL import Image
import io
from fastmcp import FastMCP
from fastmcp.prompts import UserMessage

import json
from time import sleep


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("comfy-image-mcp-server")

COMFY_SERVER = "localhost:8000"
CLIENT_ID = str(uuid.uuid4())

# Create a basic server instance
mcp = FastMCP(name="CompyImageServer")

# You can also add instructions for how to interact with the server
mcp_with_instructions = FastMCP(
    name="HelpfulAssistant",
    instructions="这个服务是用来通过comfyui生成图片的."
                 "调用generate_image_async()来异步地生成需要的图片."
)


def queue_prompt(prompt: Dict[str, Any] = None) -> Dict[str, Any]:
    url = f"http://{COMFY_SERVER}/api/prompt"
    json = {
        "prompt": prompt,
        "client_id": CLIENT_ID
    }
    try:
        response = httpx.post(url=url, json=json, verify=False, trust_env=False, timeout=60.0)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to queue prompt: {response.status_code} - {response.text}")
        return response.json()
    except httpx.RequestError as e:
        # logger.info(traceback.format_exc())
        raise RuntimeError(f"HTTP request failed: {e}")

async def download_image(prompt_id: str) -> bytes:
    uri = f"ws://{COMFY_SERVER}/ws?clientId={CLIENT_ID}"
    logger.info(f"Connecting to websocket at {uri}")
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()

                if isinstance(message, str):
                    try:
                        data = json.loads(message)
                        logger.info(f"Received text message: {data}")

                        if data.get("type") == "executing":
                            exec_data = data.get("data", {})
                            if exec_data.get("prompt_id") == prompt_id:
                                node = exec_data.get("node")
                                logger.info(f"Processing node: {node}")
                                if node is None:
                                    logger.info("Generation complete signal received")
                                    break
                    except:
                        pass
                else:
                    logger.info(f"Received binary message of length: {len(message)}")
                    if len(message) > 8:  # Check if we have actual image data
                        return message[8:]  # Remove binary header
                    else:
                        logger.warning(f"Received short binary message: {message}")

            except websockets.exceptions.ConnectionClosed as e:
                logger.error(f"WebSocket connection closed: {e}")
                break
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                continue


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(COMFY_SERVER, url_values)) as response:
        return response.read()


def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(COMFY_SERVER, prompt_id)) as response:
        return json.loads(response.read())


def get_image_and_download(prompt_id, path):
    output_images = []
    while True:
        history = get_history(prompt_id)[prompt_id]
        if history['status']['status_str'] == 'success':
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                images_output = []
                if 'images' in node_output:
                    for image in node_output['images']:
                        image_data = get_image(image['filename'], image['subfolder'], image['type'])
                        image_bytes = Image.open(io.BytesIO(image_data))
                        file_path = ""
                        if path.endswith("/"):
                            file_path = path + image['filename']
                        else:
                            file_path = path + "/" + image['filename']
                        image_bytes.save(file_path)
                        output_images.append(file_path)
                #         images_output.append(image_data)
                # output_images[node_id] = images_output
                # output_images_names[node_id] =
            return output_images
        else:
            logger.info(f"promot {prompt_id} unfinished meta: {history}")
            sleep(1)
            continue

#
# def create_simple_note():
#     title = "第四条小红书"
#     desc = "一只埃及猫"
#     images = [
#         "/Users/wangrupeng/Downloads/000000039769.jpg",
#     ]
#     note = xhs_client.create_image_note(title, desc, images, is_private=False)
#     beauty_print(note)


@mcp.prompt()
def generate_image_request(prompt: str, style: str = "动漫风格") -> UserMessage:
    """Generates a user message requesting image generation"""
    content = f"生成一个comfyui的英文prompt，要求包含下面的内容: {prompt} 并且要求生成的图片需要具有很高的质量，风格是{style}"
    return UserMessage(content=content)


@mcp.tool()
def generate_image_async(prompt: str = "a cat with yellow hat", width=512, height=512,seed=4787458) -> Dict[str, Any]:
    workflow = {
        "6": {
            "inputs": {
                "text": prompt,
                "clip": [
                    "30",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Positive Prompt)"
            }
        },
        "8": {
            "inputs": {
                "samples": [
                    "31",
                    0
                ],
                "vae": [
                    "30",
                    2
                ]
            },
            "class_type": "VAEDecode",
            "_meta": {
                "title": "VAE解码"
            }
        },
        "9": {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": [
                    "8",
                    0
                ]
            },
            "class_type": "SaveImage",
            "_meta": {
                "title": "保存图像"
            }
        },
        "27": {
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            },
            "class_type": "EmptySD3LatentImage",
            "_meta": {
                "title": "空Latent图像（SD3）"
            }
        },
        "30": {
            "inputs": {
                "ckpt_name": "flux1-dev-fp8.safetensors"
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {
                "title": "Checkpoint加载器（简易）"
            }
        },
        "31": {
            "inputs": {
                "seed": seed,
                "steps": 20,
                "cfg": 1,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1,
                "model": [
                    "30",
                    0
                ],
                "positive": [
                    "35",
                    0
                ],
                "negative": [
                    "33",
                    0
                ],
                "latent_image": [
                    "27",
                    0
                ]
            },
            "class_type": "KSampler",
            "_meta": {
                "title": "K采样器"
            }
        },
        "33": {
            "inputs": {
                "text": "",
                "clip": [
                    "30",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Negative Prompt)"
            }
        },
        "35": {
            "inputs": {
                "guidance": 3.5,
                "conditioning": [
                    "6",
                    0
                ]
            },
            "class_type": "FluxGuidance",
            "_meta": {
                "title": "Flux引导"
            }
        }
    }
    return queue_prompt(workflow)


# @mcp.tool()
# def get_image_status(prompt_id: str = "5d44dff8-8961-47a7-b26a-b51b5d801e10") -> str:
#     """get the image status"""
#     url = f"http://{COMFY_SERVER}/api/history/{prompt_id}"
#     response = httpx.get(url,verify=False, trust_env=False,timeout=60.0)
#     return str(response.json())

#
# @mcp.tool()
# def publish_xiaohongshu_note() -> str:
#     try:
#         create_simple_note()
#     except Exception as e:
#         print(e)


@mcp.tool()
def get_image_status_and_download_to_local(prompt_id:str, absolute_path: str = "/Users/wangrupeng/Documents/work/files/images") -> List[str]:
    """get image generate status and download to local when it's generating success"""
    images = get_image_and_download(prompt_id, absolute_path)
    return images


if __name__ == "__main__":
    mcp.run(transport="sse",host="127.0.0.1", port=9000)
    # create_simple_note()
    # print(generate_image_async("a cute girl with red hat standing on the green land"))
    # images = download_image_to_local("03e6da53-9779-4af8-b7a9-564f90eeea36")
    # print(images)