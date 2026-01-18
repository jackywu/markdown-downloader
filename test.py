#!/usr/bin/env python3
"""
测试脚本 - 验证 markdown-downloader 的基本功能
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """运行命令并返回结果"""
    print(f"\n🔧 运行命令: {' '.join(cmd)}")
    print("=" * 60)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print("=" * 60)
    return result.returncode == 0


def main():
    """主测试函数"""
    print("=" * 60)
    print("📋 Markdown Downloader 功能测试")
    print("=" * 60)

    # 测试 1: 显示帮助
    print("\n✅ 测试 1: 显示主帮助信息")
    if not run_command([sys.executable, "main.py", "--help"]):
        print("❌ 测试失败")
        return False

    # 测试 2: 显示 config 帮助
    print("\n✅ 测试 2: 显示 config 子命令帮助")
    if not run_command([sys.executable, "main.py", "config", "--help"]):
        print("❌ 测试失败")
        return False

    # 测试 3: 显示 save 帮助
    print("\n✅ 测试 3: 显示 save 子命令帮助")
    if not run_command([sys.executable, "main.py", "save", "--help"]):
        print("❌ 测试失败")
        return False

    # 测试 4: 显示当前配置（可能为空）
    print("\n✅ 测试 4: 显示当前配置")
    run_command([sys.executable, "main.py", "config", "--show"])

    # 测试 5: 配置示例（使用 Ollama，不需要 API key）
    print("\n✅ 测试 5: 配置 LLM（使用 ollama/llama2 作为示例）")
    if not run_command(
        [
            sys.executable,
            "main.py",
            "config",
            "--model",
            "ollama/llama2",
            "--temperature",
            "0.3",
        ]
    ):
        print("❌ 测试失败")
        return False

    # 测试 6: 验证配置已保存
    print("\n✅ 测试 6: 验证配置已保存")
    if not run_command([sys.executable, "main.py", "config", "--show"]):
        print("❌ 测试失败")
        return False

    # 测试 7: 下载一个简单的网页（不使用 LLM）
    print("\n✅ 测试 7: 下载网页为 Markdown（不使用 LLM）")
    test_dir = Path("./test_output")
    test_dir.mkdir(exist_ok=True)

    if not run_command(
        [
            sys.executable,
            "main.py",
            "save",
            "https://example.com",
            "--dir",
            str(test_dir),
            "--title",
            "test_example",
        ]
    ):
        print("❌ 测试失败")
        return False

    # 检查文件是否创建
    output_file = test_dir / "test_example.md"
    if output_file.exists():
        print(f"\n✅ 文件创建成功: {output_file}")
        print(f"📄 文件大小: {output_file.stat().st_size} 字节")

        # 显示前几行
        with open(output_file, "r", encoding="utf-8") as f:
            lines = f.readlines()[:10]
            print("\n📖 文件前 10 行预览:")
            print("-" * 60)
            for i, line in enumerate(lines, 1):
                print(f"{i}: {line.rstrip()}")
            print("-" * 60)
    else:
        print(f"\n❌ 文件未创建: {output_file}")
        return False

    print("\n" + "=" * 60)
    print("✅ 所有基本测试通过！")
    print("=" * 60)
    print("\n💡 提示:")
    print("  - 要测试 LLM 优化功能，需要先配置有效的 API key")
    print("  - 然后运行: python main.py save <URL> --title <NAME> --use-llm")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
