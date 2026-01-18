# Makefile for markdown-downloader
# 支持 Windows, Linux, macOS 跨平台编译和安装

# 项目名称
APP_NAME = markdown-downloader
MAIN_FILE = main.py

# 检测操作系统
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    BINARY_NAME := $(APP_NAME).exe
    # Windows 安装目录：使用用户本地 AppData\Local\Programs
    INSTALL_DIR := $(LOCALAPPDATA)\Programs
else
    DETECTED_OS := $(shell uname -s)
    BINARY_NAME := $(APP_NAME)
    # Linux 和 macOS 安装目录
    INSTALL_DIR := $(HOME)/.local/bin
endif

# PyInstaller 输出目录
DIST_DIR = dist
BUILD_DIR = build
SPEC_FILE = $(APP_NAME).spec

# 颜色输出（仅在 Unix 系统上）
ifneq ($(OS),Windows_NT)
    GREEN := \033[0;32m
    YELLOW := \033[0;33m
    RED := \033[0;31m
    NC := \033[0m # No Color
else
    GREEN :=
    YELLOW :=
    RED :=
    NC :=
endif

.PHONY: all build install clean help

# 默认目标
all: build

# 帮助信息
help:
	@echo "$(GREEN)markdown-downloader Makefile$(NC)"
	@echo ""
	@echo "可用命令："
	@echo "  $(YELLOW)make build$(NC)     - 使用 PyInstaller 编译单文件可执行程序"
	@echo "  $(YELLOW)make install$(NC)   - 安装编译后的二进制文件到系统目录"
	@echo "  $(YELLOW)make clean$(NC)     - 清理编译产生的临时文件"
	@echo "  $(YELLOW)make help$(NC)      - 显示此帮助信息"
	@echo ""
	@echo "检测到的操作系统: $(DETECTED_OS)"
	@echo "二进制文件名: $(BINARY_NAME)"
	@echo "安装目录: $(INSTALL_DIR)"

# 编译单文件可执行程序
build:
	@echo "$(GREEN)>>> 开始编译 $(APP_NAME) for $(DETECTED_OS)...$(NC)"
	@echo "$(YELLOW)>>> 使用 PyInstaller 打包为单文件...$(NC)"
	pyinstaller --onefile \
		--name $(APP_NAME) \
		--clean \
		--noconfirm \
		--hidden-import=litellm \
		--hidden-import=litellm.litellm_core_utils \
		--hidden-import=litellm.litellm_core_utils.tokenizers \
		--hidden-import=tiktoken_ext.openai_public \
		--hidden-import=tiktoken_ext \
		--collect-all litellm \
		--collect-data tiktoken_ext \
		--copy-metadata litellm \
		--copy-metadata tiktoken \
		$(MAIN_FILE)
	@echo "$(GREEN)>>> 编译完成！$(NC)"
	@echo "$(GREEN)>>> 二进制文件位置: $(DIST_DIR)/$(BINARY_NAME)$(NC)"

# 安装二进制文件到系统目录
install: build
	@echo "$(GREEN)>>> 开始安装 $(BINARY_NAME)...$(NC)"
ifeq ($(OS),Windows_NT)
	@echo "$(YELLOW)>>> Windows 系统：安装到 $(INSTALL_DIR)$(NC)"
	@if not exist "$(INSTALL_DIR)" mkdir "$(INSTALL_DIR)"
	@copy /Y "$(DIST_DIR)\$(BINARY_NAME)" "$(INSTALL_DIR)\$(BINARY_NAME)"
	@echo "$(GREEN)>>> 安装成功！$(NC)"
	@echo "$(YELLOW)>>> 请确保 $(INSTALL_DIR) 在系统 PATH 环境变量中$(NC)"
else
	@echo "$(YELLOW)>>> $(DETECTED_OS) 系统：安装到 $(INSTALL_DIR)$(NC)"
	@mkdir -p $(INSTALL_DIR)
	@cp -f $(DIST_DIR)/$(BINARY_NAME) $(INSTALL_DIR)/$(BINARY_NAME)
	@chmod +x $(INSTALL_DIR)/$(BINARY_NAME)
	@echo "$(GREEN)>>> 安装成功！$(NC)"
	@echo "$(YELLOW)>>> 请确保 $(INSTALL_DIR) 在 PATH 环境变量中$(NC)"
	@echo "$(YELLOW)>>> 可以运行: export PATH=\"\$$HOME/.local/bin:\$$PATH\"$(NC)"
endif
	@echo ""
	@echo "$(GREEN)>>> 安装完成！现在可以使用 '$(APP_NAME)' 命令$(NC)"

# 清理编译临时文件
clean:
	@echo "$(YELLOW)>>> 清理临时文件...$(NC)"
ifeq ($(OS),Windows_NT)
	@if exist "$(BUILD_DIR)" rmdir /S /Q "$(BUILD_DIR)"
	@if exist "$(DIST_DIR)" rmdir /S /Q "$(DIST_DIR)"
	@if exist "$(SPEC_FILE)" del /Q "$(SPEC_FILE)"
	@if exist "__pycache__" rmdir /S /Q "__pycache__"
	@for /d %%i in (*.egg-info) do @rmdir /S /Q "%%i"
else
	@rm -rf $(BUILD_DIR) $(DIST_DIR) $(SPEC_FILE)
	@rm -rf __pycache__ *.egg-info
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
endif
	@echo "$(GREEN)>>> 清理完成！$(NC)"

# 卸载
uninstall:
	@echo "$(YELLOW)>>> 卸载 $(BINARY_NAME)...$(NC)"
ifeq ($(OS),Windows_NT)
	@if exist "$(INSTALL_DIR)\$(BINARY_NAME)" del /Q "$(INSTALL_DIR)\$(BINARY_NAME)"
else
	@rm -f $(INSTALL_DIR)/$(BINARY_NAME)
endif
	@echo "$(GREEN)>>> 卸载完成！$(NC)"

# 测试编译后的程序
test: build
	@echo "$(GREEN)>>> 测试编译后的程序...$(NC)"
ifeq ($(OS),Windows_NT)
	@$(DIST_DIR)\$(BINARY_NAME) --version
	@$(DIST_DIR)\$(BINARY_NAME) --help
else
	@$(DIST_DIR)/$(BINARY_NAME) --version
	@$(DIST_DIR)/$(BINARY_NAME) --help
endif
	@echo "$(GREEN)>>> 测试完成！$(NC)"
