# 项目结构说明

## 📁 目录结构

```
MCP_Test/
├── 📁 services/           # 核心服务层
│   ├── web_service.py     # ColorHunt网站抓取服务
│   ├── file_service.py    # 文件操作服务
│   └── app_service.py     # 应用程序服务
├── 📁 views/              # 视图层 (MVP架构)
│   └── mcp_view.py        # MCP视图组件
├── 📁 presenters/         # 展示层 (MVP架构)
│   └── mcp_presenter.py   # MCP展示器
├── 📁 models/             # 数据模型层
│   └── file_model.py      # 文件和配色方案数据模型
├── 📁 utils/              # 工具类
│   └── config.py          # 配置管理工具
├── 📁 tests/              # 测试文件
│   ├── 📁 colorhunt_api/  # ColorHunt API测试
│   │   ├── test_enhanced_colorhunt.py
│   │   ├── test_realistic_colorhunt.py
│   │   ├── test_summer_palettes.py
│   │   ├── test_tag_scraping.py
│   │   ├── test_jonnymcp_summer.py
│   │   └── test_colorhunt.py
│   ├── 📁 integration/    # 集成测试
│   │   └── test_web_structure.py
│   └── 📁 debug_files/    # 调试文件
│       ├── debug_colorhunt_structure.py
│       ├── debug_mcp.py
│       ├── debug_*.html   # ColorHunt页面调试文件
│       └── colorhunt_*.html # 各标签页面HTML文件
├── 📁 examples/           # 使用示例
│   └── 📁 colorhunt_usage/
│       ├── get_summer_palettes_final.py
│       ├── generate_palettes.py
│       ├── one_palette.py
│       └── mcp_scrape_colorhunt.py
├── 📁 tools/              # 工具集
│   └── 📁 generators/     # 生成器工具
│       └── color_palette_generator.py # 配色方案图片生成器
├── 📁 archive/            # 归档文件
│   └── 📁 legacy/         # 历史版本
│       └── custom_mcp.py  # 原始MCP工具实现
├── 📁 docs/               # 文档
│   ├── 📁 ai-template/    # AI开发模板
│   │   ├── 01_tech_stack.md
│   │   ├── 02_architecture.md
│   │   ├── 03_coding_rules.md
│   │   ├── 04_business_glossary.md
│   │   └── 99_prompt_snippets.md
│   ├── 📁 project/        # 项目文档
│   │   ├── development_log.md    # 开发日志
│   │   ├── PROJECT_SUMMARY.md    # 项目总结
│   │   ├── task_list.md          # 任务清单
│   │   └── PRD.md               # 产品需求文档
│   └── project_structure.md     # 项目结构说明
├── mcp_app.py             # 🚀 MCP工具主入口文件
├── requirements.txt       # 项目依赖
├── README.md              # 项目说明
└── .gitignore            # Git忽略文件
```

## 📋 文件功能说明

### 🚀 主入口文件
- **`mcp_app.py`** - MCP工具的主入口文件，采用MVP架构，包含所有MCP工具函数

### 🔧 核心功能层

#### 服务层 (`services/`)
- **`web_service.py`** - ColorHunt网站数据抓取的核心服务
- **`file_service.py`** - 文件操作和桌面管理服务
- **`app_service.py`** - 应用程序启动服务

#### 视图层 (`views/`)
- **`mcp_view.py`** - MCP视图组件，负责数据展示和用户交互

#### 展示层 (`presenters/`)
- **`mcp_presenter.py`** - MCP展示器，连接模型和视图，处理业务逻辑

#### 模型层 (`models/`)
- **`file_model.py`** - 文件和配色方案的数据模型

#### 工具类 (`utils/`)
- **`config.py`** - 配置管理和应用设置

### 🧪 测试体系 (`tests/`)

#### ColorHunt API测试 (`tests/colorhunt_api/`)
- `test_tag_scraping.py` - 标签页面抓取功能测试
- `test_summer_palettes.py` - 夏天配色方案专项测试
- `test_enhanced_colorhunt.py` - 增强版ColorHunt功能测试
- `test_realistic_colorhunt.py` - 真实数据获取测试
- `test_jonnymcp_summer.py` - JonnyMCP夏天配色方案测试
- `test_colorhunt.py` - ColorHunt基础功能测试

