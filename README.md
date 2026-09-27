# 19-curtainlen（窗帘用布）

Curtainlen — 成品宽×褶倍率 + 上下边折；换算布长米数

## 启动

```bash
docker compose up --build
```

| 入口 | 地址 |
| --- | --- |
| 前端 | http://localhost:4800 |
| API | http://localhost:9800 |

## 主链

窗宽层高+褶量 → 布长 → 窗户示意

## 空间曝晒类型

- 普通室内：订货米 = 基础米
- 户外抗紫外：订货米 = 基础米 + 固定加米（设置页可配，可停用；停用后新测算回到基础口径）

类型枚举与加米规则在后端 `app/modules/exposure/`，前端经 `GET /api/exposure/types` 取目录；落库快照钉住类型与订货米，事后改默认加米不重算旧编号。

## 技术栈

Python 3.12 + FastAPI + SQLite；Vue 3 + Vite + Nginx。
