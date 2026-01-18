"""
Markdown Downloader - 命令行程序主入口
使用 Typer 构建的 CLI 工具，用于下载网页的 Markdown 格式并可选地使用 LLM 优化
"""

import typer
from pathlib import Path
from typing import Optional

from config import save_config, load_config, validate_config, display_config
from downloader import (
    download_markdown,
    save_markdown_to_file,
    extract_title_from_markdown,
)
from optimizer import optimize_markdown_with_llm

# 创建 Typer 应用
app = typer.Typer(
    name="markdown-downloader",
    help="📥 下载网页的 Markdown 格式，并可使用 LLM 优化内容",
    add_completion=False,
)


@app.command("config")
def config_command(
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k", help="API 密钥（某些 provider 可选）"
    ),
    api_base: Optional[str] = typer.Option(
        None, "--api-base", "-b", help="API 基础 URL（某些 provider 可选）"
    ),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="模型名称（必须）"),
    temperature: Optional[float] = typer.Option(
        None,
        "--temperature",
        "-t",
        help="温度参数，控制输出的随机性（默认: 0.3）",
        min=0.0,
        max=2.0,
    ),
    show: bool = typer.Option(False, "--show", "-s", help="显示当前配置"),
):
    """
    配置 LLM 参数

    将 LLM 大模型的配置参数写入到默认配置文件中。
    配置文件路径会根据操作系统自动确定（Windows/macOS/Linux）。

    示例：
        # 配置 OpenAI
        markdown-downloader config --model gpt-4 --api-key sk-xxx

        # 配置本地 Ollama（无需 API key）
        markdown-downloader config --model ollama/llama2

        # 配置自定义 API
        markdown-downloader config --model gpt-3.5-turbo --api-base https://api.example.com

        # 显示当前配置
        markdown-downloader config --show
    """
    if show:
        display_config()
        return

    # 如果没有提供任何参数，显示当前配置
    if all(v is None for v in [api_key, api_base, model, temperature]):
        display_config()
        typer.echo("\n💡 使用 --help 查看配置选项")
        return

    # 验证必须参数
    if model is None and api_key is None and api_base is None and temperature is None:
        typer.echo("⚠️  请至少提供一个配置参数", err=True)
        raise typer.Exit(code=1)

    # 保存配置
    save_config(
        api_key=api_key, api_base=api_base, model=model, temperature=temperature
    )

    # 显示更新后的配置
    typer.echo("")
    display_config()


@app.command("save")
def save_command(
    url: str = typer.Argument(..., help="要下载的目标网页 URL"),
    dir: Path = typer.Option(
        ".",
        "--dir",
        "-d",
        help="保存 Markdown 文件的目录（默认: 当前目录）",
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    title: Optional[str] = typer.Option(
        None,
        "--title",
        "-t",
        help="保存的文件名（不含 .md 扩展名）。如果不指定，将从下载内容的第一行自动提取",
    ),
    timeout: int = typer.Option(
        180,
        "--timeout",
        help="下载超时时间（秒），默认 180 秒（3 分钟）",
        min=1,
    ),
    use_llm: bool = typer.Option(
        False, "--use-llm", "-l", help="使用 LLM 优化 Markdown 内容"
    ),
):
    """
    下载网页的 Markdown 格式并保存到本地

    使用 Jina AI Reader (https://r.jina.ai/) 将网页转换为 Markdown 格式。
    可选择使用 LLM 清理广告和多余内容。

    示例：
        # 基本用法：下载并保存（自动提取标题）
        markdown-downloader save https://example.com

        # 指定标题
        markdown-downloader save https://example.com --title example

        # 保存到指定目录
        markdown-downloader save https://example.com --dir ./docs --title article

        # 使用 LLM 优化内容
        markdown-downloader save https://example.com --title article --use-llm
    """
    # 确保目录存在
    dir.mkdir(parents=True, exist_ok=True)

    # 下载 markdown 内容
    content = download_markdown(url, timeout=timeout)
    if content is None:
        raise typer.Exit(code=1)

    # 如果没有指定 title，尝试从内容第一行提取
    if title is None:
        title = extract_title_from_markdown(content)
        if title:
            typer.echo(f"📝 自动提取标题: {title}")
        else:
            title = "output"
            typer.echo(f"⚠️  无法提取标题，使用默认名称: {title}")

    if use_llm:
        # 先保存原始文件
        raw_filepath = dir / f"{title}.raw.md"
        typer.echo(f"\n💾 保存原始内容到: {raw_filepath}")
        if not save_markdown_to_file(content, str(raw_filepath)):
            raise typer.Exit(code=1)

        # 加载配置
        config = load_config()
        if not validate_config(config):
            typer.echo("\n💡 请先使用 'config' 命令配置 LLM 参数", err=True)
            typer.echo(
                "   示例: markdown-downloader config --model gpt-4 --api-key sk-xxx"
            )
            raise typer.Exit(code=1)

        # 使用 LLM 优化
        optimized_content = optimize_markdown_with_llm(
            content=content,
            api_key=config.get("api_key"),
            api_base=config.get("api_base"),
            model=config["model"],
            temperature=config.get("temperature", 0.3),
        )

        if optimized_content is None:
            typer.echo("\n⚠️  LLM 优化失败，保留原始文件", err=True)
            raise typer.Exit(code=1)

        # 保存优化后的内容
        final_filepath = dir / f"{title}.md"
        typer.echo(f"\n💾 保存优化后的内容到: {final_filepath}")
        if not save_markdown_to_file(optimized_content, str(final_filepath)):
            raise typer.Exit(code=1)

        typer.echo(f"\n✨ 完成! 原始文件: {raw_filepath}, 优化文件: {final_filepath}")
    else:
        # 直接保存
        final_filepath = dir / f"{title}.md"
        if not save_markdown_to_file(content, str(final_filepath)):
            raise typer.Exit(code=1)

        typer.echo(f"\n✨ 完成! 文件已保存: {final_filepath}")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="显示版本信息"),
):
    """
    📥 Markdown Downloader

    使用 Jina AI 下载网页的 Markdown 格式，并可选地使用 LLM 优化内容。
    """
    if version:
        typer.echo("Markdown Downloader v1.0.0")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    app()
