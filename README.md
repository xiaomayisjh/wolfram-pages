# Wolfram|Alpha API 项目集合

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)](#许可证)

一个完整的Wolfram|Alpha API实现项目集合，包含多个版本和实现方式，从简单的概念验证到完整的官方API仿制版本。

## 🎯 项目概述

本项目提供了多种方式来访问和使用Wolfram|Alpha的强大计算能力：

- **移动API版本** - 基于Wolfram|Alpha Mobile API的轻量级实现
- **增强版本** - 完整仿照官方版本的Pod输出系统
- **概念验证** - 原始的API调用实现和测试

## 📁 项目结构

```
wolfram-api/
├── mobile_api/                    # 移动API网络服务版本
│   ├── wolfram_api_server.py      # Flask API服务器
│   ├── wolfram_mobile_api.py      # Mobile API封装
│   ├── web_client.html            # Web客户端界面
│   ├── client_example.py          # Python客户端示例
│   ├── copyWolfram.html           # 简化版前端
│   ├── API_Server_README.md       # API服务器文档
│   └── Frontend_README.md         # 前端文档
├── pages/                         # 增强版本 (完整官方仿制)
│   ├── wolfram_enhanced_api.py    # 增强版API服务器
│   ├── wolfram_alpha_enhanced.html # 纯前端版本
│   ├── wolfram_client_enhanced.html # 客户端版本
│   ├── start_wolfram_enhanced.py  # 启动脚本
│   └── WOLFRAM_ENHANCED_README.md # 增强版文档
├── mobile_poc/                    # 概念验证版本
│   ├── poc.py                     # 原始概念验证
│   ├── full-spi.py               # 完整API实现
│   └── wolfram_mobile_api.py     # API封装
├── requirements.txt               # 基础依赖
├── requirements-enhanced.txt      # 增强版依赖
├── requirements-dev.txt          # 开发环境依赖
└── README.md                     # 本文档
```

## 🚀 快速开始

### 方法1: 移动API网络服务 (推荐新手)

最简单的使用方式，提供RESTful API接口：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动API服务器
cd mobile_api
python wolfram_api_server.py

# 3. 访问 http://localhost:5000
```

**特点:**
- ✅ 简单易用，开箱即用
- ✅ RESTful API接口
- ✅ 完整的Web客户端
- ✅ 详细的API文档

### 方法2: 增强版本 (推荐高级用户)

完整仿照官方Wolfram|Alpha的实现：

```bash
# 1. 安装增强版依赖
pip install -r requirements-enhanced.txt

# 2. 启动增强版服务器
cd pages
python wolfram_enhanced_api.py

# 3. 打开客户端页面
# 浏览器访问 wolfram_client_enhanced.html
```

**特点:**
- ✅ 完整的Pod渲染系统
- ✅ Assumptions智能处理
- ✅ Step-by-Step详细展示
- ✅ 官方界面风格
- ✅ 高级查询功能

### 方法3: 概念验证版本 (开发者)

用于学习和理解API工作原理：

```bash
# 直接运行概念验证
cd mobile_poc
python poc.py
```

## 🔧 功能特性对比

| 功能 | 移动API版本 | 增强版本 | 概念验证版本 |
|------|-------------|----------|-------------|
| **基础查询** | ✅ | ✅ | ✅ |
| **Web界面** | ✅ | ✅ | ❌ |
| **RESTful API** | ✅ | ✅ | ❌ |
| **Pod渲染** | 基础 | 完整 | 基础 |
| **数学公式渲染** | ✅ | ✅ | ❌ |
| **Assumptions处理** | ❌ | ✅ | ❌ |
| **Step-by-Step** | ❌ | ✅ | ❌ |
| **历史记录** | ❌ | ✅ | ❌ |
| **搜索建议** | ❌ | ✅ | ❌ |
| **响应式设计** | ✅ | ✅ | ❌ |
| **开发难度** | 简单 | 中等 | 简单 |

## 💡 使用示例

### 基础数学计算
```
输入: 2+2
结果: 4
```

### 方程求解
```
输入: solve x^2 + 3x + 2 = 0
结果: x = -1, x = -2
```

### 科学查询
```
输入: molecular structure of water
结果: H2O分子结构和相关信息
```

### 单位转换
```
输入: 100 km/h to m/s
结果: 27.78 m/s
```

### 地理信息
```
输入: population of China
结果: 中国人口数据和统计信息
```

## 📡 API接口

### 移动API版本接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | API文档首页 |
| GET | `/health` | 健康检查 |
| POST | `/query` | 执行查询 |
| GET | `/query/<query_text>` | 快速查询 |
| GET | `/result/<query_text>` | 获取结果文本 |
| GET | `/pods/<query_text>` | 获取所有pods |
| GET | `/math/<query_text>` | 数学查询 |
| GET | `/science/<query_text>` | 科学查询 |

### 增强版本接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | 首页和测试界面 |
| GET | `/health` | 健康检查 |
| POST | `/api/query` | 完整查询API |
| GET | `/api/simple/<query>` | 简单结果API |
| POST | `/api/validate` | 查询验证API |
| POST | `/api/stepbystep` | 逐步解决方案API |
| POST | `/api/plot` | 图表生成API |
| GET | `/api/suggestions/<query>` | 查询建议API |

## 🛠️ 开发指南

### 环境要求

- Python 3.7+
- Flask 2.0+
- 现代浏览器 (支持ES6+)

### 安装开发环境

```bash
# 克隆项目
git clone <repository-url>
cd wolfram-api

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest

# 代码格式化
black .
flake8 .
```

### 添加新功能

1. **扩展API接口**
```python
@app.route('/custom/<query_text>')
def custom_query(query_text):
    # 自定义处理逻辑
    result = wolfram_api.query(query_text)
    return jsonify(result)
```

2. **添加新的Pod类型**
```javascript
function getPodIcon(podId) {
    const iconMap = {
        'YourPodType': 'your-icon'
    };
    return iconMap[podId] || 'info-circle';
}
```

3. **自定义样式**
```css
:root {
    --primary-color: #0066CC;
    --secondary-color: #003366;
}
```

## 🔍 支持的查询类型

### 数学计算
- ✅ 基础算术运算
- ✅ 代数方程求解
- ✅ 微积分计算
- ✅ 统计学分析
- ✅ 矩阵运算
- ✅ 数论问题

### 科学查询
- ✅ 物理常数和公式
- ✅ 化学分子结构
- ✅ 天文学数据
- ✅ 生物学信息
- ✅ 地球科学数据

### 实用工具
- ✅ 单位转换
- ✅ 日期时间计算
- ✅ 金融计算
- ✅ 地理信息查询
- ✅ 天气数据
- ✅ 营养信息

## 🐛 故障排除

### 常见问题

1. **服务无法启动**
   ```bash
   # 检查端口占用
   netstat -tulpn | grep :5000
   
   # 更换端口
   python wolfram_api_server.py --port 8080
   ```

2. **CORS错误**
   ```bash
   # 使用本地服务器
   python -m http.server 8000
   ```

3. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   
   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

4. **查询无结果**
   - 检查网络连接
   - 尝试不同的查询表述
   - 查看服务器日志

### 调试模式

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看API请求详情
print(f"Request: {request_data}")
print(f"Response: {response_data}")
```

## 📈 性能优化

### 已实现的优化
- ✅ 连接复用和会话管理
- ✅ 请求缓存机制
- ✅ 防抖搜索
- ✅ 懒加载资源
- ✅ 响应式设计

### 进一步优化建议
- 🔄 Redis缓存集成
- 🔄 负载均衡配置
- 🔄 CDN静态资源加速
- 🔄 数据库持久化
- 🔄 Service Worker离线支持

## 🔒 安全考虑

### 当前安全措施
- ✅ HTTPS请求
- ✅ MD5签名验证
- ✅ 输入验证和清理
- ✅ CORS配置
- ✅ 错误处理

### 生产环境建议
- 🔐 API密钥管理
- 🔐 访问频率限制
- 🔐 防火墙配置
- 🔐 日志监控
- 🔐 安全头设置

## 📊 项目统计

### 代码统计
- **总行数**: ~3000+ 行
- **Python文件**: 8个
- **HTML文件**: 5个
- **文档文件**: 4个

### 功能覆盖
- **API端点**: 15+
- **查询类型**: 10+
- **Pod类型**: 20+
- **界面组件**: 30+

## 📝 更新日志

### v2.0.0 (2024-01-XX) - 增强版本
- ✨ 完整的官方API支持
- 🎨 Pod渲染系统
- 🔧 增强版API服务器
- 📱 响应式设计优化
- 🧮 数学公式渲染
- 🎯 智能功能集成

### v1.0.0 (2024-01-XX) - 初始版本
- 🎯 移动API集成
- 🔧 Flask网络服务
- 📡 RESTful API接口
- 🌐 Web前端客户端
- 📚 完整文档

## 🤝 贡献指南

欢迎贡献代码和建议！

### 如何贡献
1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 贡献方向
- 🐛 Bug修复
- ✨ 新功能开发
- 📚 文档改进
- 🎨 UI/UX优化
- ⚡ 性能优化
- 🧪 测试用例
- 🔧 工具改进

## 📄 许可证

本项目仅供学习和研究使用。请遵守Wolfram|Alpha的使用条款和相关法律法规。

**重要提醒**: 
- 本项目不是Wolfram|Alpha的官方实现
- 请勿用于商业用途
- 遵守API使用限制和条款
- 尊重知识产权

## 🙏 致谢

- **Wolfram|Alpha** - 提供强大的计算引擎和API
- **Flask** - 优秀的Python Web框架
- **Tailwind CSS** - 现代化的CSS框架
- **MathJax** - 数学公式渲染引擎
- **Font Awesome** - 丰富的图标库
- **开源社区** - 提供各种优秀的工具和库

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 🐛 **Issues**: [GitHub Issues页面]
- 💬 **讨论**: [GitHub Discussions页面]
- 📧 **邮件**: [联系邮箱]

## 🔗 相关链接

- [Wolfram|Alpha官网](https://www.wolframalpha.com/)
- [Wolfram|Alpha API文档](https://products.wolframalpha.com/api/)
- [Flask官方文档](https://flask.palletsprojects.com/)
- [Python官方网站](https://www.python.org/)

---

**享受使用Wolfram|Alpha API项目集合！** 🚀

> 这是一个完整的学习和研究项目，通过多种实现方式展示了如何与Wolfram|Alpha API进行交互。从简单的概念验证到完整的官方仿制版本，为不同需求的用户提供了合适的解决方案。

---

*最后更新: 2025年10月*
