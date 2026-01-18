#!/usr/bin/env python3
"""
快速示例 - 演示 markdown-downloader 的功能
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║         📥 Markdown Downloader - 快速示例                      ║
╚════════════════════════════════════════════════════════════════╝

这个工具可以：
1. 📥 下载网页的 Markdown 格式
2. ⚙️ 配置和使用 LLM 优化内容
3. 📁 保存到指定目录

════════════════════════════════════════════════════════════════

示例命令：

1️⃣  查看帮助
   python main.py --help

2️⃣  下载网页（自动提取标题）
   python main.py save https://example.com

3️⃣  下载网页（手动指定标题）
   python main.py save https://example.com --title example

4️⃣  保存到指定目录
   python main.py save https://example.com --dir ./downloads

5️⃣  配置 LLM（OpenAI）
   python main.py config --model gpt-4 --api-key sk-your-key

6️⃣  配置 LLM（本地 Ollama，无需 API key）
   python main.py config --model ollama/llama2

7️⃣  查看当前配置
   python main.py config --show

8️⃣  使用 LLM 下载并优化内容
   python main.py save https://example.com --title article --use-llm

   这会生成两个文件：
   - article.raw.md    (原始内容)
   - article.md        (LLM 优化后的内容)

9️⃣  自定义下载超时时间
   python main.py save https://example.com --timeout 300

   适用于网络较慢或内容较大的网页

════════════════════════════════════════════════════════════════

🔧 支持的 LLM 提供商（通过 LiteLLM）：

• OpenAI: gpt-4, gpt-3.5-turbo, gpt-4-turbo
• Anthropic: claude-3-opus, claude-3-sonnet
• Google: gemini/gemini-pro
• 本地 Ollama: ollama/llama2, ollama/mistral
• 更多...

════════════════════════════════════════════════════════════════

📚 更多信息请查看 README.md
""")
