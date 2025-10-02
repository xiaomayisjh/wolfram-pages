#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha Enhanced 启动脚本
一键启动增强版API服务器和客户端
"""

import os
import sys
import time
import webbrowser
import threading
import subprocess
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    Wolfram|Alpha Enhanced - 完整仿官方版本实现               ║
║                                                              ║
║    基于官方API文档，完整实现Pod输出和交互功能                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """检查依赖项"""
    print("检查依赖项...")
    
    required_packages = ['flask', 'flask_cors', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  [OK] {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  [MISSING] {package}")
    
    if missing_packages:
        print(f"\n[WARNING] 缺少依赖项: {', '.join(missing_packages)}")
        print("请运行以下命令安装：")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("[OK] 所有依赖项已安装")
    return True

def start_api_server():
    """启动API服务器"""
    print("\n启动API服务器...")
    
    # 检查API服务器文件是否存在
    api_file = Path("wolfram_enhanced_api.py")
    if not api_file.exists():
        print("[ERROR] 找不到API服务器文件: wolfram_enhanced_api.py")
        return None
    
    try:
        # 启动API服务器进程
        process = subprocess.Popen([
            sys.executable, "wolfram_enhanced_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='ignore')
        
        # 等待服务器启动
        time.sleep(3)
        
        # 检查进程是否还在运行
        if process.poll() is None:
            print("[OK] API服务器启动成功")
            print("服务地址: http://localhost:5000")
            return process
        else:
            stdout, stderr = process.communicate()
            print("[ERROR] API服务器启动失败")
            print(f"标准输出: {stdout}")
            print(f"错误信息: {stderr}")
            return None
            
    except Exception as e:
        print(f"[ERROR] 启动API服务器时出错: {e}")
        return None

def start_client():
    """启动客户端"""
    print("\n启动客户端...")
    
    # 检查客户端文件是否存在
    client_files = [
        "wolfram_client_enhanced.html",
        "wolfram_alpha_enhanced.html"
    ]
    
    client_file = None
    for file in client_files:
        if Path(file).exists():
            client_file = file
            break
    
    if not client_file:
        print("[ERROR] 找不到客户端文件")
        return False
    
    try:
        # 启动本地HTTP服务器
        print("启动本地HTTP服务器...")
        server_process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8080"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='ignore')
        
        # 等待服务器启动
        time.sleep(2)
        
        # 构建客户端URL
        client_url = f"http://localhost:8080/{client_file}"
        
        print("[OK] 客户端服务器启动成功")
        print(f"客户端地址: {client_url}")
        
        # 自动打开浏览器
        print("正在打开浏览器...")
        webbrowser.open(client_url)
        
        return server_process
        
    except Exception as e:
        print(f"[ERROR] 启动客户端时出错: {e}")
        return None

def show_usage_info():
    """显示使用信息"""
    print("\n" + "="*60)
    print("使用指南")
    print("="*60)
    print("1. API服务器: http://localhost:5000")
    print("   - API文档: http://localhost:5000/api/docs")
    print("   - 健康检查: http://localhost:5000/health")
    print("   - 测试界面: http://localhost:5000/")
    print()
    print("2. 客户端界面: http://localhost:8080/wolfram_client_enhanced.html")
    print("   - 支持完整的Wolfram|Alpha功能")
    print("   - Pod格式输出")
    print("   - 交互式计算")
    print()
    print("3. 示例查询:")
    print("   - solve x^2 + 3x + 2 = 0")
    print("   - derivative of sin(x)*cos(x)")
    print("   - plot x^2 from -5 to 5")
    print("   - molecular structure of caffeine")
    print("   - population of China")
    print()
    print("4. 快捷键:")
    print("   - Ctrl+K: 快速搜索")
    print("   - Ctrl+H: 查看历史")
    print("   - Enter: 执行查询")
    print("="*60)

def main():
    """主函数"""
    print_banner()
    
    # 检查依赖项
    if not check_dependencies():
        sys.exit(1)
    
    # 启动API服务器
    api_process = start_api_server()
    if not api_process:
        print("[ERROR] 无法启动API服务器，程序退出")
        sys.exit(1)
    
    # 启动客户端
    client_process = start_client()
    if not client_process:
        print("[ERROR] 无法启动客户端服务器")
        # 清理API服务器进程
        api_process.terminate()
        sys.exit(1)
    
    # 显示使用信息
    show_usage_info()
    
    print("\n[OK] Wolfram|Alpha Enhanced 启动完成！")
    print("提示: 按 Ctrl+C 停止所有服务")
    
    try:
        # 保持进程运行
        while True:
            time.sleep(1)
            
            # 检查进程是否还在运行
            if api_process.poll() is not None:
                print("\n[WARNING] API服务器已停止")
                break
            if client_process.poll() is not None:
                print("\n[WARNING] 客户端服务器已停止")
                break
                
    except KeyboardInterrupt:
        print("\n\n正在停止服务...")
        
        # 停止所有进程
        if api_process and api_process.poll() is None:
            api_process.terminate()
            print("[OK] API服务器已停止")
            
        if client_process and client_process.poll() is None:
            client_process.terminate()
            print("[OK] 客户端服务器已停止")
        
        print("感谢使用 Wolfram|Alpha Enhanced！")

if __name__ == "__main__":
    main()
