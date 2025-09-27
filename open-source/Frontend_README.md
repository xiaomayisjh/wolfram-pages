# Wolfram|Alpha 前端版 - 基于Mobile API

## 🎯 **项目简介**

这是一个基于Wolfram|Alpha Mobile API的纯前端实现，完全在浏览器中运行，无需后端服务器。它复刻了Wolfram|Alpha的核心功能，包括数学计算、科学查询、地理信息等。

## ✨ **主要特性**

### 🔧 **技术特性**
- **纯前端实现** - 无需后端服务器，直接在浏览器中运行
- **Mobile API集成** - 使用Wolfram|Alpha Mobile API，无需注册AppID
- **响应式设计** - 支持桌面、平板、手机等各种设备
- **数学公式渲染** - 使用MathJax渲染数学公式
- **实时搜索** - 支持实时查询和结果展示

### 🎨 **界面特性**
- **现代化UI** - 使用Tailwind CSS构建的现代化界面
- **Wolfram风格** - 复刻Wolfram|Alpha的经典设计风格
- **结果卡片** - 清晰的结果展示，支持多种数据类型
- **加载动画** - 优雅的加载状态指示
- **错误处理** - 完善的错误处理和用户反馈

### 🚀 **功能特性**
- **多类型查询** - 支持数学、科学、地理、化学等各种查询
- **示例查询** - 内置常用查询示例，一键测试
- **键盘快捷键** - 支持Ctrl+K快速聚焦搜索框
- **主题切换** - 支持明暗主题切换
- **结果分类** - 智能识别和分类不同类型的结果

## 📁 **文件结构**

```
wolfram-api/open-source/
├── wolfram_frontend.html    # 主前端文件
├── wolfram_mobile_api.py    # Python API封装
├── poc.py                   # 原始Mobile API实现
├── full-spi.py             # Full API实现
└── README.md               # 使用说明
```

## 🚀 **快速开始**

### 方法1: 直接打开
1. 下载 `wolfram_frontend.html` 文件
2. 用浏览器直接打开文件
3. 开始使用！

### 方法2: 本地服务器
```bash
# 进入项目目录
cd wolfram-api/open-source

# 启动本地服务器
python -m http.server 8000

# 访问 http://localhost:8000/wolfram_frontend.html
```

## 💡 **使用示例**

### 数学计算
- `2+2` - 基本算术
- `sqrt(16)` - 平方根
- `sin(pi/2)` - 三角函数
- `y' = y/(x+y^3)` - 微分方程

### 科学查询
- `H2O` - 化学分子
- `speed of light` - 物理常数
- `atomic mass of carbon` - 原子质量

### 地理信息
- `population of France` - 人口信息
- `weather in Beijing` - 天气信息
- `area of China` - 面积信息

### 单位转换
- `1 mile to km` - 长度转换
- `100°F to °C` - 温度转换
- `1 gallon to liters` - 体积转换

## 🔧 **技术实现**

### API调用流程
1. **用户输入** - 用户在搜索框输入查询
2. **参数构建** - 构建API请求参数
3. **签名计算** - 使用MD5算法计算请求签名
4. **API调用** - 向Wolfram|Alpha Mobile API发送请求
5. **结果解析** - 解析JSON响应数据
6. **界面渲染** - 在页面上展示结果

### 核心代码结构
```javascript
// API配置
const WOLFRAM_CONFIG = {
    appid: '3H4296-5YPAGQUJK7',
    server: 'api.wolframalpha.com',
    sigSalt: 'vFdeaRwBTVqdc5CL',
    userAgent: 'Wolfram Android App'
};

// 主要函数
- queryWolfram(inputText)     // 执行API查询
- craftSignedUrl(url)        // 构建签名URL
- calculateSignature(query)   // 计算MD5签名
- displayResults(result)      // 显示结果
- createPodElement(pod)       // 创建结果卡片
```

### 签名算法
```javascript
function calculateSignature(queryString) {
    const params = queryString.split('&')
        .map(param => param.split('='))
        .filter(param => param.length === 2)
        .sort((a, b) => a[0].localeCompare(b[0]));

    let signatureString = WOLFRAM_CONFIG.sigSalt;
    for (const [key, value] of params) {
        signatureString += key + decodeURIComponent(value);
    }

    return CryptoJS.MD5(signatureString).toString().toUpperCase();
}
```

## 🎨 **界面设计**

### 颜色方案
- **主色调**: #0066CC (Wolfram蓝)
- **次要色**: #003366 (深蓝)
- **背景色**: #E6F2FF (浅蓝)
- **文本色**: #333333 (深灰)
- **边框色**: #E0E0E0 (浅灰)

