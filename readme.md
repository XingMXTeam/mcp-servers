# MCP Servers

This repository contains MCP servers for various services.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## 小红书mcp
`fastmcp run server.py:mcp --transport sse --host 127.0.0.1 --port 9001`

```json
{
  "mcpServers": {
    "xiaohongshu": {
      "disabled": false,
      "timeout": 60,
      "url": "http://127.0.0.1:9001/sse",
      "transportType": "sse",
      "autoApprove": [
        "publish_xiaohongshu_note"
      ]
    }
  }
}
```

## compyf

```json
{
  "mcpServers": {
    "comfyui": {
      "autoApprove": [
        "generate_image_async",
        "get_image_status",
        "get_image_status_and_download_to_local"
      ],
      "disabled": false,
      "timeout": 60,
      "url": "http://127.0.0.1:9000/sse",
      "transportType": "sse"
    }
  }
}
```

## Testing

This repository includes unit tests for the modules. To run the tests:

```bash
python tests/run_tests.py
```

See the [tests/README.md](tests/README.md) file for more information about the tests.