import json
import logging

import httpx
from fastmcp import FastMCP
from time import sleep

from playwright.sync_api import sync_playwright

from xhs import XhsClient

# https://reajason.github.io/xhs/basic.html
cookie = "a1=xxxx;"

XIAOHONGSHU_SERVER = "127.0.0.1:5005"

def sign(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = "/path/to/stealth.min.js"
                chromium = playwright.chromium

                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                browser = chromium.launch(headless=True)

                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                # 这个地方设置完浏览器 cookie 之后，如果这儿不 sleep 一下签名获取就失败了，如果经常失败请设置长一点试试
                sleep(1)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception as e:
            # 这儿有时会出现 window._webmsxyw is not a function 或未知跳转错误，因此加一个失败重试趴
            logger.warning(f"failed : {e}")
            pass
    raise Exception("重试了这么多次还是无法签名成功，寄寄寄")


xhs_client = XhsClient(cookie, sign=sign)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("comfy-image-mcp-server")


# Create a basic server instance
mcp = FastMCP(name="XiaoHongShuServer")

# You can also add instructions for how to interact with the server
mcp_with_instructions = FastMCP(
    name="HelpfulAssistant",
    instructions="这个服务是用来发布管理和查看小红书笔记的"
)


def create_simple_note(title: str, desc: str, images: []) -> str:
    note = xhs_client.create_image_note(title, desc, images, is_private=False)
    return json.dumps(note, ensure_ascii=False, indent=2)


@mcp.tool()
def publish_xiaohongshu_note(title: str = "第五条小红书", desc = "一只埃及猫", images: [] = [
        "/path/to/source.jpg",
    ]) -> str:
    """publish a xiaohongshu note"""
    try:
        url = f"http://{XIAOHONGSHU_SERVER}/create"
        json = {
            "title": title,
            "desc": desc,
            "images": images}
        response = httpx.post(url=url, json=json, verify=False, trust_env=False, timeout=60.0)
        return response.json()
    except Exception as e:
        return f"error {e}"


if __name__ == "__main__":
    mcp.run(transport="sse",host="127.0.0.1", port=9001)