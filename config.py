"""
配置管理模块
用于处理 LLM 配置文件的读写操作
"""

import json
from pathlib import Path
from typing import Optional
from platformdirs import user_config_dir
import typer

# 配置文件名称
CONFIG_FILE_NAME = "config.json"
APP_NAME = "markdown-downloader"
APP_AUTHOR = "markdown-downloader"


def get_config_path() -> Path:
    """
    获取配置文件的完整路径
    使用 platformdirs 确保跨平台兼容
    """
    config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / CONFIG_FILE_NAME


def load_config() -> dict:
    """
    加载配置文件
    如果配置文件不存在，返回空字典
    """
    config_path = get_config_path()
    if not config_path.exists():
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        typer.echo(f"⚠️  读取配置文件失败: {e}", err=True)
        return {}


def save_config(
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
) -> None:
    """
    保存配置到配置文件

    参数:
        api_key: API密钥（可选，某些 provider 可以为空）
        api_base: API基础URL（可选，某些 provider 可以为空）
        model: 模型名称（必须）
        temperature: 温度参数（可选，默认0.3）
    """
    # 加载现有配置
    config = load_config()

    # 更新配置
    if api_key is not None:
        config["api_key"] = api_key
    if api_base is not None:
        config["api_base"] = api_base
    if model is not None:
        config["model"] = model
    if temperature is not None:
        config["temperature"] = temperature
    elif "temperature" not in config:
        config["temperature"] = 0.3  # 默认值

    # 保存到文件
    config_path = get_config_path()
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, indent=2, ensure_ascii=False, fp=f)
        typer.echo(f"✅ 配置已保存到: {config_path}")
    except IOError as e:
        typer.echo(f"❌ 保存配置失败: {e}", err=True)
        raise typer.Exit(code=1)


def validate_config(config: dict) -> bool:
    """
    验证配置是否有效

    参数:
        config: 配置字典

    返回:
        True 如果配置有效，否则 False
    """
    if not config:
        typer.echo("❌ 配置文件为空，请先使用 'config' 命令配置 LLM", err=True)
        return False

    if "model" not in config:
        typer.echo("❌ 配置中缺少 'model' 参数，请先配置", err=True)
        return False

    return True


def display_config() -> None:
    """
    显示当前配置
    """
    config = load_config()
    config_path = get_config_path()

    typer.echo(f"\n📁 配置文件路径: {config_path}\n")

    if not config:
        typer.echo("⚠️  配置文件为空")
        return

    typer.echo("📋 当前配置:")
    typer.echo("-" * 40)
    for key, value in config.items():
        # 隐藏 API key 的部分内容
        if key == "api_key" and value:
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            typer.echo(f"  {key}: {masked_value}")
        else:
            typer.echo(f"  {key}: {value}")
    typer.echo("-" * 40)
