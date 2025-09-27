# Wolfram|Alpha API 网络服务

基于Flask框架的Wolfram|Alpha API网络服务，提供RESTful接口方便调用Wolfram|Alpha Mobile API。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install flask flask-cors requests
```

### 2. 启动服务

```bash
python wolfram_api_server.py
```

服务将在 `http://localhost:5000` 启动

### 3. 测试服务

访问 `http://localhost:5000` 查看API文档

## 📡 API 接口

### 基础接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | API文档首页 |
| GET | `/health` | 健康检查 |
| POST | `/query` | 执行查询 |
| GET | `/query/<query_text>` | 快速查询 |
| GET | `/result/<query_text>` | 获取结果文本 |
| GET | `/pods/<query_text>` | 获取所有pods |

### 专用接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/math/<query_text>` | 数学查询 |
| GET | `/science/<query_text>` | 科学查询 |

## 🔧 使用示例

### 1. Python客户端

```python
import requests

# 快速查询
response = requests.get('http://localhost:5000/query/2+2')
result = response.json()
print(result)

# POST查询
data = {
    "input": "population of France",
    "format": "plaintext",
    "output": "json"
}
response = requests.post('http://localhost:5000/query', json=data)
result = response.json()
print(result)
```

### 2. JavaScript客户端

```javascript
// 快速查询
fetch('http://localhost:5000/query/2+2')
    .then(response => response.json())
    .then(data => console.log(data));

// POST查询
fetch('http://localhost:5000/query', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        input: 'population of France',
        format: 'plaintext',
        output: 'json'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

### 3. cURL命令

```bash
# 快速查询
curl "http://localhost:5000/query/2+2"

# POST查询
curl -X POST "http://localhost:5000/query" \
     -H "Content-Type: application/json" \
     -d '{"input": "population of France", "format": "plaintext", "output": "json"}'

# 数学查询
curl "http://localhost:5000/math/y%27%20=%20y/(x+y^3)"

# 科学查询
curl "http://localhost:5000/science/H2O"
```

## 📋 请求参数

### POST /query 参数

| 参数 | 类型 | 必需 | 描述 | 默认值 |
|------|------|------|------|--------|
| input | string | ✅ | 查询文本 | - |
| format | string | ❌ | 输出格式 | plaintext |
| output | string | ❌ | 输出类型 | json |
| includepodid | string | ❌ | 包含特定pod ID | - |

### 支持的格式

- **format**: `plaintext`, `xml`
- **output**: `json`, `xml`, `plaintext`

## 📊 响应格式

### 成功响应

```json
{
    "success": true,
    "data": {
        "queryresult": {
            "success": true,
            "pods": [
                {
                    "title": "Result",
                    "subpods": [
                        {
                            "plaintext": "4"
                        }
                    ]
                }
            ]
        }
    }
}
```

### 错误响应

```json
{
    "success": false,
    "error": "错误信息"
}
```

## 🎯 客户端示例

### Python客户端 (client_example.py)

```bash
python client_example.py
```

功能包括：
- 基本查询演示
- 高级查询演示
- POST请求演示
- 错误处理演示
- 性能测试

### Web客户端 (web_client.html)

在浏览器中打开 `web_client.html`，提供：
- 图形化查询界面
- 多种查询选项
- 实时结果展示
- 快速查询示例
- API信息查看

## 🔍 查询类型示例

### 数学查询
- `2+2` - 基本算术
- `sqrt(16)` - 平方根
- `y' = y/(x+y^3)` - 微分方程
- `integrate x^2` - 积分

### 科学查询
- `H2O` - 化学分子
- `speed of light` - 物理常数
- `atomic mass of carbon` - 原子质量

### 地理查询
- `population of France` - 人口信息
- `weather in Beijing` - 天气信息
- `area of China` - 面积信息

### 单位转换
- `1 mile to km` - 长度转换
- `100°F to °C` - 温度转换
- `1 gallon to liters` - 体积转换

## ⚙️ 配置选项

### 服务器配置

在 `wolfram_api_server.py` 中修改：

```python
# 修改端口
app.run(debug=True, host='0.0.0.0', port=8080)

# 修改API基础URL
client = WolframAPIClient(base_url="http://your-server:8080")
```

### API配置

在 `wolfram_mobile_api.py` 中修改：

```python
class WolframMobileAPI:
    def __init__(self):
        self.appid = "YOUR_APP_ID"  # 自定义AppID
        self.sig_salt = "YOUR_SALT"  # 自定义签名盐
```

## 🛠️ 开发指南

### 添加新接口

```python
@app.route('/custom/<query_text>')
def custom_query(query_text):
    try:
        # 自定义处理逻辑
        result = wolfram_api.query_json(query_text, **custom_params)
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

### 添加中间件

```python
@app.before_request
def before_request():
    # 请求前处理
    pass

@app.after_request
def after_request(response):
    # 响应后处理
    return response
```

## 🔒 安全考虑

### 当前安全措施
- CORS支持
- 输入验证
- 错误处理
- 请求限制

### 生产环境建议
- 使用HTTPS
- 添加API密钥认证
- 实现请求频率限制
- 添加日志记录
- 配置防火墙

## 📈 性能优化

### 已实现优化
- 连接复用
- 错误重试
- 响应缓存

### 进一步优化建议
- Redis缓存
- 负载均衡
- CDN加速
- 数据库优化

## 🐛 故障排除

### 常见问题

1. **服务无法启动**
   - 检查端口是否被占用
   - 确认依赖包已安装
   - 查看错误日志

2. **查询失败**
   - 检查网络连接
   - 验证查询格式
   - 查看API响应

3. **CORS错误**
   - 确认CORS配置
   - 检查请求头
   - 验证域名设置

### 调试模式

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看请求详情
print(f"Request URL: {url}")
print(f"Request Data: {data}")
print(f"Response: {response.text}")
```

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- ✨ 初始版本发布
- 🔧 Flask网络服务
- 📡 RESTful API接口
- 🐍 Python客户端示例
- 🌐 Web前端客户端
- 📚 完整文档

## 🤝 贡献指南

欢迎贡献代码和建议！

### 如何贡献
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

### 贡献方向
- 🐛 Bug修复
- ✨ 新功能
- 📚 文档改进
- 🎨 UI/UX优化
- ⚡ 性能优化

## 📄 许可证

本项目仅供学习和研究使用。请遵守Wolfram|Alpha的使用条款。

## 🙏 致谢

- Wolfram|Alpha - 提供强大的计算引擎
- Flask - 优秀的Python Web框架
- Tailwind CSS - 现代化的CSS框架
- MathJax - 数学公式渲染

---

**享受使用Wolfram|Alpha API网络服务！** 🚀
