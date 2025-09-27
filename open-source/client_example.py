#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha API 客户端示例
演示如何调用Wolfram|Alpha API网络服务
"""

import requests
import json
import time
from urllib.parse import quote

class WolframAPIClient:
    """Wolfram|Alpha API 客户端"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'WolframAPIClient/1.0'
        })
    
    def _make_request(self, method, endpoint, **kwargs):
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def query(self, input_text, format_type="plaintext", output_type="json", **kwargs):
        """
        执行查询
        
        Args:
            input_text (str): 查询文本
            format_type (str): 格式类型
            output_type (str): 输出类型
            **kwargs: 其他参数
        
        Returns:
            dict: 查询结果
        """
        data = {
            "input": input_text,
            "format": format_type,
            "output": output_type
        }
        data.update(kwargs)
        
        return self._make_request('POST', '/query', json=data)
    
    def quick_query(self, query_text):
        """快速查询"""
        return self._make_request('GET', f'/query/{quote(query_text)}')
    
    def get_result(self, query_text):
        """获取主要结果文本"""
        return self._make_request('GET', f'/result/{quote(query_text)}')
    
    def get_pods(self, query_text):
        """获取所有pods"""
        return self._make_request('GET', f'/pods/{quote(query_text)}')
    
    def math_query(self, query_text):
        """数学查询"""
        return self._make_request('GET', f'/math/{quote(query_text)}')
    
    def science_query(self, query_text):
        """科学查询"""
        return self._make_request('GET', f'/science/{quote(query_text)}')
    
    def health_check(self):
        """健康检查"""
        return self._make_request('GET', '/health')
    
    def get_api_info(self):
        """获取API信息"""
        return self._make_request('GET', '/')

def print_result(title, result):
    """格式化打印结果"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    
    if result.get('success'):
        if 'data' in result:
            print(json.dumps(result['data'], indent=2, ensure_ascii=False))
        elif 'result' in result:
            print(result['result'])
        elif 'pods' in result:
            for pod_name, pod_results in result['pods'].items():
                print(f"\n{pod_name}:")
                for pod_result in pod_results:
                    print(f"  - {pod_result}")
    else:
        print(f"错误: {result.get('error', '未知错误')}")

def demo_basic_queries():
    """演示基本查询"""
    print("🚀 Wolfram|Alpha API 客户端演示")
    print("=" * 60)
    
    # 创建客户端
    client = WolframAPIClient()
    
    # 健康检查
    print("\n1. 健康检查")
    health = client.health_check()
    print(f"服务状态: {'正常' if health.get('status') == 'healthy' else '异常'}")
    
    # 基本查询示例
    queries = [
        ("数学计算", "2+2"),
        ("人口查询", "population of France"),
        ("化学查询", "H2O"),
        ("物理常数", "speed of light"),
        ("天气查询", "weather in Beijing")
    ]
    
    print(f"\n2. 基本查询测试")
    for title, query in queries:
        print(f"\n查询: {query}")
        result = client.quick_query(query)
        if result.get('success'):
            # 提取主要结果
            data = result.get('data', {})
            query_result = data.get('queryresult', {})
            if query_result.get('success'):
                pods = query_result.get('pods', [])
                if pods:
                    first_pod = pods[0]
                    subpods = first_pod.get('subpods', [])
                    if subpods:
                        print(f"结果: {subpods[0].get('plaintext', '无文本结果')}")
                    else:
                        print("结果: 无子内容")
                else:
                    print("结果: 无pods")
            else:
                print(f"查询失败: {query_result.get('error', '未知错误')}")
        else:
            print(f"请求失败: {result.get('error', '未知错误')}")

def demo_advanced_queries():
    """演示高级查询"""
    print(f"\n{'='*60}")
    print(" 高级查询演示")
    print(f"{'='*60}")
    
    client = WolframAPIClient()
    
    # 数学查询
    print("\n1. 数学查询 (微分方程)")
    math_result = client.math_query("y' = y/(x+y^3)")
    print_result("数学查询结果", math_result)
    
    # 科学查询
    print("\n2. 科学查询 (原子质量)")
    science_result = client.science_query("atomic mass of carbon")
    print_result("科学查询结果", science_result)
    
    # 获取所有pods
    print("\n3. 获取所有pods (H2O)")
    pods_result = client.get_pods("H2O")
    print_result("所有pods结果", pods_result)

def demo_post_requests():
    """演示POST请求"""
    print(f"\n{'='*60}")
    print(" POST请求演示")
    print(f"{'='*60}")
    
    client = WolframAPIClient()
    
    # 自定义格式查询
    print("\n1. 自定义格式查询")
    custom_result = client.query(
        "population of China",
        format_type="plaintext",
        output_type="json",
        includepodid="Result"
    )
    print_result("自定义格式查询", custom_result)
    
    # 数学查询with步骤
    print("\n2. 数学查询with步骤")
    math_with_steps = client.query(
        "integrate x^2",
        format_type="plaintext",
        output_type="json",
        podstate="Solution__Step-by-step solution"
    )
    print_result("数学查询with步骤", math_with_steps)

def demo_error_handling():
    """演示错误处理"""
    print(f"\n{'='*60}")
    print(" 错误处理演示")
    print(f"{'='*60}")
    
    client = WolframAPIClient()
    
    # 无效查询
    print("\n1. 无效查询")
    invalid_result = client.quick_query("invalid_query_12345")
    print_result("无效查询结果", invalid_result)
    
    # 空查询
    print("\n2. 空查询")
    empty_result = client.quick_query("")
    print_result("空查询结果", empty_result)

def demo_performance():
    """演示性能测试"""
    print(f"\n{'='*60}")
    print(" 性能测试")
    print(f"{'='*60}")
    
    client = WolframAPIClient()
    
    queries = ["2+2", "3*3", "sqrt(16)", "log(10)", "sin(pi/2)"]
    
    print(f"\n测试 {len(queries)} 个查询的响应时间...")
    
    total_time = 0
    success_count = 0
    
    for i, query in enumerate(queries, 1):
        start_time = time.time()
        result = client.quick_query(query)
        end_time = time.time()
        
        response_time = end_time - start_time
        total_time += response_time
        
        if result.get('success'):
            success_count += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"{i:2d}. {query:12s} {status} {response_time:.2f}s")
    
    avg_time = total_time / len(queries)
    success_rate = success_count / len(queries) * 100
    
    print(f"\n统计结果:")
    print(f"  总查询数: {len(queries)}")
    print(f"  成功数: {success_count}")
    print(f"  成功率: {success_rate:.1f}%")
    print(f"  总时间: {total_time:.2f}s")
    print(f"  平均时间: {avg_time:.2f}s")

def main():
    """主函数"""
    print("Wolfram|Alpha API 客户端示例")
    print("请确保API服务器正在运行 (python wolfram_api_server.py)")
    print("服务器地址: http://localhost:5000")
    
    try:
        # 基本查询演示
        demo_basic_queries()
        
        # 高级查询演示
        demo_advanced_queries()
        
        # POST请求演示
        demo_post_requests()
        
        # 错误处理演示
        demo_error_handling()
        
        # 性能测试
        demo_performance()
        
        print(f"\n{'='*60}")
        print(" 演示完成！")
        print(f"{'='*60}")
        
    except KeyboardInterrupt:
        print("\n\n演示被用户中断")
    except Exception as e:
        print(f"\n演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
