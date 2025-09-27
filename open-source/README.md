# Wolfram|Alpha Full Results API Python 客户端

这是一个基于Wolfram|Alpha Full Results API的Python客户端，用于替代之前的Mobile App API。

## 主要变化

1. **API端点**: 从Mobile App API改为标准的Full Results API
2. **认证方式**: 移除了复杂的签名机制，使用简单的AppID认证
3. **请求格式**: 使用标准的HTTP GET请求，无需特殊签名

## 使用方法

### 1. 获取AppID

首先需要在[Wolfram|Alpha Developer Portal](https://developer.wolframalpha.com/)注册并获取AppID。

### 2. 配置AppID

在`full-spi.py`文件中，将`YOUR_APP_ID_HERE`替换为您的实际AppID：

```python
APPID = "YOUR_ACTUAL_APP_ID"
```

### 3. 基本使用

```python
from full-spi import query_wolfram, query_with_format, query_specific_pod

# 基本查询
result = query_wolfram("population of France")

# 指定输出格式
json_result = query_with_format("population of France", format_type="json")

# 查询特定pod
result_pod = query_specific_pod("population of France", "Result", "plaintext")
```

## API函数说明

### `query_wolfram(input_text, **kwargs)`
- **功能**: 基本查询函数
- **参数**: 
  - `input_text`: 查询文本
  - `**kwargs`: 其他API参数（如format, includepodid等）

### `query_with_format(input_text, format_type="xml", **kwargs)`
- **功能**: 指定输出格式的查询
- **参数**:
  - `input_text`: 查询文本
  - `format_type`: 输出格式（xml, json, plaintext等）
  - `**kwargs`: 其他API参数

### `query_specific_pod(input_text, pod_id, format_type="xml")`
- **功能**: 查询特定pod的结果
- **参数**:
  - `input_text`: 查询文本
  - `pod_id`: pod ID（如"Result", "Input"等）
  - `format_type`: 输出格式

### `validate_query(input_text)`
- **功能**: 验证查询是否有效
- **参数**:
  - `input_text`: 查询文本

### `query_with_assumptions(input_text, assumption_input)`
- **功能**: 使用假设进行查询
- **参数**:
  - `input_text`: 查询文本
  - `assumption_input`: 假设输入

## 支持的API参数

根据[Wolfram|Alpha API文档](https://products.wolframalpha.com/api/documentation)，支持的主要参数包括：

- `format`: 输出格式（xml, json, plaintext等）
- `includepodid`: 包含特定pod ID
- `excludepodid`: 排除特定pod ID
- `assumption`: 使用假设
- `podstate`: pod状态
- `location`: 位置信息
- `latlong`: 经纬度
- `width`: 图像宽度
- `maxwidth`: 最大图像宽度
- `scanner`: 扫描器类型
- `podtimeout`: pod超时时间
- `formattimeout`: 格式化超时时间
- `parsetimeout`: 解析超时时间
- `totaltimeout`: 总超时时间
- `recalculate`: 重新计算
- `async`: 异步处理

## 示例

运行`python full-spi.py`可以看到各种查询示例的输出。

## 注意事项

1. 确保您有有效的Wolfram|Alpha AppID
2. 某些查询可能需要付费账户才能访问
3. API有使用限制，请查看Wolfram|Alpha的API使用条款
4. 输入文本需要进行URL编码，但`urllib.parse.urlencode`会自动处理
