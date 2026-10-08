"""MCP server lấy tin mới nhất mục Thời sự của VnExpress qua RSS.

Mỗi lần tool được gọi đều tải RSS trực tiếp, không cache, nên luôn là tin mới nhất.
"""

import html
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

from mcp.server.mcpserver import MCPServer

RSS_URL = "https://vnexpress.net/rss/thoi-su.rss"
USER_AGENT = "Mozilla/5.0 (vnexpress-mcp)"
TIMEOUT = 15

mcp = MCPServer("vnexpress")


def _clean_summary(raw: str) -> str:
    # description của VnExpress là HTML: <a><img></a></br>Tóm tắt
    text = re.sub(r"<[^>]+>", " ", raw or "")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _format_time(raw: str) -> str:
    try:
        return parsedate_to_datetime(raw).strftime("%H:%M %d/%m/%Y")
    except (TypeError, ValueError):
        return raw or ""


def fetch_news(limit: int = 5) -> list[dict]:
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        root = ET.fromstring(resp.read())
    items = []
    for item in root.iterfind("./channel/item"):
        items.append({
            "title": (item.findtext("title") or "").strip(),
            "link": (item.findtext("link") or "").strip(),
            "published": _format_time(item.findtext("pubDate") or ""),
            "summary": _clean_summary(item.findtext("description") or ""),
        })
        if len(items) >= limit:
            break
    return items


@mcp.tool()
def get_thoi_su_news(limit: int = 5) -> str:
    """Lấy các tin mới nhất mục Thời sự của VnExpress (mặc định 5 tin).

    Mỗi lần gọi đều tải lại từ VnExpress nên luôn là tin mới nhất.
    Trả về tiêu đề, thời gian đăng, tóm tắt và link từng tin.
    """
    limit = max(1, min(limit, 30))
    try:
        news = fetch_news(limit)
    except Exception as e:  # lỗi mạng / RSS hỏng: báo lại cho client thay vì làm sập server
        return f"Không lấy được tin từ VnExpress: {e}"
    if not news:
        return "VnExpress không trả về tin nào."
    lines = [f"{len(news)} tin Thời sự mới nhất - VnExpress\n"]
    for i, n in enumerate(news, 1):
        lines.append(f"{i}. {n['title']}")
        lines.append(f"   🕒 {n['published']}")
        if n["summary"]:
            lines.append(f"   {n['summary']}")
        lines.append(f"   🔗 {n['link']}\n")
    return "\n".join(lines)


@mcp.prompt()
def tin_thoi_su() -> str:
    """Xem nhanh 5 tin Thời sự mới nhất."""
    return "Gọi tool get_thoi_su_news và liệt kê đề mục 5 tin Thời sự mới nhất của VnExpress."


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
