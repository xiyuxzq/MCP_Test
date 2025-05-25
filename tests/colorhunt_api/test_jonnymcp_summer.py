#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试JonnyMCP的夏天配色方案抓取功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from custom_mcp import scrape_colorhunt_by_tag

def main():
    """测试JonnyMCP获取夏天配色方案"""
    print("🌞 使用JonnyMCP工具获取ColorHunt夏天配色方案")
    print("=" * 60)
    
    # 使用JonnyMCP工具获取夏天配色方案
    result = scrape_colorhunt_by_tag('summer', 5)
    print(result)

if __name__ == "__main__":
    main() 