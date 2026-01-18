"""
下载模块
用于从 Jina AI 下载目标 URL 的 markdown 格式内容
"""

import requests
from typing import Optional
import typer


def download_markdown(url: str, timeout: int = 180) -> Optional[str]:
    """
    从 Jina AI 下载目标 URL 的 markdown 格式内容

    参数:
        url: 目标网页 URL
        timeout: 下载超时时间（秒），默认 180 秒（3 分钟）

    返回:
        下载的 markdown 内容，如果失败返回 None
    """
    jina_url = f"https://r.jina.ai/{url}"

    try:
        typer.echo(f"📥 正在下载: {url}")
        typer.echo(f"🔗 使用 Jina AI: {jina_url}")
        typer.echo(f"⏱️  超时设置: {timeout} 秒")

        response = requests.get(jina_url, timeout=timeout)
        response.raise_for_status()

        content = response.text

        if not content or len(content.strip()) == 0:
            typer.echo("⚠️  下载的内容为空", err=True)
            return None

        typer.echo(f"✅ 下载成功，内容长度: {len(content)} 字符")
        return content

    except requests.exceptions.Timeout:
        typer.echo("❌ 下载超时，请检查网络连接", err=True)
        return None
    except requests.exceptions.RequestException as e:
        typer.echo(f"❌ 下载失败: {e}", err=True)
        return None
    except Exception as e:
        typer.echo(f"❌ 未知错误: {e}", err=True)
        return None


def extract_title_from_markdown(content: str) -> Optional[str]:
    """
    从 markdown 内容的第一行提取标题
    Jina AI 返回的第一行格式为: Title: {文章的标题}

    参数:
        content: markdown 内容

    返回:
        提取的标题，如果提取失败返回 None
    """
    if not content:
        return None

    # 获取第一行
    first_line = content.split("\n")[0].strip()

    # 检查是否符合 "Title: {标题}" 格式
    if first_line.startswith("Title:"):
        title = first_line[6:].strip()  # 去掉 "Title:" 前缀
        if title:
            # 清理文件名中不允许的字符
            invalid_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
            for char in invalid_chars:
                title = title.replace(char, "_")
            return title

    return None


def save_markdown_to_file(content: str, filepath: str) -> bool:
    """
    将 markdown 内容保存到文件

    参数:
        content: markdown 内容
        filepath: 目标文件路径

    返回:
        True 如果保存成功，否则 False
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        typer.echo(f"💾 已保存到: {filepath}")
        return True
    except IOError as e:
        typer.echo(f"❌ 保存文件失败: {e}", err=True)
        return False
