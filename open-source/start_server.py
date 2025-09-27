#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha API 服务器启动脚本
提供便捷的服务器启动和配置选项
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖包"""
    required_packages = ['flask', 'flask_cors', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def start_server(host='0.0.0.0', port=5000, debug=True):
    """启动服务器"""
    print("🚀 启动 Wolfram|Alpha API 服务器...")
    print(f"   地址: http://{host}:{port}")
    print(f"   调试模式: {'开启' if debug else '关闭'}")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    try:
        # 导入并启动服务器
        from wolfram_api_server import app
        app.run(debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Wolfram|Alpha API 服务器')
    parser.add_argument('--host', default='0.0.0.0', help='服务器地址 (默认: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='服务器端口 (默认: 5000)')
    parser.add_argument('--no-debug', action='store_true', help='关闭调试模式')
    parser.add_argument('--check-deps', action='store_true', help='只检查依赖包')
    
    args = parser.parse_args()
    
    print("Wolfram|Alpha API 服务器启动器")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    if args.check_deps:
        print("✅ 依赖检查完成")
        return
    
    # 启动服务器
    success = start_server(
        host=args.host,
        port=args.port,
        debug=not args.no_debug
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
