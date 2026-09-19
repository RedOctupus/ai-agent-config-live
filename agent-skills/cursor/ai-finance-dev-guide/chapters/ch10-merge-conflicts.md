# Chapter 10: 合并时常见冲突及解法

## Core Idea
冲突是 Git 无法自动合并，非「代码坏了」；按**文件 Owner** 协调，保留双方合理变更，解决后重跑测试。

## Frameworks Introduced
- **冲突场景表**: requirements 合并排序；API/模型由负责人统一；`.env` 不进 Git 只 `.env.example`。
- **黄金法则**: 不确定找 Owner；不为消冲突删功能；解决后全量自测。

## Code Examples
```bash
git status
# 编辑 <<<<<<< ======= >>>>>>> 区块
git add <file>
git commit -m "fix: 解决xxx冲突"
```

## Key Takeaways
1. 非自己模块的冲突先找负责人
2. 依赖冲突保留双方包名并排序
3. 合并后 pytest + 冒烟接口

## Connects To
- **Ch 4**: 公共能力 Owner
- **Ch 6**: PR 流程
