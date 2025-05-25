# JonnyMCP 桌面工具集

## 项目简介

JonnyMCP是一个基于Python的桌面工具集，采用MVP架构设计，提供文件整理、应用启动、ColorHunt配色方案抓取等实用功能。该项目使用面向对象编程原则和设计模式，具有良好的可维护性和可扩展性。

## 🚀 功能特性

### 桌面管理工具
- **桌面文件列表**: 获取桌面上的所有文件
- **桌面文件整理**: 根据文件类型自动分类整理桌面文件
- **应用程序启动**: 打开谷歌浏览器等应用程序
- **个性化问候**: 生成中英双语个性化问候语

### ColorHunt配色方案抓取 🎨
- **标签页面抓取**: 支持通过标签获取ColorHunt配色方案
- **真实数据获取**: 直接调用ColorHunt官方API，获取真实的点赞数、发布时间
- **多标签支持**: 支持summer、retro、vintage、pastel、neon等标签
- **准确数据**: 所有颜色代码和配色方案网址均为准确数据

## 📁 项目结构

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
│   ├── 📁 integration/    # 集成测试
│   └── 📁 debug_files/    # 调试文件和HTML快照
├── 📁 examples/           # 使用示例
│   └── 📁 colorhunt_usage/ # ColorHunt使用示例
├── 📁 tools/              # 工具集
│   └── 📁 generators/     # 生成器工具
│       └── color_palette_generator.py # 配色方案图片生成器
├── 📁 archive/            # 归档文件
│   └── 📁 legacy/         # 历史版本
│       └── custom_mcp.py  # 原始MCP工具实现
├── 📁 docs/               # 文档
│   ├── 📁 ai-template/    # AI开发模板
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

## 🏗️ 项目架构

项目采用MVP(Model-View-Presenter)架构模式，分为以下几层:

```
JonnyMCP
├── Models      - 数据模型层
├── Views       - 视图层
├── Presenters  - 表示层
├── Services    - 服务层
├── Tools       - 工具层
├── Utils       - 工具类
└── Archive     - 归档层
```

### 架构图

```
┌───────────────┐     ┌────────────────┐     ┌──────────────┐
│     Model     │◄────┤    Presenter   │◄────┤     View     │
│  (数据模型)    │     │   (业务逻辑)    │     │   (界面)     │
└───────┬───────┘     └────────┬───────┘     └──────────────┘
        │                      │                      ▲
        │                      │                      │
        │                      ▼                      │
        │             ┌────────────────┐              │
        └────────────►│    Service     │──────────────┘
                      │   (服务实现)    │
                      └────────────────┘
```

## 🎨 ColorHunt功能展示

### 获取夏天主题配色方案
```python
# 使用JonnyMCP工具获取3种夏天配色方案
from services.web_service import WebService

success, error, palettes = WebService.scrape_colorhunt_by_tag('summer', 3)

# 示例输出：
# Summer Palette 1: #FE5D26 | #F2C078 | #FAEDCA | #C1DBB3 (583点赞)
# Summer Palette 2: #537D5D | #73946B | #9EBC8A | #D2D0A0 (1913点赞)  
# Summer Palette 3: #4ED7F1 | #6FE6FC | #A8F1FF | #FFFA8D (1167点赞)
```

### 支持的标签
- **季节类**: summer, fall, winter, spring
- **风格类**: vintage, retro, pastel, neon
- **颜色类**: blue, green, red, yellow, pink, purple
- **特殊类**: nature, space, gradient, rainbow

## 🚀 快速开始

### 1. 环境准备
```bash
# 克隆项目
git clone https://github.com/xiyuxzq/MCP_Test.git
cd MCP_Test

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行主要功能
```bash
# 🚀 启动MCP主服务
python mcp_app.py

# 运行ColorHunt配色方案获取示例
python examples/colorhunt_usage/get_summer_palettes_final.py

# 使用配色方案生成器
python tools/generators/color_palette_generator.py
```

### 3. 运行测试
```bash
# 运行所有测试
python -m pytest tests/

# 运行ColorHunt API测试
python tests/colorhunt_api/test_tag_scraping.py

# 运行调试工具
python tests/debug_files/debug_colorhunt_structure.py
```

### 4. 查看历史版本
```bash
# 运行原始版本 (归档)
python archive/legacy/custom_mcp.py
```

## 📋 使用方法

### 桌面管理功能
```python
# 列出桌面文件
list_desktop_files()

# 整理桌面文件
create_folder_and_move_files()

# 打开谷歌浏览器
open_chrome()

# 生成问候语
say_hello("Jonny")
```

### ColorHunt配色方案抓取
```python
# 获取指定标签的配色方案
scrape_colorhunt_palettes(5)

# 测试简化版本
test_simple_colorhunt(3)
```

## 🔧 技术特点

### ColorHunt API集成
- **官方API调用**: 直接调用`https://colorhunt.co/php/feed.php`
- **真实数据**: 获取真实的点赞数、发布时间和配色方案信息
- **准确网址**: 提供真实有效的ColorHunt配色方案链接
- **多标签支持**: 支持所有ColorHunt官方标签

### 架构优势
- **MVP模式**: 清晰的分层架构，易于维护和扩展
- **面向对象**: 使用OOP原则，提高代码复用性
- **设计模式**: 应用多种设计模式，提高代码质量
- **测试覆盖**: 完整的测试体系，确保功能稳定性

### 项目组织
- **模块化设计**: 清晰的文件夹分类和职责分离
- **工具集成**: 独立的工具层，支持各种生成器和实用工具
- **版本管理**: 归档历史版本，保持项目演进记录
- **文档完善**: 完整的文档体系和开发指南

## 📚 文档

- [项目结构说明](docs/project_structure.md) - 详细的项目结构和文件说明
- [开发日志](docs/project/development_log.md) - 完整的开发历程记录
- [项目总结](docs/project/PROJECT_SUMMARY.md) - 项目成果和技术亮点
- [AI开发模板](docs/ai-template/) - AI辅助开发的模板和规范

## 🤝 贡献指南

1. **功能开发** - 在对应的服务层添加新功能
2. **单元测试** - 在`tests/`对应目录添加测试文件
3. **集成测试** - 在`tests/integration/`添加集成测试
4. **示例创建** - 在`examples/`添加使用示例
5. **工具开发** - 在`tools/`添加辅助工具
6. **文档更新** - 更新相关文档和README

## 📄 许可证

本项目采用MIT许可证，详情请参阅LICENSE文件。

## 🔗 相关链接

- [ColorHunt官网](https://colorhunt.co/) - 配色方案来源网站
- [GitHub仓库](https://github.com/xiyuxzq/MCP_Test) - 项目源代码 