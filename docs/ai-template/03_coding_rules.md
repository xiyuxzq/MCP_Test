# 编码规范

## 命名规范

### 文件命名
- 使用小写字母和下划线
- 模块名使用单数形式
- 例如：`file_service.py`, `mcp_view.py`

### 类命名
- 使用驼峰命名法（CamelCase）
- 类名使用名词，表示对象
- 例如：`FileService`, `McpPresenter`

### 方法/函数命名
- 使用小写字母和下划线（snake_case）
- 函数名使用动词开头，表示动作
- 例如：`list_desktop_files()`, `organize_desktop_files()`

### 变量命名
- 使用小写字母和下划线（snake_case）
- 变量名应该具有描述性
- 例如：`file_list`, `error_message`

### 常量命名
- 使用全大写字母和下划线
- 例如：`MAX_FILES`, `DEFAULT_TIMEOUT`

## 代码格式化

### 缩进
- 使用4个空格进行缩进
- 不使用制表符（Tab）

### 行长度
- 每行代码不超过120个字符
- 对于长行，使用适当的换行和缩进

### 空行
- 在顶级函数和类定义之间使用两个空行
- 在类内的方法之间使用一个空行
- 在函数内的逻辑块之间使用一个空行

### 导入顺序
1. 标准库导入
2. 相关第三方库导入
3. 本地应用/库导入

## 文档注释

### 模块注释
- 每个模块文件应该包含一个文档字符串
- 描述模块的功能和用途

### 类注释
- 每个类应该有一个文档字符串
- 描述类的功能、责任和使用方式

### 方法/函数注释
- 使用Google风格的文档字符串
- 包含功能描述、参数、返回值和异常
```python
def example_function(param1, param2):
    """
    函数功能描述
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述
        
    Returns:
        返回值的描述
        
    Raises:
        ExceptionType: 异常的描述
    """
    pass
```

## 异常处理

### 异常捕获
- 只捕获预期的异常，避免捕获所有异常
- 在适当的层次处理异常，不在所有函数中都添加try-except

### 异常传递
- 使用异常传递机制，而不是返回错误码
- 在服务层捕获底层异常并转换为业务异常

### 自定义异常
- 为特定的错误情况定义自定义异常类
- 继承自适当的基础异常类

## 日志记录

### 日志级别
- DEBUG: 详细的调试信息
- INFO: 一般的运行信息
- WARNING: 警告但不影响程序继续运行
- ERROR: 错误导致部分功能无法完成
- CRITICAL: 严重错误导致程序无法继续运行

### 日志内容
- 记录详细的上下文信息
- 包括操作、参数、错误原因等
- 避免记录敏感信息（密码、个人数据等）

## SQL安全

### 参数化查询
- 使用参数化查询而不是字符串拼接
- 避免SQL注入风险

### 最小权限原则
- 数据库连接使用最小必要权限
- 避免使用管理员权限执行常规操作

### 数据验证
- 在执行SQL前验证输入数据
- 实现适当的数据类型转换

## 代码安全

### 输入验证
- 验证所有用户输入
- 使用白名单而不是黑名单

### 敏感数据
- 不在代码中硬编码敏感信息
- 使用环境变量或配置文件存储

### 第三方库
- 谨慎选择第三方依赖
- 定期更新依赖库以修复安全漏洞 