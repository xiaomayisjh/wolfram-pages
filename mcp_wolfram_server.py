#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wolfram|Alpha MCP (Model Context Protocol) 服务器
提供 Wolfram|Alpha 查询能力的 MCP 工具
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# 导入现有的 Wolfram API 类
import os
open_source_path = os.path.join(os.path.dirname(__file__), 'open-source')
if open_source_path not in sys.path:
    sys.path.insert(0, open_source_path)
from wolfram_mobile_api import WolframMobileAPI

# 创建 MCP 服务器实例
server = Server("wolfram-alpha-mcp")

# 创建 Wolfram API 实例
wolfram_api = WolframMobileAPI()

@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出可用的工具"""
    return [
        Tool(
            name="wolfram_query",
            description="Wolfram|Alpha 通用查询工具 - 可以回答数学、科学、事实等各种问题。使用此工具进行一般性查询。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要查询的问题或表达式，例如：'population of China', 'H2O molecular structure', 'what is the speed of light'"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["plaintext", "json", "xml"],
                        "default": "plaintext",
                        "description": "输出格式类型"
                    },
                    "pod_id": {
                        "type": "string",
                        "description": "指定要获取的特定 pod ID（如 'Result', 'Input', 'Solution' 等），如果为空则返回所有结果"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="wolfram_math",
            description="Wolfram|Alpha 数学计算工具 - 专门用于解决数学问题，包括方程求解、微积分、代数运算等。当需要数学计算时使用此工具。",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式或方程，例如：'solve x^2 + 2x + 1 = 0', 'integrate x^2 dx', 'plot sin(x)', 'solve x^5 + 179x^2 + 198 = 0'"
                    },
                    "include_plot": {
                        "type": "boolean",
                        "default": False,
                        "description": "是否包含图形绘制结果"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="wolfram_science",
            description="Wolfram|Alpha 科学查询工具 - 专门用于科学相关查询，包括化学、物理、生物等。当需要科学信息时使用此工具。",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "科学主题查询，例如：'H2O molecular structure', 'speed of light', 'DNA structure', 'carbon properties'"
                    },
                    "include_visualization": {
                        "type": "boolean",
                        "default": True,
                        "description": "是否包含可视化结果"
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="wolfram_fact",
            description="Wolfram|Alpha 事实查询工具 - 专门用于查询事实性信息，包括地理、历史、统计等。当需要事实数据时使用此工具。",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "事实性问题，例如：'population of France', 'capital of Japan', 'area of Earth', 'when was the first computer invented'"
                    }
                },
                "required": ["question"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    
    if name == "wolfram_query":
        return await handle_wolfram_query(arguments)
    elif name == "wolfram_math":
        return await handle_wolfram_math(arguments)
    elif name == "wolfram_science":
        return await handle_wolfram_science(arguments)
    elif name == "wolfram_fact":
        return await handle_wolfram_fact(arguments)
    else:
        raise ValueError(f"未知的工具: {name}")

async def handle_wolfram_query(arguments: Dict[str, Any]) -> List[TextContent]:
    """处理通用 Wolfram 查询"""
    query = arguments.get("query", "")
    format_type = arguments.get("format", "plaintext")
    pod_id = arguments.get("pod_id")
    
    if not query:
        return [TextContent(type="text", text="错误：查询内容不能为空")]
    
    try:
        if pod_id:
            # 获取特定 pod 的结果
            result = wolfram_api.get_result_text(query, pod_id)
            return [TextContent(type="text", text=f"查询结果 ({pod_id}):\n{result}")]
        else:
            # 获取所有结果
            all_results = wolfram_api.get_all_results(query)
            
            if "error" in all_results:
                return [TextContent(type="text", text=f"查询失败: {all_results['error']}")]
            
            result_text = f"查询: {query}\n\n"
            result_text += "=" * 50 + "\n\n"
            
            for pod_name, pod_results in all_results.items():
                result_text += f"📊 {pod_name}:\n"
                result_text += "-" * 30 + "\n"
                for i, result in enumerate(pod_results, 1):
                    result_text += f"{i}. {result}\n"
                result_text += "\n"
            
            return [TextContent(type="text", text=result_text)]
            
    except Exception as e:
        return [TextContent(type="text", text=f"查询执行失败: {str(e)}")]

async def handle_wolfram_math(arguments: Dict[str, Any]) -> List[TextContent]:
    """处理数学查询"""
    expression = arguments.get("expression", "")
    include_plot = arguments.get("include_plot", False)
    
    if not expression:
        return [TextContent(type="text", text="错误：数学表达式不能为空")]
    
    try:
        # 使用通用查询方法获取所有结果
        all_results = wolfram_api.get_all_results(expression)
        
        if "error" in all_results:
            return [TextContent(type="text", text=f"数学计算失败: {all_results['error']}")]
        
        result_text = f"🧮 数学计算: {expression}\n\n"
        result_text += "=" * 50 + "\n\n"
        
        for pod_name, pod_results in all_results.items():
            result_text += f"📐 {pod_name}:\n"
            result_text += "-" * 30 + "\n"
            for i, result in enumerate(pod_results, 1):
                result_text += f"{i}. {result}\n"
            result_text += "\n"
        
        return [TextContent(type="text", text=result_text)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"数学计算失败: {str(e)}")]

async def handle_wolfram_science(arguments: Dict[str, Any]) -> List[TextContent]:
    """处理科学查询"""
    topic = arguments.get("topic", "")
    include_visualization = arguments.get("include_visualization", True)
    
    if not topic:
        return [TextContent(type="text", text="错误：科学主题不能为空")]
    
    try:
        # 构建科学查询参数
        kwargs = {}
        if include_visualization:
            kwargs["includepodid"] = "Result,Properties,Structure,Visualization"
        else:
            kwargs["includepodid"] = "Result,Properties"
        
        # 执行查询
        result = wolfram_api.query_json(topic, **kwargs)
        query_result = result.get('queryresult', {})
        
        if not query_result.get('success', False):
            return [TextContent(type="text", text=f"科学查询失败: {query_result.get('error', '未知错误')}")]
        
        pods = query_result.get('pods', [])
        result_text = f"🔬 科学查询: {topic}\n\n"
        result_text += "=" * 50 + "\n\n"
        
        for pod in pods:
            pod_title = pod.get('title', 'Unknown')
            subpods = pod.get('subpods', [])
            
            result_text += f"🔬 {pod_title}:\n"
            result_text += "-" * 30 + "\n"
            
            for subpod in subpods:
                plaintext = subpod.get('plaintext', '')
                if plaintext:
                    result_text += f"{plaintext}\n"
            
            result_text += "\n"
        
        return [TextContent(type="text", text=result_text)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"科学查询失败: {str(e)}")]

async def handle_wolfram_fact(arguments: Dict[str, Any]) -> List[TextContent]:
    """处理事实查询"""
    question = arguments.get("question", "")
    
    if not question:
        return [TextContent(type="text", text="错误：问题不能为空")]
    
    try:
        # 执行事实查询
        result = wolfram_api.get_result_text(question, "Result")
        
        if "查询失败" in result or "获取结果失败" in result:
            # 尝试获取所有结果
            all_results = wolfram_api.get_all_results(question)
            if "error" in all_results:
                return [TextContent(type="text", text=f"事实查询失败: {all_results['error']}")]
            
            result_text = f"📚 事实查询: {question}\n\n"
            result_text += "=" * 50 + "\n\n"
            
            for pod_name, pod_results in all_results.items():
                result_text += f"📖 {pod_name}:\n"
                result_text += "-" * 30 + "\n"
                for result in pod_results:
                    result_text += f"{result}\n"
                result_text += "\n"
            
            return [TextContent(type="text", text=result_text)]
        else:
            return [TextContent(type="text", text=f"📚 事实查询: {question}\n\n结果:\n{result}")]
        
    except Exception as e:
        return [TextContent(type="text", text=f"事实查询失败: {str(e)}")]

async def main():
    """主函数"""
    # 使用 stdio 传输
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="wolfram-alpha-mcp",
                server_version="1.0.0",
                capabilities={
                    "tools": {}
                }
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
