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