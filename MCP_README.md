# Wolfram|Alpha MCP 服务器

这是一个基于 Model Context Protocol (MCP) 的 Wolfram|Alpha 查询服务器，提供强大的数学计算、科学查询和事实查询能力。

## 功能特性

### 🔧 可用工具

1. **wolfram_query** - 通用 Wolfram|Alpha 查询
   - 支持数学计算、科学问题、事实查询等
   - 可选择输出格式（plaintext, json, xml）
   - 可指定特定 pod ID 获取特定结果

2. **wolfram_math** - 数学计算专用工具
   - 专门处理数学表达式和方程
   - 支持积分、微分、绘图等高级数学功能
   - 可选择是否包含图形结果

3. **wolfram_science** - 科学查询专用工具
   - 处理化学、物理、生物等科学主题
   - 支持分子结构、物理常数等查询
   - 可选择是否包含可视化结果

4. **wolfram_fact** - 事实查询专用工具
   - 查询各种事实性信息
   - 支持地理、历史、统计等数据查询

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements-mcp.txt
```

### 2. 配置 MCP 客户端

将以下配置添加到您的 MCP 客户端配置文件中：

```json
{
  "mcpServers": {
    "wolfram-alpha": {
      "command": "python",
      "args": ["mcp_wolfram_server.py"],
      "cwd": "/path/to/wolfram-api",
      "env": {
        "PYTHONPATH": "./open-source"
      }
    }
  }
}
```

### 3. 启动服务器

```bash
python mcp_wolfram_server.py
```

## 使用示例

### 数学计算

```python
# 基本数学运算
wolfram_query("2 + 2 * 3")

# 微积分
wolfram_math("integrate x^2 dx")

# 方程求解
wolfram_math("solve x^2 + 2x + 1 = 0")

# 绘图
wolfram_math("plot sin(x) from 0 to 2pi", include_plot=True)
```

### 科学查询

```python
# 化学结构
wolfram_science("H2O molecular structure")

# 物理常数
wolfram_science("speed of light")

# 元素信息
wolfram_science("carbon properties")
```

### 事实查询

```python
# 地理信息
wolfram_fact("population of China")

# 历史数据
wolfram_fact("when was the first computer invented")

# 统计信息
wolfram_fact("GDP of United States")
```

## 工具参数说明

### wolfram_query 参数

- `query` (必需): 查询文本
- `format` (可选): 输出格式，默认为 "plaintext"
- `pod_id` (可选): 特定 pod ID，如 "Result", "Input", "Solution"

### wolfram_math 参数

- `expression` (必需): 数学表达式
- `include_plot` (可选): 是否包含图形，默认为 False

### wolfram_science 参数

- `topic` (必需): 科学主题
- `include_visualization` (可选): 是否包含可视化，默认为 True

### wolfram_fact 参数

- `question` (必需): 事实性问题

## 输出格式

所有工具都返回格式化的文本结果，包含：

- 查询内容
- 分类结果（按 pod 分组）
- 详细的文本描述
- 错误信息（如果查询失败）

## 错误处理

服务器包含完善的错误处理机制：

- 网络请求错误
- API 响应错误
- 参数验证错误
- JSON 解析错误

所有错误都会以用户友好的方式返回。

## 技术架构

- **MCP 协议**: 使用 Model Context Protocol 进行通信
- **异步处理**: 基于 asyncio 的异步架构
- **Wolfram API**: 基于现有的 Wolfram|Alpha Mobile API 实现
- **类型安全**: 完整的类型提示支持

## 依赖关系

- `mcp`: MCP 协议支持
- `requests`: HTTP 请求处理
- `asyncio`: 异步编程支持
- `typing-extensions`: 类型提示支持

## 注意事项

1. 确保 `open-source` 目录中的 `wolfram_mobile_api.py` 文件存在
2. 服务器需要网络连接来访问 Wolfram|Alpha API
3. 某些查询可能需要较长时间，请耐心等待
4. 图形和可视化结果以文本形式返回

## 故障排除

### 常见问题

1. **导入错误**: 确保 PYTHONPATH 设置正确
2. **网络错误**: 检查网络连接和防火墙设置
3. **API 错误**: 检查 Wolfram|Alpha API 状态

### 调试模式

可以通过修改代码启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 许可证

本项目基于现有的 Wolfram|Alpha API 项目，遵循相同的许可证条款。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个 MCP 服务器。

## 更新日志

### v1.0.0
- 初始版本发布
- 支持四种主要查询工具
- 完整的错误处理机制
- 详细的文档和示例
