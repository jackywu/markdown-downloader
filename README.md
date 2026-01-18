# 📥 Markdown Downloader

使用 Typer 和 LiteLLM 构建的命令行工具，用于下载网页的 Markdown 格式，并可选地使用 LLM 优化内容。

## ✨ 功能特性

- 🌐 **网页转 Markdown**：使用 [Jina AI Reader](https://jina.ai/reader) 将任意网页转换为 Markdown 格式
- 📝 **智能标题提取**：自动从下载内容第一行提取标题作为文件名
- 🤖 **LLM 优化**：可选使用大语言模型清理广告和多余内容
- ⚙️ **灵活配置**：支持多种 LLM 提供商（OpenAI、Anthropic、Ollama 等）
- 🔧 **跨平台**：使用 `platformdirs` 确保 Windows、macOS、Linux 多平台支持
- 📁 **智能保存**：自定义保存路径和文件名

## 📦 安装

### 前置要求

- Python 3.12 或更高版本
- uv 包管理器（推荐）或 pip

### 使用 uv（推荐）

```bash
# 安装依赖
uv sync

# 或者使用 pip
pip install -e .
```

## 🚀 快速开始

### 1. 配置 LLM（如果需要使用 `--use-llm` 功能）

```bash
# 配置 OpenAI
python main.py config --model gpt-4 --api-key sk-xxx

# 配置本地 Ollama（无需 API key）
python main.py config --model ollama/llama2

# 配置自定义 API 端点
python main.py config --model gpt-3.5-turbo --api-base https://api.example.com

# 自定义温度参数
python main.py config --model gpt-4 --temperature 0.5

# 查看当前配置
python main.py config --show
```

### 2. 下载网页为 Markdown

```bash
# 基本用法：下载网页并保存（自动提取标题）
python main.py save https://example.com

# 手动指定标题
python main.py save https://example.com --title example

# 保存到指定目录
python main.py save https://example.com --dir ./docs

# 手动指定标题并使用 LLM 优化内容（需要先配置 LLM）
python main.py save https://example.com --title article --use-llm
```

## 📖 命令详解

### `config` 子命令

配置 LLM 参数，用于优化 Markdown 内容。

**选项：**

- `--api-key, -k`：API 密钥（某些 provider 可选）
- `--api-base, -b`：API 基础 URL（某些 provider 可选）
- `--model, -m`：模型名称（必须）
- `--temperature, -t`：温度参数，范围 0.0-2.0（默认: 0.3）
- `--show, -s`：显示当前配置

**配置文件位置：**

- **Linux**: `~/.config/markdown-downloader/config.json`
- **macOS**: `~/Library/Application Support/markdown-downloader/config.json`
- **Windows**: `C:\Users\<username>\AppData\Local\markdown-downloader\markdown-downloader\config.json`

**支持的 LLM 提供商：**

通过 LiteLLM，支持以下提供商：

- OpenAI (`gpt-4`, `gpt-3.5-turbo` 等)
- Anthropic (`claude-3-opus`, `claude-3-sonnet` 等)
- Google (`gemini/gemini-pro` 等)
- Cohere (`command-nightly` 等)
- Mistral (`mistral/mistral-medium` 等)
- Ollama 本地模型 (`ollama/llama2`, `ollama/mistral` 等)
- Together AI (`together_ai/...` 等)
- 更多...

对于 LiteLLM 内建支持的 provider，`api_key` 和 `api_base` 可以为空。

### `save` 子命令

下载网页的 Markdown 格式并保存到本地。

**参数：**

- `url`（必需）：要下载的目标网页 URL

**选项：**

- `--dir, -d`：保存 Markdown 文件的目录（默认: 当前目录）
- `--title, -t`：保存的文件名，不含 `.md` 扩展名（可选，默认自动从内容第一行提取）
- `--timeout`：下载超时时间（秒），默认 180 秒（3 分钟）
- `--use-llm, -l`：使用 LLM 优化 Markdown 内容

**关于 `--title` 参数：**

Jina AI 返回的 Markdown 内容第一行格式为 `Title: {文章标题}`。如果不指定 `--title` 参数，程序会自动提取这个标题作为文件名。如果提取失败，将使用默认名称 `output`。

**使用 `--use-llm` 时的行为：**

1. 下载原始 Markdown 内容
2. 保存原始内容到 `{title}.raw.md`
3. 使用配置的 LLM 优化内容（清理广告、多余文案）
4. 保存优化后的内容到 `{title}.md`

如果不使用 `--use-llm`，直接保存到 `{title}.md`。

## 💡 使用示例

### 示例 1: 下载技术文档

```bash
# 自动提取标题下载
python main.py save https://docs.python.org/3/tutorial/index.html

# 或手动指定标题
python main.py save https://docs.python.org/3/tutorial/index.html --title python-tutorial
```

### 示例 2: 下载并使用 LLM 优化博客文章

```bash
# 先配置 LLM
python main.py config --model gpt-4 --api-key sk-xxx

# 下载并优化
python main.py save https://blog.example.com/article --title article --use-llm

# 结果：
# - article.raw.md  （原始内容）
# - article.md      （优化后的内容）
```

### 示例 3: 批量下载到指定目录

```bash
# 创建目录并下载多篇文章（自动提取标题）
mkdir -p ./articles

python main.py save https://example.com/post1 --dir ./articles
python main.py save https://example.com/post2 --dir ./articles
python main.py save https://example.com/post3 --dir ./articles
```

### 示例 4: 使用本地 Ollama 模型

```bash
# 配置 Ollama（无需 API key）
python main.py config --model ollama/llama2

# 下载并使用本地 LLM 优化
python main.py save https://example.com/article --title article --use-llm
```

### 示例 5: 自定义下载超时时间

```bash
# 对于网络较慢或内容较大的网页，可以增加超时时间
python main.py save https://example.com/large-article --timeout 300

# 对于快速响应的网站，可以减少超时时间
python main.py save https://example.com/quick-page --timeout 30
```

## 🛠️ 项目结构

```
markdown-downloader/
├── main.py              # 主入口，Typer CLI 应用
├── config.py            # 配置管理模块
├── downloader.py        # Markdown 下载模块（含标题提取）
├── optimizer.py         # LLM 优化模块
├── pyproject.toml       # 项目配置
└── README.md            # 本文件
```

## 🔧 技术栈

- **CLI 框架**: [Typer](https://typer.tiangolo.com/) - 现代化的 Python CLI 构建工具
- **LLM 集成**: [LiteLLM](https://docs.litellm.ai/) - 统一的 LLM API 接口
- **跨平台支持**: [platformdirs](https://github.com/platformdirs/platformdirs) - 跨平台目录路径
- **HTTP 请求**: [requests](https://requests.readthedocs.io/) - HTTP 库
- **Markdown 转换**: [Jina AI Reader](https://jina.ai/reader) - 网页转 Markdown 服务

## 📝 开发指南

### 运行测试

```bash
# 查看帮助
python main.py --help

# 查看子命令帮助
python main.py config --help
python main.py save --help
```

### 代码结构

1. **main.py**: 定义 Typer 应用和子命令
2. **config.py**: 处理配置文件的读写和验证
3. **downloader.py**: 从 Jina AI 下载 Markdown 内容和提取标题
4. **optimizer.py**: 使用 LiteLLM 调用 LLM 优化内容

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Jina AI](https://jina.ai/) - 提供优秀的网页转 Markdown 服务
- [LiteLLM](https://docs.litellm.ai/) - 简化 LLM API 调用
- [Typer](https://typer.tiangolo.com/) - 优雅的 CLI 框架

---

Made with ❤️ by the Markdown Downloader Team
