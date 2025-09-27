#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试五次方程求解
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
from mcp_wolfram_server import handle_wolfram_math

async def test_quintic_equation():
    """测试五次方程求解"""
    print("🧮 测试五次方程求解: x^5 + 179x^2 + 198 = 0")
    print("=" * 60)
    
    try:
        # 使用数学计算工具
        result = await handle_wolfram_math({
            "expression": "solve x^5 + 179x^2 + 198 = 0",
            "include_plot": False
        })
        
        print("MCP 工具结果:")
        print(result[0].text)
        
    except Exception as e:
        print(f"❌ MCP 工具调用失败: {e}")
        import traceback
        traceback.print_exc()

async def test_direct_api():
    """直接测试 Wolfram API"""
    print("\n🔍 直接测试 Wolfram API:")
    print("-" * 30)
    
    try:
        from wolfram_mobile_api import WolframMobileAPI
        api = WolframMobileAPI()
        
        result = api.get_all_results("solve x^5 + 179x^2 + 198 = 0")
        
        print("直接 API 结果:")
        for pod_name, pod_results in result.items():
            print(f"\n{pod_name}:")
            for result_text in pod_results:
                print(f"  {result_text}")
                
    except Exception as e:
        print(f"❌ 直接 API 调用失败: {e}")

async def main():
    """主函数"""
    print("🚀 开始测试五次方程求解...")
    
    # 测试直接 API
    await test_direct_api()
    
    # 测试 MCP 工具
    await test_quintic_equation()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")

if __name__ == "__main__":
    asyncio.run(main())
