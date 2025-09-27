# Wolfram|Alpha MCP Agent 使用指南

## 问题解决

您遇到的 "name 'wolfram_alpha' is not defined" 错误是因为工具调用方式不正确。

## 正确的工具调用方式

### ❌ 错误的调用方式
```python
# 这些方式都是错误的
wolfram_alpha.wolfram_math()
wolfram_alpha____wolfram_math____mcp()
wolfram_alpha.wolfram_query()
```

### ✅ 正确的调用方式
```python
# 直接使用工具名称
wolfram_math(expression="solve x^5 + 179x^2 + 198 = 0")
wolfram_query(query="population of China")
wolfram_science(topic="H2O molecular structure")
wolfram_fact(question="capital of Japan")
```

## 工具详细说明

### 1. wolfram_math - 数学计算工具
**用途**: 专门用于数学计算和方程求解
**调用方式**: `wolfram_math(expression="数学表达式")`

**示例**:
```python
# 求解五次方程
wolfram_math(expression="solve x^5 + 179x^2 + 198 = 0")

# 求解二次方程
wolfram_math(expression="solve x^2 + 5x + 1 = 0")

# 微积分计算
wolfram_math(expression="integrate x^2 dx")

# 函数绘图
wolfram_math(expression="plot sin(x) from 0 to 2pi")
```

### 2. wolfram_query - 通用查询工具
**用途**: 用于一般性查询，包括数学、科学、事实等
**调用方式**: `wolfram_query(query="查询内容")`

**示例**:
```python
# 人口查询
wolfram_query(query="population of China")

# 分子结构查询
wolfram_query(query="H2O molecular structure")

# 物理常数查询
wolfram_query(query="speed of light")
```

### 3. wolfram_science - 科学查询工具
**用途**: 专门用于科学相关查询
**调用方式**: `wolfram_science(topic="科学主题")`

**示例**:
```python
# 元素性质查询
wolfram_science(topic="carbon properties")

# 生物结构查询
wolfram_science(topic="DNA structure")
```

### 4. wolfram_fact - 事实查询工具
**用途**: 专门用于事实性信息查询
**调用方式**: `wolfram_fact(question="事实性问题")`

**示例**:
```python
# 地理事实查询
wolfram_fact(question="capital of Japan")

# 历史事实查询
wolfram_fact(question="when was the first computer invented")
```

## 五次方程求解示例

对于方程 **x^5 + 179x^2 + 198 = 0**，正确的调用方式是：

```python
result = wolfram_math(expression="solve x^5 + 179x^2 + 198 = 0")
```

**结果**:
- 实数解: x ≈ -5.69901
- 复数解: 4个复数根
- 根的和: 0
- 根的积: -198

## 常见错误和解决方案

### 错误 1: NameError
```
NameError: name 'wolfram_alpha' is not defined
```
**解决方案**: 直接使用工具名称，不要加前缀

### 错误 2: 工具名称错误
```
wolfram_alpha____wolfram_math____mcp()
```
**解决方案**: 使用简化的工具名称 `wolfram_math()`

### 错误 3: 参数格式错误
```python
# 错误
wolfram_math("solve x^2 + 1 = 0")

# 正确
wolfram_math(expression="solve x^2 + 1 = 0")
```

## 测试验证

您可以使用以下命令测试工具是否正常工作：

```bash
# 检查环境
python start_mcp_server.py --check

# 运行演示
python mcp_demo.py

# 测试五次方程
python test_quintic.py
```

## 配置检查

确保 MCP 客户端配置正确：

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

## 关键要点

1. **直接使用工具名称**: `wolfram_math()`, `wolfram_query()` 等
2. **参数以字典形式传递**: `{"expression": "..."}`
3. **确保 MCP 服务器正在运行**
4. **检查网络连接和 Wolfram API 状态**

现在您应该能够正确使用 Wolfram Alpha MCP 工具了！
