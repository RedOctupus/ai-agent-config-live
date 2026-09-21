# CI/CD：把 OCR 部署到 GitHub Actions

本 skill **不含** 审查引擎，也 **不要** 把 workflow YAML 写死在这里。GitHub / GitLab / Gerrit 怎么接，以上游**当前**文档为准。

## 何时读本文件

用户要：PR 自动审查、GitHub Actions、CI/CD、把 OCR 部署到 GitHub、fork PR 也能审、评论 `/open-code-review` 再审。

**不要**为此走本机 Gate / `ocr review`，除非用户同时要在本机审一份。CI 路径需要 **OCR 自己的 LLM secrets**，不是 Cursor 委托模式。

## 能力（显式）

上游提供可复用 Composite Action：在目标仓库 workflow 里 `uses: alibaba/open-code-review@<ref>`。Action 装 CLI、对 PR diff 跑 `ocr review`、用 Pull Request Review API 发行内评论 + 摘要。

- 自动：`pull_request_target` 的 opened / synchronize / reopened
- 按需：PR 评论 `/open-code-review` 或 `@open-code-review`
- 官方还列了 GitLab CI、GitFlic CI、Gerrit（细节只在上游 CI/CD 页，本文件不展开）

## 有需要时按这个顺序读上游

不要凭记忆拼 workflow。站点路径若 404，跳到 GitHub 文件，不要猜输入名。

1. 官方 CI/CD 总览：https://open-codereview.ai/docs/cicd
2. GitHub Actions 接到自己的仓库（拷贝示例、secrets/vars、self-hosted、钉版本）：  
   https://github.com/alibaba/open-code-review/blob/main/examples/github_actions/README.md
3. 可复制的 workflow：  
   https://github.com/alibaba/open-code-review/blob/main/examples/github_actions/ocr-review.yml
4. Action 输入 / 输出 / 安全说明（完整清单只在这里）：  
   https://github.com/alibaba/open-code-review/blob/main/action.yml
5. 上游自己怎么跑（self-hosted + `uses: ./`，**别抄 `uses: ./` 到别人仓库**）：  
   https://github.com/alibaba/open-code-review/blob/main/.github/workflows/ocr-review.yml

读完再写 `.github/workflows/`。生产钉 **Action commit SHA + `ocr_version`**，不要长期 `@main` + `latest`。

## 硬约束

- 禁止把 LLM token 写进仓库 / skill。Secrets：`OCR_LLM_URL`、`OCR_LLM_AUTH_TOKEN`；模型可用 vars。
- 外部仓库必须 `uses: alibaba/open-code-review@<sha-or-tag>`，不要 `uses: ./`（那是上游仓内部捷径）。
- `pull_request_target` 能拿到 fork 的 secrets；官方说明 OCR 只读 diff、不执行 PR 代码。改权限或加「checkout 再执行 PR 代码」之前，先再读 `action.yml` 安全段。
