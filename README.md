# OCR Desktop - 本地化 OCR 桌面应用

基于 Tauri + React + FastAPI + PaddleOCR 的跨平台 OCR 桌面应用，支持中文/英文文档识别，具备自学习能力。

## 项目架构

```
code/
├── src-tauri/          # Tauri 桌面应用 (Rust)
│   ├── src/
│   │   └── main.rs    # Rust 主程序
│   ├── Cargo.toml     # Rust 依赖
│   └── tauri.conf.json # Tauri 配置
├── src/               # React 前端
│   ├── App.tsx        # 主应用组件
│   ├── App.css        # 应用样式
│   ├── main.tsx       # 入口文件
│   └── styles.css     # 全局样式
├── python-api/        # Python FastAPI 后端
│   ├── main.py        # API 服务
│   └── requirements.txt # Python 依赖
├── tests/             # 测试文件
│   └── test_api.py    # API 测试
├── models/            # OCR 模型目录
├── docs/              # 文档
└── PLAN.md            # 项目规划
```

## 技术栈

- **前端**: Tauri 2 + React + TypeScript
- **后端**: Python FastAPI
- **OCR 引擎**: PaddleOCR (PP-OCRv5 + PP-StructureV3)
- **支持平台**: Windows, macOS, Linux

## 功能特性

### 核心功能
- 📄 支持图片、PDF、截图识别
- 📝 支持导出 docx、xlsx、txt、md
- 🎯 双层模型架构 (Lite + Pro)
- 💻 完全本地运行，无需联网

### 自学习能力
- 🧠 用户纠错记忆
- 📊 版式模板学习
- 📚 领域词典构建
- 🔄 自适应引擎策略

## 快速开始

### 环境要求
- Node.js 18+
- Python 3.9+
- Rust 1.70+

### 安装依赖

```bash
# 安装 Node 依赖
npm install

# 安装 Python 依赖
pip install -r python-api/requirements.txt

# 安装 Tauri CLI
npm install -g @tauri-apps/cli
```

### 开发模式

```bash
# 启动 Python 后端
cd python-api
python main.py

# 启动 Tauri 开发模式
npm run tauri dev
```

### 构建

```bash
# 构建桌面应用
npm run tauri build
```

## API 接口

### 健康检查
```
GET /health
```

### 文档识别
```
POST /recognize
Content-Type: application/json

{
  "file_path": "/path/to/document.pdf",
  "language": "ch",
  "performance_mode": "lite",
  "export_formats": ["txt", "md"]
}
```

### 文件上传识别
```
POST /recognize/upload
Content-Type: multipart/form-data

file: <binary>
language: ch
performance_mode: lite
```

### 提交反馈
```
POST /feedback
Content-Type: application/json

{
  "document_id": "doc_xxx",
  "page_number": 1,
  "original_text": "OCR结果",
  "corrected_text": "修正结果",
  "allow_training": true
}
```

## 测试

```bash
# 运行 API 测试
cd python-api
pytest ../tests/test_api.py -v
```

## 项目规划

详见 [PLAN.md](PLAN.md)

## 许可证

MIT License