#### 集成测试 (`tests/integration/`)
- `test_web_structure.py` - 网站结构分析集成测试

#### 调试工具 (`tests/debug_files/`)
- `debug_colorhunt_structure.py` - ColorHunt网站结构调试工具
- `debug_mcp.py` - MCP功能调试工具
- `debug_*.html` - 各种调试页面HTML文件
- `colorhunt_*.html` - ColorHunt各标签页面的HTML快照

### 📚 使用示例 (`examples/colorhunt_usage/`)
- `get_summer_palettes_final.py` - 获取夏天配色方案的完整示例
- `generate_palettes.py` - 配色方案生成示例
- `one_palette.py` - 单个配色方案处理示例
- `mcp_scrape_colorhunt.py` - MCP抓取ColorHunt示例

### 🔨 工具集 (`tools/`)

#### 生成器工具 (`tools/generators/`)
- `color_palette_generator.py` - 配色方案图片生成器，支持生成配色预览图

### 📦 归档文件 (`archive/`)

#### 历史版本 (`archive/legacy/`)
- `custom_mcp.py` - 原始MCP工具实现，保留作为参考

### 📖 文档系统 (`docs/`)

#### AI开发模板 (`docs/ai-template/`)
- `01_tech_stack.md` - 技术栈说明
- `02_architecture.md` - 架构设计文档
- `03_coding_rules.md` - 编码规范
- `04_business_glossary.md` - 业务术语表
- `99_prompt_snippets.md` - 提示词片段

#### 项目文档 (`docs/project/`)
- `development_log.md` - 完整的开发历程记录
- `PROJECT_SUMMARY.md` - 项目总结和成果展示
- `task_list.md` - 任务清单和待办事项
- `PRD.md` - 产品需求文档

## 🏗️ 架构设计

### MVP架构模式
- **Model** (`models/`) - 数据模型和业务逻辑
- **View** (`views/`) - 用户界面和数据展示
- **Presenter** (`presenters/`) - 业务逻辑处理和数据转换

### 服务层设计
- **WebService** - 负责网络请求和数据抓取
- **FileService** - 负责文件操作和数据存储
- **AppService** - 负责应用程序启动和系统交互

### 工具层设计
- **Generators** - 各种生成器工具
- **Utilities** - 通用工具和配置管理

## 🔄 开发流程

1. **功能开发** - 在对应的服务层添加新功能
2. **单元测试** - 在`tests/`对应目录添加测试文件
3. **集成测试** - 在`tests/integration/`添加集成测试
4. **示例创建** - 在`examples/`添加使用示例
5. **工具开发** - 在`tools/`添加辅助工具
6. **文档更新** - 更新相关文档和README

## 📝 命名规范

### 文件命名
- 主入口文件：`mcp_app.py`
- 测试文件：`test_*.py`
- 调试文件：`debug_*.py`
- 示例文件：功能描述性命名
- HTML文件：`colorhunt_page_*.html` 或 `debug_*.html`

### 文件夹命名
- 功能模块：小写单词，下划线分隔
- 测试分类：功能描述性命名
- 示例分类：用途描述性命名
- 工具分类：工具类型命名

## 🚀 快速开始

1. **运行主要功能**：`python mcp_app.py` 🚀
2. **运行测试**：`python -m pytest tests/`
3. **查看示例**：`python examples/colorhunt_usage/get_summer_palettes_final.py`
4. **使用生成器**：`python tools/generators/color_palette_generator.py`
5. **调试功能**：`python tests/debug_files/debug_colorhunt_structure.py`
6. **查看历史版本**：`python archive/legacy/custom_mcp.py`

## 📊 项目统计

### 文件分布
- **核心代码**: 9个文件 (services, views, presenters, models, utils + mcp_app.py)
- **测试文件**: 9个文件 (API测试 + 集成测试 + 调试工具)
- **示例文件**: 4个文件 (ColorHunt使用示例)
- **工具文件**: 1个文件 (配色方案生成器)
- **文档文件**: 10个文件 (项目文档 + AI模板)
- **归档文件**: 1个文件 (历史版本)

### 目录层次
- **一级目录**: 11个 (功能模块 + 特殊目录)
- **二级目录**: 8个 (分类子目录)
- **总文件数**: 34个 (不含HTML调试文件) 