# 架构设计

## 架构模式
本项目采用MVP（Model-View-Presenter）架构模式，清晰分离数据模型、视图展示和业务逻辑。

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│    Model    │◄────►│  Presenter  │◄────►│    View     │
└─────────────┘      └─────────────┘      └─────────────┘
       ▲                    ▲                    ▲
       │                    │                    │
       ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Services  │      │    Utils    │      │     MCP     │
└─────────────┘      └─────────────┘      └─────────────┘
```

## 目录结构

```
MCP_Test/
├── mcp_app.py           # 应用程序入口
├── custom_mcp.py        # MCP工具注册
├── README.md            # 项目说明文档
├── development_log.md   # 开发日志
│
├── models/              # 数据模型层
│   ├── __init__.py
│   ├── file_model.py    # 文件模型
│   └── file_type.py     # 文件类型模型
│
├── views/               # 视图层
│   ├── __init__.py
│   └── mcp_view.py      # MCP视图接口和实现
│
├── presenters/          # 表示层
│   ├── __init__.py
│   └── mcp_presenter.py # MCP表示层
│
├── services/            # 服务层
│   ├── __init__.py
│   ├── app_service.py   # 应用程序服务
│   ├── file_service.py  # 文件服务
│   └── web_service.py   # 网络服务
│
├── utils/               # 工具类
│   ├── __init__.py
│   └── config.py        # 配置工具
│
└── docs/                # 文档
    └── ai-template/     # AI开发模板
        ├── 01_tech_stack.md         # 技术栈
        ├── 02_architecture.md       # 架构设计
        ├── 03_coding_rules.md       # 编码规范
        ├── 04_business_glossary.md  # 业务术语
        └── 99_prompt_snippets.md    # 提示词片段
```

## 分层设计

### 模型层 (Models)
- 负责定义数据结构和业务实体
- 包含数据验证和转换逻辑
- 例如：FileModel, FileType

### 视图层 (Views)
- 负责信息的展示和格式化
- 不包含业务逻辑
- 例如：IMcpView, McpView

### 表示层 (Presenters)
- 连接模型层和视图层
- 处理用户操作和业务逻辑
- 例如：McpPresenter

### 服务层 (Services)
- 提供特定领域的功能服务
- 封装底层实现细节
- 例如：FileService, AppService, WebService

### 工具层 (Utils)
- 提供通用工具和辅助功能
- 不包含特定业务逻辑
- 例如：Config

## 数据流
1. MCP工具接收用户请求
2. Presenter层处理请求并调用相应Service
3. Service层执行业务逻辑，可能使用Model层
4. 处理结果通过Presenter返回给View层
5. View层格式化结果并返回给用户

## 扩展性设计
- 通过接口定义实现松耦合
- 使用依赖注入提高可测试性
- 采用设计模式提升代码质量 