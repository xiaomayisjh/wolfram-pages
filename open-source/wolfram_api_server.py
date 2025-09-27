#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha API 网络服务
基于Flask框架，提供RESTful API接口
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import traceback
from wolfram_mobile_api import WolframMobileAPI

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 创建API实例
wolfram_api = WolframMobileAPI()

@app.route('/')
def home():
    """首页 - API文档"""
    return jsonify({
        "service": "Wolfram|Alpha API Server",
        "version": "1.0.0",
        "description": "基于Wolfram|Alpha Mobile API的网络服务",
        "endpoints": {
            "/query": "POST - 执行查询",
            "/query/<query_text>": "GET - 快速查询",
            "/result/<query_text>": "GET - 获取结果文本",
            "/pods/<query_text>": "GET - 获取所有pods",
            "/health": "GET - 健康检查"
        },
        "usage": {
            "POST /query": {
                "body": {
                    "input": "查询文本",
                    "format": "输出格式 (plaintext, xml)",
                    "output": "输出类型 (json, xml, plaintext)",
                    "includepodid": "包含特定pod ID (可选)"
                }
            },
            "GET /query/<query_text>": "快速查询，返回JSON格式",
            "GET /result/<query_text>": "获取主要结果文本",
            "GET /pods/<query_text>": "获取所有pods结果"
        }
    })

@app.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "service": "Wolfram|Alpha API Server",
        "version": "1.0.0"
    })

@app.route('/query', methods=['POST'])
def query():
    """执行Wolfram|Alpha查询"""
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必需参数 'input'"
            }), 400
        
        input_text = data['input']
        format_type = data.get('format', 'plaintext')
        output_type = data.get('output', 'json')
        includepodid = data.get('includepodid')
        
        # 构建查询参数
        kwargs = {}
        if includepodid:
            kwargs['includepodid'] = includepodid
        
        # 执行查询
        if output_type == 'json':
            result = wolfram_api.query_json(input_text, **kwargs)
        else:
            result = wolfram_api.query(input_text, format_type, output_type, **kwargs)
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/query/<path:query_text>')
def quick_query(query_text):
    """快速查询 - GET方式"""
    try:
        result = wolfram_api.query_json(query_text)
        return jsonify({
            "success": True,
            "query": query_text,
            "data": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "query": query_text
        }), 500

@app.route('/result/<path:query_text>')
def get_result(query_text):
    """获取主要结果文本"""
    try:
        result = wolfram_api.get_result_text(query_text)
        return jsonify({
            "success": True,
            "query": query_text,
            "result": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "query": query_text
        }), 500

@app.route('/pods/<path:query_text>')
def get_pods(query_text):
    """获取所有pods结果"""
    try:
        result = wolfram_api.get_all_results(query_text)
        return jsonify({
            "success": True,
            "query": query_text,
            "pods": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "query": query_text
        }), 500

@app.route('/math/<path:query_text>')
def math_query(query_text):
    """数学查询专用接口"""
    try:
        # 数学查询通常需要特殊处理
        result = wolfram_api.query_json(
            query_text, 
            includepodid="Result,Solution,Plot",
            podstate="Solution__Step-by-step solution"
        )
        return jsonify({
            "success": True,
            "query": query_text,
            "type": "math",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "query": query_text
        }), 500

@app.route('/science/<path:query_text>')
def science_query(query_text):
    """科学查询专用接口"""
    try:
        result = wolfram_api.query_json(query_text)
        return jsonify({
            "success": True,
            "query": query_text,
            "type": "science",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "query": query_text
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "接口不存在",
        "available_endpoints": [
            "/", "/health", "/query", "/query/<text>", 
            "/result/<text>", "/pods/<text>", "/math/<text>", "/science/<text>"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "服务器内部错误"
    }), 500

if __name__ == '__main__':
    print("Wolfram|Alpha API Server 启动中...")
    print("服务地址: http://localhost:5000")
    print("API文档: http://localhost:5000/")
    print("健康检查: http://localhost:5000/health")
    print("\n示例请求:")
    print("GET  http://localhost:5000/query/2+2")
    print("GET  http://localhost:5000/result/population%20of%20France")
    print("POST http://localhost:5000/query")
    print('     {"input": "H2O", "format": "plaintext", "output": "json"}')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
