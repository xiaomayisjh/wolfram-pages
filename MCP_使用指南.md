# Wolfram|Alpha MCP 使用指南

## 问题解决

您之前遇到的 "name 'wolfram_alpha' is not defined" 错误已经解决。现在 MCP 工具可以正常工作了。

## 正确的工具调用方式

在 MCP 客户端中，您应该使用以下工具名称：

### 1. 数学计算工具
```
工具名称: wolfram_math
参数: 
- expression: 数学表达式
- include_plot: 是否包含图形（可选）
```

**示例：**
- 求解五次方程：`wolfram_math(expression="solve x^5 + 179x^2 + 198 = 0")`
- 基本计算：`wolfram_math(expression="2 + 2")`
- 微积分：`wolfram_math(expression="integrate x^2 dx")`

### 2. 通用查询工具
```
工具名称: wolfram_query
参数:
- query: 查询文本
- format: 输出格式（可选）
- pod_id: 特定pod ID（可选）
```

**示例：**
- 人口查询：`wolfram_query(query="population of China")`
- 科学查询：`wolfram_query(query="H2O molecular structure")`

### 3. 科学查询工具
```
工具名称: wolfram_science
参数:
- topic: 科学主题
- include_visualization: 是否包含可视化（可选）
```

### 4. 事实查询工具
```
工具名称: wolfram_fact
参数:
- question: 事实性问题
```

## 五次方程求解结果

对于方程 **x^5 + 179x^2 + 198 = 0**，Wolfram Alpha 给出了以下数值解：

**实数解：**
- x ≈ -5.69901

**复数解：**
- x ≈ -0.003417 - 1.051684 i
- x ≈ -0.003417 + 1.051684 i  
- x ≈ 2.85292 - 4.82416 i
- x ≈ 2.85292 + 4.82416 i

**根的性质：**
- 根的和：0
- 根的积：-198

## 配置说明

确保您的 MCP 客户端配置正确：

```json
{
  "mcpServers": {
    "wolfram-alpha": {
      "command": "H:\\项目文件\\wolfram-api\\.venv\\Scripts\\python.exe",
      "args": ["H:\\项目文件\\wolfram-api\\mcp_wolfram_server.py"],
      "cwd": "H:\\项目文件\\wolfram-api",
      "env": {
        "PYTHONPATH": "H:\\项目文件\\wolfram-api\\open-source"
      }
    }
  }
}
```

## 测试验证

您可以使用以下命令测试 MCP 工具：

```bash
# 检查环境
python start_mcp_server.py --check

# 运行测试
python test_quintic.py

# 启动 MCP 服务器
python start_mcp_server.py
```

## 常见问题

1. **工具名称错误**：确保使用正确的工具名称（wolfram_math, wolfram_query 等）
2. **参数格式错误**：确保参数以字典形式传递
3. **网络连接问题**：确保能够访问 Wolfram Alpha API

## 支持的功能

- ✅ 数学计算和方程求解
- ✅ 科学查询和分子结构
- ✅ 事实查询和地理信息
- ✅ 复数计算
- ✅ 微积分和积分
- ✅ 函数绘图（文本描述）

现在您可以正常使用 Wolfram Alpha MCP 工具来解决各种数学和科学问题了！
