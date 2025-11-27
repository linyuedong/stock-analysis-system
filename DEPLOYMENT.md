# 部署指南：Smart Stock Analyst

本文档提供多种部署方案，让您的股票分析系统可以在互联网上公开访问。

---

## 🚀 方案一：Vercel + Render（推荐，免费）

**适合**：个人项目、原型演示
**成本**：完全免费（有额度限制）

### 步骤 1：部署后端到 Render

1. **准备代码**
   ```bash
   cd stock-analysis-system/backend
   ```

2. **创建 `render.yaml`**（在 backend 目录）
   ```yaml
   services:
     - type: web
       name: stock-analysis-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **部署到 Render**
   - 访问 https://render.com 并注册
   - 点击 "New" → "Web Service"
   - 连接您的 GitHub 仓库（需先推送代码到 GitHub）
   - 选择 `backend` 目录
   - Render 会自动部署，完成后会给您一个 URL，如：`https://your-app.onrender.com`

### 步骤 2：部署前端到 Vercel

1. **修改前端 API 配置**
   编辑 `frontend/src/lib/api.ts`：
   ```typescript
   const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://your-app.onrender.com/api';
   ```

2. **部署到 Vercel**
   ```bash
   cd stock-analysis-system/frontend
   npm install -g vercel
   vercel
   ```
   - 按提示登录或注册 Vercel
   - 选择项目目录
   - 设置环境变量：`NEXT_PUBLIC_API_URL=https://your-app.onrender.com/api`
   - 部署完成后会得到一个 URL，如：`https://your-app.vercel.app`

3. **更新后端 CORS**
   编辑 `backend/main.py`：
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:3000",
           "https://your-app.vercel.app"  # 添加您的 Vercel 域名
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

---

## 🐳 方案二：Docker 容器化部署

**适合**：拥有 VPS 或云服务器
**成本**：取决于服务器价格

### 1. 创建 Dockerfile（后端）

在 `backend/` 目录创建 `Dockerfile`：
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. 创建 Dockerfile（前端）

在 `frontend/` 目录创建 `Dockerfile`：
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ENV NEXT_PUBLIC_API_URL=http://your-server-ip:8000/api

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

### 3. 使用 Docker Compose

在项目根目录创建 `docker-compose.yml`：
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api
    depends_on:
      - backend
    restart: unless-stopped
```

### 4. 部署到服务器

```bash
# 在服务器上
git clone <your-repo>
cd stock-analysis-system
docker-compose up -d
```

---

## ☁️ 方案三：云平台一键部署

### Railway（推荐）

1. 访问 https://railway.app
2. 连接 GitHub 仓库
3. 分别部署前后端：
   - Backend: 选择 Python 环境，设置启动命令
   - Frontend: 选择 Node.js 环境

### Heroku

1. 安装 Heroku CLI
2. 部署后端：
   ```bash
   cd backend
   heroku create stock-analysis-api
   git push heroku main
   ```

---

## 🔒 安全建议

### 1. 环境变量管理
不要在代码中硬编码敏感信息，使用环境变量：

**后端 `.env`**：
```env
CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

**前端 `.env.production`**：
```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.onrender.com/api
```

### 2. 启用 HTTPS
大多数现代部署平台（Vercel, Render, Railway）会自动提供 SSL 证书。

### 3. 添加访问限制
如果担心 API 被滥用，可以添加：
- API Key 认证
- 速率限制（Rate Limiting）
- IP 白名单

---

## 📝 部署检查清单

- [ ] 后端 API 已部署并可访问
- [ ] 前端已配置正确的 API URL
- [ ] CORS 设置包含前端域名
- [ ] 环境变量已正确配置
- [ ] HTTPS 已启用
- [ ] 测试所有功能（搜索、选股器、图表）

---

## 🆘 常见问题

**Q: Render 免费版会休眠吗？**
A: 是的，15分钟无访问会自动休眠，下次访问需要 30 秒唤醒。

**Q: 如何绑定自定义域名？**
A: Vercel 和 Render 都支持自定义域名，在控制台的 Settings → Domains 添加即可。

**Q: 数据会丢失吗？**
A: 当前系统不存储数据，所有数据实时从 Yahoo Finance 获取。

---

## 🎯 下一步优化

1. **添加数据缓存**：使用 Redis 缓存股票数据，减少 API 调用
2. **用户系统**：添加登录功能，保存自选股
3. **监控告警**：使用 Sentry 监控错误，Uptime Robot 监控服务状态
4. **CDN 加速**：Vercel 自带 CDN，可进一步优化图片和静态资源

需要帮助具体实施某个方案吗？
