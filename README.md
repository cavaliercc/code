# OCR Local Platform (Scaffold)

根据 `PLAN.md` 生成的首版后端代码骨架，重点实现：

- FastAPI 服务入口
- `RecognizeRequest/RecognizeResult` 等核心接口模型
- Lite/Pro 路由决策（含升级触发）
- 导出层接口（txt/md/docx/xlsx 占位实现）
- 反馈学习与学习任务入口（内存存储占位）

## Run

```bash
python -m pip install -e .[dev]
uvicorn app.main:app --reload
```

## Test

```bash
pytest
```
