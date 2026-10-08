# vnexpress-mcp

MCP server lấy **tin mới nhất mục Thời sự của VnExpress** (qua RSS `https://vnexpress.net/rss/thoi-su.rss`).
Mỗi lần gọi đều tải lại trực tiếp, không cache, nên luôn có tin mới.

## Tool / Prompt

| Tên | Loại | Mô tả |
|---|---|---|
| `get_thoi_su_news(limit=5)` | tool | Tiêu đề, giờ đăng, tóm tắt, link của `limit` tin mới nhất (1–30) |
| `tin_thoi_su` | prompt | Gợi ý nhanh "liệt kê 5 tin Thời sự mới nhất" |

## Cài đặt

Cần Python ≥ 3.10. Chọn một cách:

```bash
# Cách 0: cài thẳng từ GitHub
uv tool install git+https://github.com/trantuandat2460/vnexpress-mcp
# hoặc tải file .whl ở mục Releases của repo rồi cài theo cách 1
```

```bash
# Cách 1: cài từ file wheel (mang sang máy khác)
pipx install vnexpress_mcp-0.1.0-py3-none-any.whl     # hoặc: uv tool install <file.whl>

# Cách 2: chạy thẳng không cần cài
uvx --from /đường/dẫn/vnexpress_mcp-0.1.0-py3-none-any.whl vnexpress-mcp
```

Sau khi cài, lệnh `vnexpress-mcp` khởi động server (giao tiếp stdio).

## Thêm vào các ứng dụng

**Claude Code**
```bash
claude mcp add vnexpress -s user -- vnexpress-mcp
```

**Claude Desktop** (`claude_desktop_config.json`), **Cursor** (`~/.cursor/mcp.json`),
**Windsurf**, **Cline**… đều dùng cùng dạng:
```json
{
  "mcpServers": {
    "vnexpress": { "command": "vnexpress-mcp" }
  }
}
```

**VS Code Copilot** (`.vscode/mcp.json`):
```json
{
  "servers": {
    "vnexpress": { "type": "stdio", "command": "vnexpress-mcp" }
  }
}
```

Nếu ứng dụng không tìm thấy lệnh, dùng đường dẫn đầy đủ (xem bằng `which vnexpress-mcp`,
trên Windows: `where vnexpress-mcp`).

## Build lại package

```bash
uv build        # tạo dist/*.whl và dist/*.tar.gz
```
