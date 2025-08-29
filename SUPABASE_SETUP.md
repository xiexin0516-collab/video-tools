# Supabase 配置指南

## 🚀 快速配置步骤

### 1. 访问Supabase项目

1. 打开 [Supabase Dashboard](https://supabase.com/dashboard/org/vacsvoxdoqtxelrmfdpc)
2. 选择您的项目（如果没有项目，请创建一个新项目）

### 2. 配置数据库

1. 在左侧菜单中点击 **SQL Editor**
2. 复制 `supabase-setup.sql` 文件中的内容
3. 粘贴到SQL Editor中并执行

### 3. 配置存储

1. 在左侧菜单中点击 **Storage**
2. 点击 **Create bucket**
3. 输入名称：`vidtools`
4. 选择 **Private**（私有）
5. 点击 **Create bucket**

### 4. 配置认证

1. 在左侧菜单中点击 **Authentication** > **Settings**
2. 在 **Site URL** 中输入：`https://vidtools.tools`
3. 在 **Redirect URLs** 中添加：`https://vidtools.tools/auth/callback`
4. 启用 **Email** 认证
5. 保存设置

### 5. 获取API密钥

1. 在左侧菜单中点击 **Settings** > **API**
2. 记录以下信息：
   - **Project URL** (例如：`https://your-project.supabase.co`)
   - **anon public** (公开密钥)
   - **service_role secret** (服务角色密钥)

### 6. 更新前端配置

在 `frontend/js/supabaseClient.js` 中更新：

```javascript
const SUPABASE_URL = 'https://your-project.supabase.co'
const SUPABASE_ANON_KEY = 'your-anon-key'
```

### 7. 更新后端环境变量

在 `backend/.env` 中配置：

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE=your-service-role-key
SUPABASE_JWKS_URL=https://your-project.supabase.co/auth/v1/jwks
```

## 🔧 详细配置说明

### 数据库表结构

- **projects表**: 存储用户的项目信息
- **行级安全**: 确保用户只能访问自己的数据
- **自动时间戳**: 自动记录创建和更新时间

### 存储配置

- **私有bucket**: 确保文件安全
- **访问策略**: 用户只能访问自己的文件
- **支持格式**: 音频、视频、字幕文件

### 认证配置

- **邮箱认证**: 支持邮箱注册和登录
- **回调URL**: 处理认证后的重定向
- **JWT令牌**: 用于API认证

## 🐛 常见问题

### 1. 数据库连接失败
- 检查Project URL是否正确
- 确认网络连接正常
- 验证API密钥是否有效

### 2. 文件上传失败
- 确认Storage bucket已创建
- 检查存储策略是否正确
- 验证文件大小是否超限

### 3. 认证失败
- 检查Site URL和Redirect URLs配置
- 确认邮箱认证已启用
- 验证JWT令牌是否有效

## 📞 获取帮助

如果遇到问题：
1. 查看 [Supabase文档](https://supabase.com/docs)
2. 检查项目日志
3. 联系技术支持
