"""
LLM 优化模块
使用 LiteLLM 调用大语言模型优化 markdown 内容
"""

from typing import Optional
import typer
from litellm import completion
import os


def optimize_markdown_with_llm(
    content: str,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.3,
) -> Optional[str]:
    """
    使用 LLM 优化 markdown 内容
    清理广告和多余文案

    参数:
        content: 原始 markdown 内容
        api_key: API密钥
        api_base: API基础URL
        model: 模型名称
        temperature: 温度参数

    返回:
        优化后的 markdown 内容，如果失败返回 None
    """
    try:
        typer.echo("🤖 正在使用 LLM 优化内容...")

        # 设置环境变量（如果提供）
        if api_key:
            # 检测provider并设置相应的环境变量
            provider = _detect_provider(model)
            if provider:
                env_key = f"{provider.upper()}_API_KEY"
                os.environ[env_key] = api_key

        # 构建请求参数
        kwargs = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": """你是一个专业的 Markdown 内容编辑助手。你的任务是：
1. 清理文档中的广告内容
2. 删除无关的营销信息
3. 删除页面导航、侧边栏、页脚等非正文内容
4. 保留文章的核心内容和结构
5. 保持 Markdown 格式的正确性和可读性
6. 修正明显的格式错误
7. 不要添加任何自己的评论或说明，直接输出优化后的 Markdown 内容""",
                },
                {
                    "role": "user",
                    "content": f"请优化以下 Markdown 内容，去除广告和多余文案，只保留核心内容：\n\n{content}",
                },
            ],
            "temperature": temperature,
            "drop_params": True,
        }

        # 如果提供了 api_base，添加到参数中
        if api_base:
            kwargs["api_base"] = api_base

        # 调用 LLM
        response = completion(**kwargs)

        # 提取优化后的内容
        optimized_content = response.choices[0].message.content

        if not optimized_content or len(optimized_content.strip()) == 0:
            typer.echo("⚠️  LLM 返回的内容为空", err=True)
            return None

        typer.echo(f"✅ 优化完成，新内容长度: {len(optimized_content)} 字符")
        return optimized_content

    except Exception as e:
        typer.echo(f"❌ LLM 优化失败: {e}", err=True)
        typer.echo("💡 提示: 请检查 API 配置是否正确", err=True)
        return None


def _detect_provider(model: str) -> Optional[str]:
    """
    检测模型所属的 provider

    参数:
        model: 模型名称

    返回:
        provider 名称，如果无法检测返回 None
    """
    # 常见的 provider 前缀
    provider_prefixes = {
        "gpt": "openai",
        "claude": "anthropic",
        "gemini": "gemini",
        "command": "cohere",
        "mistral": "mistral",
        "together": "together_ai",
        "ollama": "ollama",
        "azure": "azure",
        "bedrock": "bedrock",
        "vertex": "vertex_ai",
    }

    model_lower = model.lower()
    for prefix, provider in provider_prefixes.items():
        if model_lower.startswith(prefix):
            return provider

    # 如果模型名称包含 '/' 可能是 together_ai 或 huggingface 格式
    if "/" in model:
        return None  # 让 litellm 自动检测

    return None
