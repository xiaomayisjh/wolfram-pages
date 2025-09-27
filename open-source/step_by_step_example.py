#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha Step-by-Step 查询示例
演示如何获取详细的解题步骤
"""

import requests
import json
from urllib.parse import quote

class WolframStepByStepClient:
    """专门用于step-by-step查询的客户端"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'WolframStepByStepClient/1.0'
        })
    
    def get_step_by_step_solution(self, equation):
        """
        获取step-by-step解题步骤
        
        Args:
            equation (str): 方程，如 "x^2+5x+1=0"
        
        Returns:
            dict: 包含详细步骤的结果
        """
        # 方法1: 使用数学查询端点，专门获取Solution pod
        try:
            result = self.session.get(f"{self.base_url}/math/{quote(equation)}")
            if result.status_code == 200:
                data = result.json()
                if data.get('success'):
                    return self._extract_solution_steps(data['data'])
        except Exception as e:
            print(f"数学查询失败: {e}")
        
        # 方法2: 使用POST查询，指定podstate参数
        try:
            query_data = {
                "input": f"step-by-step solve {equation}",
                "format": "plaintext",
                "output": "json",
                "podstate": "Solution__Step-by-step solution"
            }
            result = self.session.post(f"{self.base_url}/query", json=query_data)
            if result.status_code == 200:
                data = result.json()
                if data.get('success'):
                    return self._extract_solution_steps(data['data'])
        except Exception as e:
            print(f"POST查询失败: {e}")
        
        # 方法3: 使用所有pods，然后筛选Solution相关的内容
        try:
            result = self.session.get(f"{self.base_url}/pods/{quote(f'step-by-step solve {equation}')}")
            if result.status_code == 200:
                data = result.json()
                if data.get('success'):
                    return self._extract_solution_from_pods(data['pods'])
        except Exception as e:
            print(f"Pods查询失败: {e}")
        
        return {"error": "无法获取step-by-step解决方案"}
    
    def _extract_solution_steps(self, data):
        """从查询结果中提取解题步骤"""
        query_result = data.get('queryresult', {})
        if not query_result.get('success'):
            return {"error": f"查询失败: {query_result.get('error', '未知错误')}"}
        
        pods = query_result.get('pods', [])
        solution_info = {
            "input": query_result.get('inputstring', ''),
            "success": True,
            "steps": [],
            "result": "",
            "other_info": {}
        }
        
        for pod in pods:
            pod_id = pod.get('id', '')
            pod_title = pod.get('title', '')
            subpods = pod.get('subpods', [])
            
            # 查找Solution相关的pod
            if 'Solution' in pod_id or 'Step' in pod_title:
                for subpod in subpods:
                    plaintext = subpod.get('plaintext', '')
                    if plaintext:
                        solution_info['steps'].append({
                            'title': pod_title,
                            'content': plaintext
                        })
            
            # 查找Result pod
            elif pod_id == 'Result':
                for subpod in subpods:
                    plaintext = subpod.get('plaintext', '')
                    if plaintext:
                        solution_info['result'] = plaintext
            
            # 其他有用信息
            else:
                for subpod in subpods:
                    plaintext = subpod.get('plaintext', '')
                    if plaintext:
                        solution_info['other_info'][pod_title] = plaintext
        
        return solution_info
    
    def _extract_solution_from_pods(self, pods_data):
        """从pods数据中提取解决方案"""
        solution_info = {
            "success": True,
            "steps": [],
            "result": "",
            "other_info": {}
        }
        
        for pod_name, pod_results in pods_data.items():
            if 'Solution' in pod_name or 'Step' in pod_name:
                solution_info['steps'].extend([
                    {'title': pod_name, 'content': result} 
                    for result in pod_results
                ])
            elif 'Result' in pod_name:
                solution_info['result'] = '\n'.join(pod_results)
            else:
                solution_info['other_info'][pod_name] = pod_results
        
        return solution_info
    
    def print_solution(self, solution_info):
        """格式化打印解决方案"""
        if not solution_info.get('success'):
            print(f"❌ 错误: {solution_info.get('error', '未知错误')}")
            return
        
        print("🧮 Wolfram|Alpha Step-by-Step 解决方案")
        print("=" * 60)
        
        if solution_info.get('input'):
            print(f"📝 输入: {solution_info['input']}")
            print()
        
        if solution_info.get('steps'):
            print("📚 解题步骤:")
            print("-" * 40)
            for i, step in enumerate(solution_info['steps'], 1):
                print(f"{i}. {step['title']}")
                print(f"   {step['content']}")
                print()
        
        if solution_info.get('result'):
            print("✅ 最终结果:")
            print("-" * 40)
            print(solution_info['result'])
            print()
        
        if solution_info.get('other_info'):
            print("ℹ️  其他信息:")
            print("-" * 40)
            for title, content in solution_info['other_info'].items():
                print(f"{title}: {content}")
            print()

