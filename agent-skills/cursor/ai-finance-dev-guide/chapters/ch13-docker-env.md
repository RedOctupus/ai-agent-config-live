# Chapter 13: 工程环境与部署基础

## Core Idea
用 docker-compose 统一中间件版本，消除「装环境半天」；教学项目不做 K8s 但**必须**能 compose 一键拉起（否则答辩 -20）。

## Frameworks Introduced
- **compose 组件按需**: MySQL+Redis 基础；Milvus/Neo4j 方案确认后再加；Milvus 依赖以可运行仓库配置为准。
- **启动四步**: compose up → ps 健康 → source init.sql → uvicorn。

## Code Examples
```bash
docker-compose up -d
docker-compose ps
mysql -h localhost -u root -p wealth_manager  # source sql/init.sql
uvicorn app.main:app --reload
```

## Key Takeaways
1. 完整 compose 由后端/DB Owner 维护，指南不复制易过期 YAML
2. 演示前在干净机器验证 clone→compose→启动
3. 与需求「范围外：复杂编排」不矛盾 — 简单 compose 属于必做

## Connects To
- **Ch 7.8**: T-3 环境验收
- **Ch 9**: DoD docker-compose
