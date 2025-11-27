# 逐步部署指南 - Vercel + Render 方案

本指南将手把手教您部署到免费的云平台。

---

## 📋 准备工作

### 1. 注册账号
- [ ] 注册 GitHub 账号：https://github.com
- [ ] 注册 Render 账号：https://render.com（用 GitHub 登录）
- [ ] 注册 Vercel 账号：https://vercel.com（用 GitHub 登录）

### 2. 准备代码
确保您的代码在本地能正常运行。

---

## 🚀 第一步：推送代码到 GitHub

### 1.1 初始化 Git 仓库
```bash
cd /Users/ydlin/.gemini/antigravity/scratch/stock-analysis-system
git init
git add .
git commit -m "Initial commit: Smart Stock Analyst"
```

### 1.2 创建 GitHub 仓库
1. 访问 https://github.com/new
2. 仓库名称：`stock-analysis-system`
3. 设置为 Public（公开）或 Private（私有）
4. **不要**勾选 "Add a README file"
5. 点击 "Create repository"

### 1.3 推送代码
在终端执行（替换 `YOUR_USERNAME` 为您的 GitHub 用户名）：
```bash
git remote add origin https://github.com/YOUR_USERNAME/stock-analysis-system.git
git branch -M main
git push -u origin main
```

---

## 🐍 第二步：部署后端到 Render

### 2.1 创建 Web Service
1. 访问 https://dashboard.render.com
2. 点击 **"New +"** → **"Web Service"**
3. 选择 **"Build and deploy from a Git repository"**
4. 点击 **"Connect account"** 连接您的 GitHub
5. 找到并选择 `stock-analysis-system` 仓库
6. 点击 **"Connect"**

### 2.2 配置服务
填写以下信息：

| 字段 | 值 |
|------|-----|
| **Name** | `stock-analysis-api` |
| **Region** | Singapore（或离您最近的） |
| **Root Directory** | `backend` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### 2.3 环境变量（可选）
在 "Environment Variables" 区域，暂时不需要添加。

### 2.4 部署
1. 点击 **"Create Web Service"**
2. 等待 5-10 分钟，Render 会自动构建和部署
3. 部署成功后，您会看到一个 URL，例如：
   ```
   https://stock-analysis-api.onrender.com
   ```
4. **记录这个 URL**，后面会用到！

### 2.5 验证后端
访问：`https://stock-analysis-api.onrender.com/health`

应该看到：`{"status": "ok"}`

---

## ⚛️ 第三步：部署前端到 Vercel

### 3.1 安装 Vercel CLI（任选一种方式）

**方式 A：使用 npx（推荐）**
无需安装，直接使用：
```bash
cd frontend
npx vercel
```

**方式 B：全局安装**
```bash
npm install -g vercel
cd frontend
vercel
```

### 3.2 首次登录
```bash
npx vercel login
```
- 选择登录方式（推荐：GitHub）
- 在浏览器中完成授权

### 3.3 部署
在 `frontend` 目录执行：
```bash
npx vercel
```

交互式问答：
```
? Set up and deploy "~/stock-analysis-system/frontend"? [Y/n] y
? Which scope do you want to deploy to? <YOUR_USERNAME>
? Link to existing project? [y/N] n
? What's your project's name? stock-analyzer
? In which directory is your code located? ./
? Want to override the settings? [y/N] n
```

### 3.4 配置环境变量
部署完成后，需要设置 API URL：

```bash
npx vercel env add NEXT_PUBLIC_API_URL
```

提示输入值时，输入（替换为您的 Render URL）：
```
https://stock-analysis-api.onrender.com/api
```

选择环境：
```
? Add NEXT_PUBLIC_API_URL to which Environments? 
  ◉ Production
  ◉ Preview
  ◉ Development
```

### 3.5 重新部署（应用环境变量）
```bash
npx vercel --prod
```

部署成功后会得到一个 URL，例如：
```
https://stock-analyzer.vercel.app
```

---

## 🔧 第四步：配置 CORS

### 4.1 更新后端 CORS 设置
编辑 `backend/main.py`：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://stock-analyzer.vercel.app"  # 替换为您的 Vercel 域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4.2 推送更新
```bash
git add .
git commit -m "Update CORS for production"
git push
```

Render 会自动检测到更新并重新部署（约 3-5 分钟）。

---

## ✅ 第五步：验证部署

### 5.1 测试前端
访问您的 Vercel URL：`https://stock-analyzer.vercel.app`

### 5.2 测试功能
- [ ] 搜索股票（如 `AAPL`）
- [ ] 查看 K 线图和指标
- [ ] 点击 "Open Smart Screener"
- [ ] 查看选股结果

---

## 🎉 完成！

您的股票分析系统现在已经上线了！

- **前端地址**：https://stock-analyzer.vercel.app
- **后端 API**：https://stock-analysis-api.onrender.com

---

## ⚠️ 常见问题

### Q1: Render 部署失败
**检查**：
- `backend/requirements.txt` 是否正确
- Python 版本是否为 3.9+
- 查看 Render 控制台的日志

### Q2: 前端无法连接后端
**检查**：
1. 环境变量 `NEXT_PUBLIC_API_URL` 是否设置正确
2. 后端 CORS 是否包含前端域名
3. 在浏览器控制台查看错误信息

### Q3: Render 免费版休眠
Render 免费版会在 15 分钟无访问后休眠，下次访问需要 30 秒唤醒。

**解决方案**：
- 使用 UptimeRobot 每 5 分钟 ping 一次
- 升级到付费版（$7/月）

### Q4: 如何更新代码
```bash
git add .
git commit -m "Update: 说明"
git push
```
Render 和 Vercel 会自动重新部署。

---

## 📝 后续优化

1. **自定义域名**：
   - Vercel: Settings → Domains
   - Render: Settings → Custom Domain

2. **监控和日志**：
   - 使用 Sentry 监控错误
   - Render 和 Vercel 控制台都有日志

3. **性能优化**：
   - 添加 Redis 缓存（需付费）
   - 使用 CDN 加速静态资源

需要帮助吗？随时联系！
