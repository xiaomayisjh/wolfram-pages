#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha MCP 工具测试脚本
用于验证 MCP 工具是否正常工作
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加 open-source 目录到 Python 路径
current_dir = Path(__file__).parent
open_source_dir = current_dir / "open-source"
sys.path.insert(0, str(open_source_dir))

# 导入 MCP 服务器函数
from mcp_wolfram_server import (
    handle_wolfram_query,
    handle_wolfram_math,
    handle_wolfram_science,
    handle_wolfram_fact
)

async def test_wolfram_math():
    """测试数学计算工具"""
    print("🧮 测试数学计算工具...")
    print("=" * 50)
    
    # 测试二次方程求解
    test_cases = [
        {
            "expression": "solve x^2 + 5x + 1 = 0",
            "description": "二次方程求解"
        },
        {
            "expression": "2 + 2",
            "description": "基本算术"
        },
        {
            "expression": "integrate x^2 dx",
            "description": "积分计算"
        },
        {
            "expression": "plot sin(x) from 0 to 2pi",
            "description": "函数绘图",
            "include_plot": True
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {case['description']}")
        print(f"表达式: {case['expression']}")
        print("-" * 30)
        
        try:
            args = {"expression": case["expression"]}
            if "include_plot" in case:
                args["include_plot"] = case["include_plot"]
            
            result = await handle_wolfram_math(args)
            print("结果:")
            print(result[0].text[:500] + "..." if len(result[0].text) > 500 else result[0].text)
            
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        print()

async def test_wolfram_query():
    """测试通用查询工具"""
    print("\n🔍 测试通用查询工具...")
    print("=" * 50)
    
    test_cases = [
        {
            "query": "population of China",
            "description": "人口查询"
        },
        {
            "query": "H2O molecular structure",
            "description": "分子结构查询"
        },
        {
            "query": "speed of light",
            "description": "物理常数查询"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {case['description']}")
        print(f"查询: {case['query']}")
        print("-" * 30)
        
        try:
            result = await handle_wolfram_query({"query": case["query"]})
            print("结果:")
            print(result[0].text[:500] + "..." if len(result[0].text) > 500 else result[0].text)
            
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        print()

async def test_wolfram_science():
    """测试科学查询工具"""
    print("\n🔬 测试科学查询工具...")
    print("=" * 50)
    
    test_cases = [
        {
            "topic": "carbon properties",
            "description": "元素性质查询"
        },
        {
            "topic": "DNA structure",
            "description": "生物结构查询"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {case['description']}")
        print(f"主题: {case['topic']}")
        print("-" * 30)
        
        try:
            result = await handle_wolfram_science({"topic": case["topic"]})
            print("结果:")
            print(result[0].text[:500] + "..." if len(result[0].text) > 500 else result[0].text)
            
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        print()

async def test_wolfram_fact():
    """测试事实查询工具"""
    print("\n📚 测试事实查询工具...")
    print("=" * 50)
    
    test_cases = [
        {
            "question": "capital of Japan",
            "description": "地理事实查询"
        },
        {
            "question": "when was the first computer invented",
            "description": "历史事实查询"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {case['description']}")
        print(f"问题: {case['question']}")
        print("-" * 30)
        
        try:
            result = await handle_wolfram_fact({"question": case["question"]})
            print("结果:")
            print(result[0].text[:500] + "..." if len(result[0].text) > 500 else result[0].text)
            
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        print()

async def main():
    """主测试函数"""
    print("🚀 开始测试 Wolfram|Alpha MCP 工具...")
    print("=" * 60)
    
    # 检查环境
    print("🔍 检查环境...")
    try:
        from wolfram_mobile_api import WolframMobileAPI
        api = WolframMobileAPI()
        test_result = api.get_result_text("2+2")
        if "4" in test_result:
            print("✅ Wolfram API 连接正常")
        else:
            print("⚠️ Wolfram API 响应异常")
            return
    except Exception as e:
        print(f"❌ Wolfram API 连接失败: {e}")
        return
    
    # 运行各项测试
    await test_wolfram_math()
    await test_wolfram_query()
    await test_wolfram_science()
    await test_wolfram_fact()
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成！")
    print("\n💡 如果测试通过，说明 MCP 工具配置正确")
    print("💡 您可以在 MCP 客户端中使用以下工具:")
    print("   - wolfram_query: 通用查询")
    print("   - wolfram_math: 数学计算")
    print("   - wolfram_science: 科学查询")
    print("   - wolfram_fact: 事实查询")

if __name__ == "__main__":
    asyncio.run(main())
