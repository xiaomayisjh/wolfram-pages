#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha MCP 工具演示脚本
展示如何在 MCP 客户端中正确调用 Wolfram Alpha 工具
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

async def demo_quintic_solution():
    """演示五次方程求解"""
    print("🔍 演示：求解五次方程 x^5 + 179x^2 + 198 = 0")
    print("=" * 60)
    
    # 正确的 MCP 工具调用方式
    print("📝 在 MCP 客户端中，您应该这样调用：")
    print("   wolfram_math(expression='solve x^5 + 179x^2 + 198 = 0')")
    print()
    
    # 执行实际的工具调用
    try:
        result = await handle_wolfram_math({
            "expression": "solve x^5 + 179x^2 + 198 = 0"
        })
        
        print("✅ 工具调用成功！结果如下：")
        print(result[0].text)
        
    except Exception as e:
        print(f"❌ 工具调用失败: {e}")

async def demo_other_examples():
    """演示其他数学问题"""
    print("\n🔍 演示：其他数学问题")
    print("=" * 60)
    
    examples = [
        {
            "expression": "solve x^2 + 5x + 1 = 0",
            "description": "二次方程求解"
        },
        {
            "expression": "integrate x^2 dx",
            "description": "积分计算"
        },
        {
            "expression": "plot sin(x) from 0 to 2pi",
            "description": "函数绘图"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   调用: wolfram_math(expression='{example['expression']}')")
        
        try:
            result = await handle_wolfram_math({
                "expression": example["expression"]
            })
            print("   结果:")
            # 只显示前200个字符
            result_text = result[0].text
            if len(result_text) > 200:
                print(f"   {result_text[:200]}...")
            else:
                print(f"   {result_text}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")

async def demo_general_queries():
    """演示通用查询"""
    print("\n🔍 演示：通用查询")
    print("=" * 60)
    
    examples = [
        {
            "query": "population of China",
            "description": "人口查询"
        },
        {
            "query": "H2O molecular structure",
            "description": "分子结构查询"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   调用: wolfram_query(query='{example['query']}')")
        
        try:
            result = await handle_wolfram_query({
                "query": example["query"]
            })
            print("   结果:")
            result_text = result[0].text
            if len(result_text) > 200:
                print(f"   {result_text[:200]}...")
            else:
                print(f"   {result_text}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")

def print_usage_guide():
    """打印使用指南"""
    print("\n📚 MCP 工具使用指南")
    print("=" * 60)
    print()
    print("在 MCP 客户端中，使用以下工具名称：")
    print()
    print("1. 数学计算工具：")
    print("   wolfram_math(expression='数学表达式')")
    print("   示例：wolfram_math(expression='solve x^2 + 5x + 1 = 0')")
    print()
    print("2. 通用查询工具：")
    print("   wolfram_query(query='查询文本')")
    print("   示例：wolfram_query(query='population of China')")
    print()
    print("3. 科学查询工具：")
    print("   wolfram_science(topic='科学主题')")
    print("   示例：wolfram_science(topic='H2O molecular structure')")
    print()
    print("4. 事实查询工具：")
    print("   wolfram_fact(question='事实性问题')")
    print("   示例：wolfram_fact(question='capital of Japan')")
    print()
    print("❌ 错误的调用方式：")
    print("   - wolfram_alpha.wolfram_math()  ❌")
    print("   - wolfram_alpha____wolfram_math____mcp()  ❌")
    print()
    print("✅ 正确的调用方式：")
    print("   - wolfram_math()  ✅")
    print("   - wolfram_query()  ✅")
    print("   - wolfram_science()  ✅")
    print("   - wolfram_fact()  ✅")

async def main():
    """主演示函数"""
    print("🚀 Wolfram|Alpha MCP 工具演示")
    print("=" * 60)
    print()
    print("这个演示展示了如何在 MCP 客户端中正确调用 Wolfram Alpha 工具")
    print("解决您之前遇到的 'name not defined' 错误问题")
    print()
    
    # 演示五次方程求解
    await demo_quintic_solution()
    
    # 演示其他数学问题
    await demo_other_examples()
    
    # 演示通用查询
    await demo_general_queries()
    
    # 打印使用指南
    print_usage_guide()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print()
    print("💡 关键要点：")
    print("   1. 使用正确的工具名称（wolfram_math, wolfram_query 等）")
    print("   2. 参数以字典形式传递")
    print("   3. 确保 MCP 服务器正在运行")
    print("   4. 检查网络连接和 Wolfram API 状态")

if __name__ == "__main__":
    asyncio.run(main())
