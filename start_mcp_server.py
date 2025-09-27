#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha MCP 服务器启动脚本
提供便捷的启动和测试功能
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# 添加 open-source 目录到 Python 路径
current_dir = Path(__file__).parent
open_source_dir = current_dir / "open-source"
sys.path.insert(0, str(open_source_dir))

# 导入 MCP 服务器
from mcp_wolfram_server import main

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import mcp
        import requests
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements-mcp.txt")
        return False

def check_wolfram_api():
    """检查 Wolfram API 文件是否存在"""
    api_file = open_source_dir / "wolfram_mobile_api.py"
    if api_file.exists():
        print("✅ Wolfram API 文件存在")
        return True
    else:
        print(f"❌ Wolfram API 文件不存在: {api_file}")
        return False

def test_connection():
    """测试 Wolfram API 连接"""
    try:
        from wolfram_mobile_api import WolframMobileAPI
        api = WolframMobileAPI()
        result = api.get_result_text("2+2")
        if "4" in result:
            print("✅ Wolfram API 连接正常")
            return True
        else:
            print(f"⚠️ Wolfram API 响应异常: {result}")
            return False
    except Exception as e:
        print(f"❌ Wolfram API 连接失败: {e}")
        return False

def print_usage():
    """打印使用说明"""
    print("\n" + "="*60)
    print("Wolfram|Alpha MCP 服务器")
    print("="*60)
    print("\n使用方法:")
    print("  python start_mcp_server.py          # 启动 MCP 服务器")
    print("  python start_mcp_server.py --test   # 运行测试")
    print("  python start_mcp_server.py --check  # 检查环境")
    print("\n配置 MCP 客户端:")
    print("  将以下配置添加到您的 MCP 客户端配置文件中:")
    print(f'  "wolfram-alpha": {{')
    print(f'    "command": "python",')
    print(f'    "args": ["{os.path.basename(__file__).replace("start_", "")}"],')
    print(f'    "cwd": "{current_dir}",')
    print(f'    "env": {{"PYTHONPATH": "./open-source"}}')
    print(f'  }}')
    print("\n可用工具:")
    print("  - wolfram_query: 通用查询")
    print("  - wolfram_math: 数学计算")
    print("  - wolfram_science: 科学查询")
    print("  - wolfram_fact: 事实查询")
    print("="*60)

async def run_tests():
    """运行测试"""
    print("\n🧪 运行 MCP 服务器测试...")
    
    try:
        from mcp_wolfram_server import server, handle_wolfram_query, handle_wolfram_math
        
        # 测试数学查询
        print("\n测试数学查询...")
        math_result = await handle_wolfram_math({"expression": "2+2"})
        print(f"结果: {math_result[0].text[:100]}...")
        
        # 测试通用查询
        print("\n测试通用查询...")
        query_result = await handle_wolfram_query({"query": "population of China"})
        print(f"结果: {query_result[0].text[:100]}...")
        
        print("\n✅ 所有测试通过!")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def main_cli():
    """命令行主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # 运行测试
            print("🔍 检查环境...")
            if not check_dependencies() or not check_wolfram_api():
                sys.exit(1)
            
            if not test_connection():
                print("⚠️ 警告: Wolfram API 连接可能有问题")
            
            asyncio.run(run_tests())
            return
            
        elif sys.argv[1] == "--check":
            # 检查环境
            print("🔍 检查环境...")
            deps_ok = check_dependencies()
            api_ok = check_wolfram_api()
            conn_ok = test_connection() if deps_ok and api_ok else False
            
            if deps_ok and api_ok and conn_ok:
                print("\n✅ 环境检查通过，可以启动 MCP 服务器")
            else:
                print("\n❌ 环境检查失败，请修复问题后重试")
                sys.exit(1)
            return
            
        elif sys.argv[1] in ["--help", "-h"]:
            print_usage()
            return
    
    # 默认启动服务器
    print("🚀 启动 Wolfram|Alpha MCP 服务器...")
    
    # 检查环境
    if not check_dependencies() or not check_wolfram_api():
        print("\n❌ 环境检查失败，请先运行: python start_mcp_server.py --check")
        sys.exit(1)
    
    if not test_connection():
        print("⚠️ 警告: Wolfram API 连接可能有问题，但服务器仍会启动")
    
    print("✅ 环境检查通过，启动服务器...")
    print("📡 MCP 服务器正在运行，等待客户端连接...")
    print("💡 按 Ctrl+C 停止服务器")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        try:
            print("\n👋 服务器已停止")
        except:
            pass  # 忽略I/O错误
    except Exception as e:
        try:
            print(f"\n❌ 服务器启动失败: {e}")
            import traceback
            traceback.print_exc()
        except:
            pass  # 忽略I/O错误
        sys.exit(1)

if __name__ == "__main__":
    main_cli()