def demo_step_by_step():
    """演示step-by-step功能"""
    print("🚀 Wolfram|Alpha Step-by-Step 功能演示")
    print("=" * 60)
    
    client = WolframStepByStepClient()
    
    # 测试方程
    equations = [
        "x^2+5x+1=0",
        "x^2-4x+4=0", 
        "2x^2-7x+3=0",
        "x^3-6x^2+11x-6=0"
    ]
    
    for equation in equations:
        print(f"\n🔍 求解方程: {equation}")
        print("=" * 50)
        
        solution = client.get_step_by_step_solution(equation)
        client.print_solution(solution)
        
        print("\n" + "="*60)

def test_different_methods():
    """测试不同的查询方法"""
    print("🧪 测试不同的Step-by-Step查询方法")
    print("=" * 60)
    
    client = WolframStepByStepClient()
    equation = "x^2+5x+1=0"
    
    # 方法1: 数学查询端点
    print("方法1: 数学查询端点")
    print("-" * 30)
    try:
        result = requests.get(f"http://localhost:5000/math/{quote(equation)}")
        data = result.json()
        if data.get('success'):
            print("✅ 数学查询成功")
            # 查找Solution pod
            query_result = data['data'].get('queryresult', {})
            pods = query_result.get('pods', [])
            for pod in pods:
                if 'Solution' in pod.get('id', ''):
                    print(f"找到Solution pod: {pod.get('title', '')}")
                    for subpod in pod.get('subpods', []):
                        if subpod.get('plaintext'):
                            print(f"内容: {subpod['plaintext'][:100]}...")
        else:
            print(f"❌ 数学查询失败: {data.get('error')}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print()
    
    # 方法2: POST查询with podstate
    print("方法2: POST查询with podstate")
    print("-" * 30)
    try:
        query_data = {
            "input": f"step-by-step solve {equation}",
            "format": "plaintext",
            "output": "json",
            "podstate": "Solution__Step-by-step solution"
        }
        result = requests.post("http://localhost:5000/query", json=query_data)
        data = result.json()
        if data.get('success'):
            print("✅ POST查询成功")
            # 分析结果
            query_result = data['data'].get('queryresult', {})
            pods = query_result.get('pods', [])
            print(f"找到 {len(pods)} 个pods:")
            for pod in pods:
                print(f"  - {pod.get('id', '')}: {pod.get('title', '')}")
        else:
            print(f"❌ POST查询失败: {data.get('error')}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    print("Wolfram|Alpha Step-by-Step 查询示例")
    print("请确保API服务器正在运行 (python wolfram_api_server.py)")
    print("服务器地址: http://localhost:5000")
    print()
    
    try:
        # 演示step-by-step功能
        demo_step_by_step()
        
        # 测试不同方法
        test_different_methods()
        
    except KeyboardInterrupt:
        print("\n\n演示被用户中断")
    except Exception as e:
        print(f"\n演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
