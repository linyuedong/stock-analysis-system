# Smart Stock Analyst

智能股票分析与决策辅助系统 - 基于技术指标的量化分析工具

## 功能特性

- 📊 **交互式 K 线图**：使用 TradingView Lightweight Charts
- 📈 **技术指标分析**：MACD, RSI, 均线, 布林带
- 🎯 **智能选股器**：自动扫描并筛选买入信号
- 🌏 **全球市场支持**：美股、A股、港股
- ⚡ **实时分析**：基于 Yahoo Finance 数据

## 技术栈

### 后端
- **FastAPI** - Python 高性能 Web 框架
- **Pandas** - 数据处理
- **Pandas-TA** - 技术指标计算
- **yfinance** - 股票数据获取

### 前端
- **Next.js 14** - React 框架
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式系统
- **Shadcn UI** - UI 组件库
- **Lightweight Charts** - 金融图表

## 本地开发

### 后端启动
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

## 部署指南

详细部署步骤请查看 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 数据源说明

详见 [DATA_SOURCE.md](./DATA_SOURCE.md)

## License

MIT
