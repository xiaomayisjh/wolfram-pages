#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha Enhanced API Server
基于官方API文档实现的完整功能服务器
支持Full Results API的所有功能
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
from hashlib import md5
from urllib.parse import urlsplit, urlencode, unquote_plus, quote_plus
import json
import xml.etree.ElementTree as ET
import traceback
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # 允许跨域请求

class WolframAlphaAPI:
    """Wolfram|Alpha API 完整封装"""
    
    def __init__(self):
        self.headers = {"User-Agent": "Wolfram Android App"}
        self.appid = "3H4296-5YPAGQUJK7"  # Mobile app AppId
        self.server = "api.wolframalpha.com"
        self.sig_salt = "vFdeaRwBTVqdc5CL"  # Mobile app salt
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _calc_sig(self, query):
        """计算签名 - 基于官方文档的签名算法"""
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
    
    def query(self, input_text, **kwargs):
        """
        执行Wolfram|Alpha查询 - 支持官方API的所有参数
        
        Args:
            input_text (str): 查询文本
            **kwargs: API参数，支持：
                - format: 输出格式 (plaintext, image, html, mathml, sound, wav)
                - output: 输出类型 (xml, json)
                - includepodid: 包含特定pod ID
                - excludepodid: 排除特定pod ID
                - podtitle: 包含特定pod标题
                - podindex: 包含特定pod索引
                - scanner: 指定扫描器
                - async: 异步查询
                - podtimeout: pod超时时间
                - scantimeout: 扫描超时时间
                - podstate: pod状态
                - assumption: 假设
                - reinterpret: 重新解释
                - translation: 翻译
                - ignorecase: 忽略大小写
                - sig: 签名（自动计算）
                - ip: IP地址
                - latlong: 经纬度
                - location: 位置
                - countrycode: 国家代码
                - units: 单位系统
                - width: 图像宽度
                - maxwidth: 最大图像宽度
                - plotwidth: 图表宽度
                - mag: 放大倍数
                - fontsize: 字体大小
        
        Returns:
            dict: 查询结果
        """
        # 默认参数 - 确保获取Pod数据
        params = {
            "input": input_text,
            "format": kwargs.get('format', 'plaintext,image'),
            "output": kwargs.get('output', 'json'),
            "podtimeout": kwargs.get('podtimeout', 10),  # 增加Pod超时时间
            "scantimeout": kwargs.get('scantimeout', 5),  # 增加扫描超时时间
            "reinterpret": kwargs.get('reinterpret', 'true'),  # 启用重新解释
        }
        
        # 添加其他参数
        for key, value in kwargs.items():
            if key not in ['format', 'output', 'podtimeout', 'scantimeout', 'reinterpret'] and value is not None:
                params[key] = value
        
        query_string = urlencode(params)
        url = f"https://{self.server}/v2/query.jsp?{query_string}"
        
        try:
            response = self.session.get(self._craft_signed_url(url))
            response.raise_for_status()
            
            if params['output'] == 'json':
                result = response.json()
                
                # 如果没有Pod数据，尝试不同的参数组合
                if result.get('numpods', 0) == 0:
                    print(f"首次查询无Pod数据，尝试调整参数...")
                    
                    # 尝试不同的参数组合
                    retry_params = params.copy()
                    retry_params.update({
                        'podtimeout': 15,
                        'scantimeout': 10,
                        'format': 'plaintext',
                        'reinterpret': 'true',
                        'translation': 'true'
                    })
                    
                    retry_query_string = urlencode(retry_params)
                    retry_url = f"https://{self.server}/v2/query.jsp?{retry_query_string}"
                    
                    retry_response = self.session.get(self._craft_signed_url(retry_url))
                    retry_response.raise_for_status()
                    retry_result = retry_response.json()
                    
                    if retry_result.get('numpods', 0) > 0:
                        print(f"重试成功，获得 {retry_result.get('numpods')} 个Pod")
                        return retry_result
                    else:
                        print(f"重试仍无Pod数据，返回原始结果")
                        return result
                
                return result
            else:
                return response.text
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析失败: {e}")
    
    def validate_query(self, input_text):
        """
        验证查询 - 使用validatequery功能
        快速检查输入是否可以被Wolfram|Alpha理解
        """
        params = {
            "input": input_text,
            "output": "json"
        }
        
        query_string = urlencode(params)
        url = f"https://{self.server}/v2/validatequery.jsp?{query_string}"
        
        try:
            response = self.session.get(self._craft_signed_url(url))
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"查询验证失败: {e}")
    
    def get_simple_result(self, input_text):
        """获取简单结果 - 仅返回主要结果"""
        result = self.query(input_text, includepodid="Result")
        
        query_result = result.get('queryresult', {})
        if not query_result.get('success', False):
            return None
        
        pods = query_result.get('pods', [])
        if not pods:
            return None
        
        result_pod = pods[0]
        subpods = result_pod.get('subpods', [])
        if not subpods:
            return None
        
        return subpods[0].get('plaintext', '')
    
    def get_step_by_step(self, input_text):
        """获取逐步解决方案"""
        return self.query(
            input_text, 
            podstate="Solution__Step-by-step solution",
            includepodid="Solution"
        )
    
    def get_plot(self, input_text, width=400, height=300):
        """获取图表"""
        return self.query(
            input_text,
            includepodid="Plot",
            width=width,
            plotwidth=width
        )
    
    def get_related_queries(self, input_text):
        """获取相关查询建议"""
        # 这个功能需要特殊的API端点，这里提供模拟实现
        common_prefixes = [
            "solve", "derivative of", "integral of", "graph", 
            "factor", "simplify", "expand", "limit of"
        ]
        
        suggestions = []
        for prefix in common_prefixes:
            if not input_text.lower().startswith(prefix):
                suggestions.append(f"{prefix} {input_text}")
        
        return suggestions[:5]

