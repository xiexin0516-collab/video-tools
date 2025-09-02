# vidtools.tools 下载统计系统使用说明

## 🎯 系统概述

这个下载统计系统为你的网站 vidtools.tools 提供了完整的下载次数跟踪功能，包括：

- **实时下载计数**：在网站首页显示当前下载次数
- **Google Analytics 集成**：专业的网站访问和下载行为分析
- **GitHub 统计同步**：自动从 GitHub Releases 获取下载数据
- **本地统计记录**：记录每次下载的详细信息
- **管理后台**：查看详细的统计数据和导出报告

## 🚀 快速开始

### 1. 配置 Google Analytics

1. 访问 [Google Analytics](https://analytics.google.com/)
2. 创建新的数据流，选择网站类型
3. 输入你的域名：`vidtools.tools`
4. 获取测量 ID（格式：G-XXXXXXXXXX）
5. 将测量 ID 替换到 `docs/index.html` 中的 Google Analytics 代码

### 2. 部署到你的网站

将以下文件部署到你的网站：

```
docs/
├── index.html              # 主页面（已集成统计代码）
├── js/
│   └── download-stats.js   # 下载统计核心功能
└── admin/
    └── stats.html          # 统计管理后台
```

### 3. 访问统计后台

访问 `https://vidtools.tools/admin/stats.html` 查看详细统计信息。

## 📊 功能特性

### 实时统计显示
- 在网站首页显示当前下载次数
- 自动格式化数字（K、M 单位）
- 美观的渐变样式和动画效果

### 多平台统计
- 自动识别下载平台（Windows、Mac、Linux）
- 记录用户代理信息
- 按平台分类统计下载次数

### 数据同步
- 自动从 GitHub API 获取官方下载统计
- 本地记录每次下载事件
- 定期同步更新（每5分钟）

### 管理功能
- 实时查看下载统计
- 导出统计数据为 JSON 格式
- 清除本地缓存数据
- 手动刷新统计数据

## 🔧 技术实现

### 核心组件

1. **DownloadStats 类**：管理所有统计功能
2. **GitHub API 集成**：获取官方下载数据
3. **本地存储**：使用 localStorage 保存统计信息
4. **Google Analytics**：发送下载事件到 GA4

### 数据流程

```
用户下载 → 记录本地统计 → 发送 GA 事件 → 更新显示 → 同步 GitHub 数据
```

### 存储结构

```json
{
  "totalDownloads": 1234,
  "lastUpdated": "2024-01-01T00:00:00.000Z",
  "downloadHistory": [
    {
      "tool": "ManualSubtitleEditor",
      "platform": "windows",
      "timestamp": "2024-01-01T00:00:00.000Z",
      "userAgent": "Mozilla/5.0..."
    }
  ]
}
```

## 📈 查看统计数据

### 方式1：Google Analytics
1. 登录 Google Analytics 账号
2. 选择你的网站数据流
3. 在"事件"报告中查看下载事件
4. 可以按工具名称、平台等维度分析

### 方式2：统计管理后台
1. 访问 `/admin/stats.html`
2. 查看实时统计概览
3. 分析平台分布情况
4. 查看最近下载记录

### 方式3：GitHub Releases
1. 访问你的 GitHub 仓库
2. 查看 Releases 页面
3. 每个版本都会显示下载次数

## 🛠️ 自定义配置

### 修改统计更新频率

在 `download-stats.js` 中修改：

```javascript
// 每5分钟更新一次统计
setInterval(() => {
    this.fetchGitHubStats();
}, 5 * 60 * 1000); // 修改这个数值
```

### 添加新的统计维度

在 `recordLocalDownload` 方法中添加：

```javascript
const downloadEvent = {
    tool: toolName,
    platform: platform,
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    // 添加新的字段
    country: getUserCountry(),
    referrer: document.referrer
};
```

### 自定义显示样式

在 `docs/index.html` 中修改 CSS 类：

```css
.download-counter {
    background: linear-gradient(135deg, #your-color 0%, #your-color 100%);
    /* 自定义样式 */
}
```

## 🔍 故障排除

### 常见问题

1. **统计不显示**
   - 检查 JavaScript 控制台是否有错误
   - 确认 `download-stats.js` 文件已正确加载
   - 验证 HTML 元素 ID 是否正确

2. **GitHub 数据同步失败**
   - 检查网络连接
   - 确认 GitHub API 访问正常
   - 查看控制台错误信息

3. **Google Analytics 不工作**
   - 验证测量 ID 是否正确
   - 检查 gtag 代码是否正确加载
   - 使用 GA 调试工具验证

### 调试模式

在浏览器控制台中：

```javascript
// 查看统计对象
console.log(window.downloadStats);

// 手动触发统计更新
window.downloadStats.fetchGitHubStats();

// 查看统计摘要
console.log(window.downloadStats.getStatsSummary());
```

## 📱 移动端支持

系统完全支持移动端设备：

- 响应式设计，适配各种屏幕尺寸
- 触摸友好的操作界面
- 移动端优化的统计显示

## 🔒 隐私保护

- 不收集个人身份信息
- 只记录必要的技术数据
- 符合 GDPR 和隐私法规要求
- 用户可以清除本地数据

## 📞 技术支持

如果你在使用过程中遇到问题：

1. 检查浏览器控制台的错误信息
2. 确认所有文件都已正确部署
3. 验证网络连接和 API 访问权限
4. 查看本文档的故障排除部分

## 🎉 开始使用

现在你的网站已经具备了完整的下载统计功能！

1. 用户每次下载都会自动记录
2. 统计数据实时显示在首页
3. 可以通过管理后台查看详细分析
4. Google Analytics 提供专业的用户行为分析

享受你的新统计系统吧！ 🚀