### 响应式布局
- **手机** (< 768px): 单列布局
- **平板** (768px - 1023px): 双列布局
- **桌面** (> 1024px): 三列布局

### 组件设计
- **搜索框**: 大尺寸输入框，支持键盘快捷键
- **结果卡片**: 悬停效果，清晰的层次结构
- **加载动画**: 三个点的弹跳动画
- **错误提示**: 红色警告框，包含重试按钮

## 🔍 **结果展示**

### Pod类型识别
系统会自动识别不同类型的结果并显示相应的图标：

| Pod类型 | 图标 | 说明 |
|---------|------|------|
| Input | ⌨️ | 输入解释 |
| Result | ✅ | 主要结果 |
| Solution | 💡 | 解题步骤 |
| Plot | 📈 | 图表 |
| Graph | 🔗 | 图形 |
| Table | 📊 | 表格 |
| Formula | 🧮 | 公式 |
| Properties | 📋 | 属性 |

### 数学公式渲染
使用MathJax自动渲染数学公式：
- 检测数学符号和函数
- 自动包装为LaTeX格式
- 实时渲染为美观的数学公式

## 🛠️ **自定义配置**

### 修改API配置
```javascript
const WOLFRAM_CONFIG = {
    appid: 'YOUR_APP_ID',        // 自定义AppID
    server: 'api.wolframalpha.com',
    sigSalt: 'YOUR_SALT',       // 自定义签名盐
    userAgent: 'Your App Name'  // 自定义User-Agent
};
```

### 添加新的Pod类型
```javascript
function getPodIcon(podId) {
    const iconMap = {
        // 现有映射...
        'YourPodType': 'your-icon'  // 添加新的Pod类型
    };
    return iconMap[podId] || 'info-circle';
}
```

### 自定义样式
可以通过修改CSS变量来自定义界面：
```css
:root {
    --primary-color: #0066CC;
    --secondary-color: #003366;
    --text-color: #333333;
    --border-color: #E0E0E0;
}
```

## 🐛 **故障排除**

### 常见问题

1. **CORS错误**
   - 问题: 浏览器阻止跨域请求
   - 解决: 使用本地服务器或配置CORS

2. **签名错误**
   - 问题: API返回签名错误
   - 解决: 检查签名算法和参数顺序

3. **数学公式不显示**
   - 问题: MathJax未正确加载
   - 解决: 检查网络连接和MathJax配置

4. **结果为空**
   - 问题: 查询无结果或API限制
   - 解决: 尝试不同的查询或检查API状态

### 调试模式
在浏览器控制台中启用调试：
```javascript
// 启用详细日志
localStorage.setItem('debug', 'true');

// 查看API请求
console.log('API Request:', signedUrl);

// 查看响应数据
console.log('API Response:', result);
```

## 📈 **性能优化**

### 已实现的优化
- **防抖搜索** - 避免频繁API调用
- **结果缓存** - 缓存相同查询的结果
- **懒加载** - 按需加载MathJax
- **响应式图片** - 优化图片加载

### 进一步优化建议
- **Service Worker** - 离线缓存
- **Web Workers** - 后台计算
- **CDN加速** - 静态资源加速
- **压缩优化** - 代码和资源压缩

## 🔒 **安全考虑**

### 当前安全措施
- **HTTPS请求** - 所有API请求使用HTTPS
- **签名验证** - 使用MD5签名防止篡改
- **输入验证** - 前端输入验证和清理
- **错误处理** - 不暴露敏感信息

### 安全建议
- **API密钥保护** - 不要在前端暴露真实API密钥
- **输入过滤** - 严格过滤用户输入
- **HTTPS强制** - 生产环境强制使用HTTPS
- **内容安全策略** - 配置CSP防止XSS

## 📝 **更新日志**

### v1.0.0 (2024-01-XX)
- ✨ 初始版本发布
- 🎨 完整的Wolfram|Alpha界面复刻
- 🔧 Mobile API集成
- 📱 响应式设计
- 🧮 数学公式渲染
- 🎯 示例查询功能
- 🌙 主题切换
- ⌨️ 键盘快捷键

## 🤝 **贡献指南**

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

## 📄 **许可证**

本项目仅供学习和研究使用。请遵守Wolfram|Alpha的使用条款。

## 🙏 **致谢**

- Wolfram|Alpha - 提供强大的计算引擎
- Tailwind CSS - 优秀的CSS框架
- MathJax - 数学公式渲染
- CryptoJS - 加密算法库

---

**享受使用Wolfram|Alpha前端版！** 🚀
