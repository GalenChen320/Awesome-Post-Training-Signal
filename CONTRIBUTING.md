# Contributing

Thanks for helping improve **Awesome Post-Training Signal**!

## How to add an entry

1. Find the module file under [`data/`](data/) (e.g. `data/environment_synthesis.json`).
2. Append an object with the following fields:

```json
{
  "name": "ShortName",
  "title": "Full Paper Title",
  "arxiv": "2601.05808",
  "date": "2026-01",
  "domain": "Tool & API",
  "affiliations": ["Univ A", "Company B", "Univ C"],
  "code": "https://github.com/...",
  "data": "https://huggingface.co/...",
  "summary_en": "One sentence (<= 25 words) on how the data/environment is built.",
  "summary_zh": "对应的一句话中文简介。"
}
```

   - `date`: month of the **first** arXiv version (`YYYY-MM`).
   - `domain`:
     - Environment Synthesis: `Tool & API`, `SWE`, `Terminal`, `Web & GUI`, `Game & Embodied`, `Reasoning`
     - Verifiable Rewards: `Math`, `Science`, `General Reasoning`, `Code`, `Formal Proof`, `Instruction Following`, `Verifier`
   - `affiliations`: up to **three** distinct affiliations in author order (main page column).
   - Leave `code`, `data` as `""` if unavailable.
3. Regenerate all pages (do **not** edit `README*.md` / `topics/*.md` by hand):

```bash
python3 scripts/build_readme.py
```

4. Open a pull request.

## Inclusion criteria (Environment Synthesis)

- The work **automatically or semi-automatically constructs interactive, verifiable environments** (state, tools/actions, tasks, rewards/verifiers).
- The environments are used for **agent training** (RL or trajectory collection), not only evaluation.
- Purely hand-built static benchmarks and trajectory-only synthesis on existing environments are out of scope.

## Inclusion criteria (Verifiable Rewards)

- Rewards are **checked automatically by programs, rules or formal systems** (answer matching, unit tests, proof checkers, constraint checkers).
- Includes verifiable training datasets, methods that synthesize answers / tests / checkers, and verifier design.
- Learned reward models, LLM judges, rubrics, pure benchmarks and pure RL algorithms are out of scope.

---

# 贡献指南

1. 在 [`data/`](data/) 下找到对应模块的 JSON 文件，按上方字段格式追加条目（`date` 为 arXiv 首版月份，缺失的 `code`/`data` 留空字符串）。
2. 运行 `python3 scripts/build_readme.py` 重新生成主页与各主题子页面，**不要**手动修改 README 与 topics/ 下的文件；`affiliations` 按作者顺序至多填三个单位。
3. 提交 Pull Request。

**可验证奖励模块收录标准**：奖励由程序、规则或形式系统自动校验（答案匹配、单元测试、证明检查、约束检查）；收录可验证训练数据、合成答案/测试/检查器的方法及验证器设计；不收奖励模型、LLM 评判、rubric、纯评测集与纯 RL 算法。

**环境合成模块收录标准**：自动/半自动构建可交互、可验证的环境，且用于 Agent 训练（RL 或轨迹采集）；纯人工静态评测集、仅在现有环境上合成轨迹的工作不收录。