# 创建API实例
wolfram_api = WolframAlphaAPI()

@app.route('/')
def home():
    """首页 - API文档和测试界面"""
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Wolfram|Alpha Enhanced API Server</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body class="bg-gray-50 min-h-screen">
        <div class="max-w-6xl mx-auto px-4 py-8">
            <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
                <h1 class="text-3xl font-bold text-orange-600 mb-4">
                    <i class="fas fa-calculator mr-3"></i>
                    Wolfram|Alpha Enhanced API Server
                </h1>
                <p class="text-gray-600 text-lg mb-6">
                    基于官方Wolfram|Alpha API文档实现的完整功能服务器，支持所有官方API参数和功能。
                </p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-blue-50 p-6 rounded-lg">
                        <h3 class="text-xl font-semibold text-blue-800 mb-3">
                            <i class="fas fa-rocket mr-2"></i>主要功能
                        </h3>
                        <ul class="space-y-2 text-blue-700">
                            <li><i class="fas fa-check mr-2"></i>完整的Full Results API支持</li>
                            <li><i class="fas fa-check mr-2"></i>所有官方API参数支持</li>
                            <li><i class="fas fa-check mr-2"></i>查询验证功能</li>
                            <li><i class="fas fa-check mr-2"></i>Step-by-step解决方案</li>
                            <li><i class="fas fa-check mr-2"></i>图表和可视化</li>
                            <li><i class="fas fa-check mr-2"></i>Assumptions处理</li>
                        </ul>
                    </div>
                    
                    <div class="bg-green-50 p-6 rounded-lg">
                        <h3 class="text-xl font-semibold text-green-800 mb-3">
                            <i class="fas fa-code mr-2"></i>API端点
                        </h3>
                        <ul class="space-y-2 text-green-700 text-sm">
                            <li><code class="bg-green-100 px-2 py-1 rounded">POST /api/query</code> - 完整查询</li>
                            <li><code class="bg-green-100 px-2 py-1 rounded">GET /api/simple/{query}</code> - 简单结果</li>
                            <li><code class="bg-green-100 px-2 py-1 rounded">POST /api/validate</code> - 查询验证</li>
                            <li><code class="bg-green-100 px-2 py-1 rounded">POST /api/stepbystep</code> - 逐步解决</li>
                            <li><code class="bg-green-100 px-2 py-1 rounded">POST /api/plot</code> - 图表生成</li>
                            <li><code class="bg-green-100 px-2 py-1 rounded">GET /api/suggestions/{query}</code> - 查询建议</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-lg p-8">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">
                    <i class="fas fa-flask mr-3"></i>API测试
                </h2>
                
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">查询输入</label>
                    <input type="text" id="testQuery" placeholder="例如: solve x^2 + 3x + 2 = 0" 
                           class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-orange-500">
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">API端点</label>
                        <select id="testEndpoint" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500">
                            <option value="query">完整查询</option>
                            <option value="simple">简单结果</option>
                            <option value="validate">查询验证</option>
                            <option value="stepbystep">逐步解决</option>
                            <option value="suggestions">查询建议</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">输出格式</label>
                        <select id="testFormat" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500">
                            <option value="json">JSON</option>
                            <option value="xml">XML</option>
                        </select>
                    </div>
                    
                    <div class="flex items-end">
                        <button onclick="testAPI()" class="w-full bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-colors">
                            <i class="fas fa-play mr-2"></i>测试API
                        </button>
                    </div>
                </div>
                
                <div id="testResult" class="hidden">
                    <h3 class="text-lg font-semibold text-gray-800 mb-3">测试结果</h3>
                    <pre id="testOutput" class="bg-gray-100 p-4 rounded-md overflow-auto text-sm"></pre>
                </div>
            </div>
        </div>
        
        <script>
            async function testAPI() {
                const query = document.getElementById('testQuery').value;
                const endpoint = document.getElementById('testEndpoint').value;
                const format = document.getElementById('testFormat').value;
                
                if (!query.trim()) {
                    alert('请输入查询内容');
                    return;
                }
                
                const resultDiv = document.getElementById('testResult');
                const outputPre = document.getElementById('testOutput');
                
                resultDiv.classList.remove('hidden');
                outputPre.textContent = '正在查询...';
                
                try {
                    let url, options;
                    
                    switch(endpoint) {
                        case 'query':
                            url = '/api/query';
                            options = {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ input: query, output: format })
                            };
                            break;
                        case 'simple':
                            url = `/api/simple/${encodeURIComponent(query)}`;
                            options = { method: 'GET' };
                            break;
                        case 'validate':
                            url = '/api/validate';
                            options = {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ input: query })
                            };
                            break;
                        case 'stepbystep':
                            url = '/api/stepbystep';
                            options = {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ input: query })
                            };
                            break;
                        case 'suggestions':
                            url = `/api/suggestions/${encodeURIComponent(query)}`;
                            options = { method: 'GET' };
                            break;
                    }
                    
                    const response = await fetch(url, options);
                    const result = await response.json();
                    
                    outputPre.textContent = JSON.stringify(result, null, 2);
                } catch (error) {
                    outputPre.textContent = `错误: ${error.message}`;
                }
            }
            
            // 回车键触发测试
            document.getElementById('testQuery').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    testAPI();
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "service": "Wolfram|Alpha Enhanced API Server",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "Full Results API",
            "Query Validation", 
            "Step-by-Step Solutions",
            "Plot Generation",
            "Assumptions Handling",
            "Related Queries"
        ]
    })

