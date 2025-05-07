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

