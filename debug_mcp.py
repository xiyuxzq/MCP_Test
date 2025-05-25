#!/usr/bin/env python3
"""
调试MCP工具返回值问题
"""
from mcp.server.fastmcp import FastMCP

# 创建MCP实例
mcp = FastMCP()

@mcp.tool()
def test_simple_return() -> str:
    """测试简单字符串返回"""
    return "这是一个简单的字符串返回"

@mcp.tool()
def test_tuple_return() -> str:
    """测试元组返回（可能导致问题）"""
    # 模拟可能的问题场景
    result = (True, None, ["test"])
    # 这里应该只返回字符串
    return f"成功: {result[2]}"

@mcp.tool()
def test_complex_return() -> str:
    """测试复杂返回"""
    try:
        # 模拟WebService的返回
        success, error, data = (True, None, [{"test": "data"}])
        if success:
            return f"数据: {data}"
        else:
            return f"错误: {error}"
    except Exception as e:
        return f"异常: {str(e)}"

if __name__ == "__main__":
    print("调试脚本创建完成") 