@app.route('/api/query', methods=['POST'])
def api_query():
    """完整查询API - 支持所有官方参数"""
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必需参数 'input'"
            }), 400
        
        input_text = data['input']
        
        # 提取API参数
        api_params = {}
        supported_params = [
            'format', 'output', 'includepodid', 'excludepodid', 'podtitle', 
            'podindex', 'scanner', 'async', 'podtimeout', 'scantimeout', 
            'podstate', 'assumption', 'reinterpret', 'translation', 
            'ignorecase', 'ip', 'latlong', 'location', 'countrycode', 
            'units', 'width', 'maxwidth', 'plotwidth', 'mag', 'fontsize'
        ]
        
        for param in supported_params:
            if param in data:
                api_params[param] = data[param]
        
        # 执行查询
        result = wolfram_api.query(input_text, **api_params)
        
        return jsonify({
            "success": True,
            "data": result,
            "query": input_text,
            "params": api_params,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/simple/<path:query_text>')
def api_simple(query_text):
    """简单结果API - 仅返回主要结果"""
    try:
        result = wolfram_api.get_simple_result(query_text)
        return jsonify({
            "success": True,
            "query": query_text,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "query": query_text
        }), 500

@app.route('/api/validate', methods=['POST'])
def api_validate():
    """查询验证API"""
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必需参数 'input'"
            }), 400
        
        input_text = data['input']
        result = wolfram_api.validate_query(input_text)
        
        return jsonify({
            "success": True,
            "data": result,
            "query": input_text,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/stepbystep', methods=['POST'])
def api_step_by_step():
    """逐步解决方案API"""
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必需参数 'input'"
            }), 400
        
        input_text = data['input']
        result = wolfram_api.get_step_by_step(input_text)
        
        return jsonify({
            "success": True,
            "data": result,
            "query": input_text,
            "type": "step-by-step",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/plot', methods=['POST'])
def api_plot():
    """图表生成API"""
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必需参数 'input'"
            }), 400
        
        input_text = data['input']
        width = data.get('width', 400)
        height = data.get('height', 300)
        
        result = wolfram_api.get_plot(input_text, width, height)
        
        return jsonify({
            "success": True,
            "data": result,
            "query": input_text,
            "type": "plot",
            "width": width,
            "height": height,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/suggestions/<path:query_text>')
def api_suggestions(query_text):
    """查询建议API"""
    try:
        suggestions = wolfram_api.get_related_queries(query_text)
        return jsonify({
            "success": True,
            "query": query_text,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "query": query_text
        }), 500

@app.route('/api/docs')
def api_docs():
    """API文档"""
    docs = {
        "service": "Wolfram|Alpha Enhanced API Server",
        "version": "2.0.0",
        "description": "基于官方Wolfram|Alpha API文档实现的完整功能服务器",
        "base_url": request.host_url,
        "endpoints": {
            "/": {
                "method": "GET",
                "description": "首页和API测试界面"
            },
            "/health": {
                "method": "GET", 
                "description": "健康检查"
            },
            "/api/query": {
                "method": "POST",
                "description": "完整查询API，支持所有官方参数",
                "parameters": {
                    "input": "查询文本 (必需)",
                    "format": "输出格式 (plaintext, image, html, mathml, sound, wav)",
                    "output": "输出类型 (xml, json)",
                    "includepodid": "包含特定pod ID",
                    "excludepodid": "排除特定pod ID",
                    "podtitle": "包含特定pod标题",
                    "podindex": "包含特定pod索引",
                    "scanner": "指定扫描器",
                    "podstate": "pod状态",
                    "assumption": "假设",
                    "units": "单位系统",
                    "width": "图像宽度",
                    "location": "位置信息"
                }
            },
            "/api/simple/{query}": {
                "method": "GET",
                "description": "简单结果API，仅返回主要结果"
            },
            "/api/validate": {
                "method": "POST",
                "description": "查询验证API",
                "parameters": {
                    "input": "查询文本 (必需)"
                }
            },
            "/api/stepbystep": {
                "method": "POST",
                "description": "逐步解决方案API",
                "parameters": {
                    "input": "查询文本 (必需)"
                }
            },
            "/api/plot": {
                "method": "POST",
                "description": "图表生成API",
                "parameters": {
                    "input": "查询文本 (必需)",
                    "width": "图表宽度 (可选)",
                    "height": "图表高度 (可选)"
                }
            },
            "/api/suggestions/{query}": {
                "method": "GET",
                "description": "查询建议API"
            }
        },
        "examples": {
            "basic_query": {
                "url": "/api/query",
                "method": "POST",
                "body": {
                    "input": "2+2",
                    "format": "plaintext",
                    "output": "json"
                }
            },
            "math_query": {
                "url": "/api/query", 
                "method": "POST",
                "body": {
                    "input": "solve x^2 + 3x + 2 = 0",
                    "format": "plaintext,image",
                    "output": "json",
                    "includepodid": "Result,Solution"
                }
            },
            "step_by_step": {
                "url": "/api/stepbystep",
                "method": "POST", 
                "body": {
                    "input": "derivative of x^2 + 3x + 1"
                }
            }
        }
    }
    
    return jsonify(docs)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "接口不存在",
        "available_endpoints": [
            "/", "/health", "/api/docs", "/api/query", "/api/simple/<query>", 
            "/api/validate", "/api/stepbystep", "/api/plot", "/api/suggestions/<query>"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "服务器内部错误",
        "message": "请检查请求参数或联系管理员"
    }), 500

if __name__ == '__main__':
    import sys
    import os
    
    # 设置UTF-8编码输出
    if sys.platform.startswith('win'):
        os.system('chcp 65001 > nul')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("Wolfram|Alpha Enhanced API Server 启动中...")
    print("=" * 60)
    print(f"服务地址: http://localhost:5000")
    print(f"API文档: http://localhost:5000/api/docs")
    print(f"健康检查: http://localhost:5000/health")
    print(f"测试界面: http://localhost:5000/")
    print()
    print("主要功能:")
    print("  - 完整的Full Results API支持")
    print("  - 所有官方API参数支持")
    print("  - 查询验证功能")
    print("  - Step-by-step解决方案")
    print("  - 图表和可视化")
    print("  - Assumptions处理")
    print()
    print("示例请求:")
    print("  POST http://localhost:5000/api/query")
    print('       {"input": "solve x^2+3x+2=0", "format": "plaintext", "output": "json"}')
    print("  GET  http://localhost:5000/api/simple/2+2")
    print("  POST http://localhost:5000/api/stepbystep")
    print('       {"input": "derivative of x^2"}')
    print("=" * 60)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
