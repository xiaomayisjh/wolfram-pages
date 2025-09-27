#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha Mobile API 简化封装
基于poc.py的成功实现，提供更友好的接口
"""

import requests
from hashlib import md5
from urllib.parse import urlsplit, urlencode, unquote_plus
import json

class WolframMobileAPI:
    """Wolfram|Alpha Mobile API 客户端"""
    
    def __init__(self):
        self.headers = {"User-Agent": "Wolfram Android App"}
        self.appid = "3H4296-5YPAGQUJK7"  # Mobile app AppId
        self.server = "api.wolframalpha.com"
        self.sig_salt = "vFdeaRwBTVqdc5CL"  # Mobile app salt
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _calc_sig(self, query):
        """计算签名"""
        params = list(filter(lambda x: len(x) > 1, 
                    list(map(lambda x: x.split("="), query.split("&")))))
        params.sort(key=lambda x: x[0])
        
        s = self.sig_salt
        for key, val in params:
            s += key + val
        s = s.encode("utf-8")
        return md5(s).hexdigest().upper()
    
    def _craft_signed_url(self, url):
        """构建签名URL"""
        (scheme, netloc, path, query, _) = urlsplit(url)
        _query = {"appid": self.appid}
        
        _query.update(dict(list(filter(lambda x: len(x) > 1, 
            list(map(lambda x: list(map(lambda y: unquote_plus(y), x.split("="))), 
                   query.split("&")))))))
        query = urlencode(_query)
        _query.update({"sig": self._calc_sig(query)})
        return f"{scheme}://{netloc}{path}?{urlencode(_query)}"
    
    def query(self, input_text, format_type="plaintext", output_type="json", **kwargs):
        """
        执行Wolfram|Alpha查询
        
        Args:
            input_text (str): 查询文本
            format_type (str): 格式类型 (plaintext, xml等)
            output_type (str): 输出类型 (json, xml等)
            **kwargs: 其他API参数
        
        Returns:
            str: 查询结果
        """
        params = {
            "input": input_text,
            "format": format_type,
            "output": output_type
        }
        params.update(kwargs)
        
        query_string = urlencode(params)
        url = f"https://{self.server}/v2/query.jsp?{query_string}"
        
        try:
            response = self.session.get(self._craft_signed_url(url))
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {e}")
    
    def query_json(self, input_text, **kwargs):
        """查询并返回JSON格式结果"""
        result = self.query(input_text, format_type="plaintext", output_type="json", **kwargs)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            raise Exception("无法解析JSON结果")
    
    def query_plaintext(self, input_text, **kwargs):
        """查询并返回纯文本格式结果"""
        return self.query(input_text, format_type="plaintext", output_type="plaintext", **kwargs)
    
    def query_xml(self, input_text, **kwargs):
        """查询并返回XML格式结果"""
        return self.query(input_text, format_type="xml", output_type="xml", **kwargs)
    
    def get_result_text(self, input_text, pod_id="Result"):
        """
        获取指定pod的纯文本结果
        
        Args:
            input_text (str): 查询文本
            pod_id (str): Pod ID (如 "Result", "Input" 等)
        
        Returns:
            str: Pod的纯文本内容
        """
        try:
            result = self.query_json(input_text, includepodid=pod_id)
            query_result = result.get('queryresult', {})
            
            if not query_result.get('success', False):
                return f"查询失败: {query_result.get('error', '未知错误')}"
            
            pods = query_result.get('pods', [])
            if not pods:
                return "未找到结果"
            
            pod = pods[0]
            subpods = pod.get('subpods', [])
            if not subpods:
                return "Pod中没有子内容"
            
            return subpods[0].get('plaintext', '无文本内容')
            
        except Exception as e:
            return f"获取结果失败: {e}"
    
    def get_all_results(self, input_text):
        """
        获取所有pod的结果文本
        
        Args:
            input_text (str): 查询文本
        
        Returns:
            dict: 所有pod的结果
        """
        try:
            result = self.query_json(input_text)
            query_result = result.get('queryresult', {})
            
            if not query_result.get('success', False):
                return {"error": f"查询失败: {query_result.get('error', '未知错误')}"}
            
            pods = query_result.get('pods', [])
            results = {}
            
            for pod in pods:
                pod_title = pod.get('title', 'Unknown')
                pod_id = pod.get('id', 'Unknown')
                subpods = pod.get('subpods', [])
                
                pod_results = []
                for subpod in subpods:
                    plaintext = subpod.get('plaintext', '')
                    if plaintext:
                        pod_results.append(plaintext)
                
                if pod_results:
                    results[f"{pod_title} ({pod_id})"] = pod_results
            
            return results
            
        except Exception as e:
            return {"error": f"获取结果失败: {e}"}

# 便捷函数
def quick_query(input_text, format_type="plaintext", output_type="json"):
    """快速查询函数"""
    api = WolframMobileAPI()
    return api.query(input_text, format_type, output_type)

def quick_result(input_text):
    """快速获取结果文本"""
    api = WolframMobileAPI()
    return api.get_result_text(input_text)

# 示例使用
if __name__ == "__main__":
    print("Wolfram|Alpha Mobile API 简化封装测试")
    print("=" * 50)
    
    # 创建API实例
    api = WolframMobileAPI()
    
    # 测试查询
    test_queries = [
        "2+2",
        "population of France", 
        "H2O",
        "speed of light"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        print("-" * 30)
        try:
            result = api.get_result_text(query)
            print(f"结果: {result}")
        except Exception as e:
            print(f"错误: {e}")
    
    # 测试获取所有结果
    print(f"\n{'='*50}")
    print("测试获取所有结果 (H2O):")
    print("-" * 30)
    try:
        all_results = api.get_all_results("H2O")
        if "error" in all_results:
            print(f"错误: {all_results['error']}")
        else:
            for pod_name, pod_results in all_results.items():
                print(f"\n{pod_name}:")
                for result in pod_results:
                    print(f"  - {result[:100]}..." if len(result) > 100 else f"  - {result}")
    except Exception as e:
        print(f"错误: {e}")
    
    print(f"\n{'='*50}")
    print("测试完成！")
