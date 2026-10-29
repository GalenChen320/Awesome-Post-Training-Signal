"""Generate README.md and README_zh.md from data/*.json.

Usage: python3 scripts/build_readme.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODULES = [
    {
        "file": "environment_synthesis.json",
        "anchor": "environment-synthesis",
        "title_en": "Environment Synthesis",
        "title_zh": "环境合成（Environment Synthesis）",
        "desc_en": (
            "Works that **automatically or semi-automatically synthesize interactive, verifiable environments** "
            "(state, tools/actions, tasks, rewards/verifiers) for agent RL or trajectory collection. "
            "Hand-built static benchmarks are excluded."
        ),
        "desc_zh": (
            "收录**自动或半自动合成可交互、可验证环境**（状态、工具/动作空间、任务、奖励/验证器）的工作，"
            "环境用于 Agent 强化学习或轨迹采集。纯人工搭建的静态评测集不收录。"
        ),
    },
]

DOMAIN_ZH = {
    "Tool & API": "工具与 API",
    "SWE": "软件工程",
    "Terminal": "终端",
    "Web & GUI": "Web 与 GUI",
    "Game & Embodied": "游戏与具身",
    "Reasoning": "推理谜题",
}

TEXT = {
    "en": {
        "file": "README.md",
        "switch": '<b>English</b> | <a href="README_zh.md">简体中文</a>',
        "tagline": "Where do post-training signals come from?",
        "intro": (
            "LLM post-training mainly consumes three kinds of signals: **demonstrations** (what a good response "
            "looks like), **preferences** (which response is better), and **rewards / verification** (how good an "
            "outcome is). This repository focuses on works about ***how to obtain these signals*** (e.g. tasks, "
            "environments, verifiers, judges); it does not cover works about *how to consume them* (e.g. training "
            "algorithms)."
        ),
        "contents": "Contents",
        "modules": "Modules",
        "header": "| Name | Domain | Date | Links | Summary |",
        "contrib_title": "Contributing",
        "contrib": (
            "Contributions are welcome! Please edit the JSON files under [`data/`](data/) and run "
            "`python3 scripts/build_readme.py` to regenerate both READMEs. See [CONTRIBUTING.md](CONTRIBUTING.md)."
        ),
        "note": "Entries are sorted by first arXiv submission date (newest first).",
        "license_title": "License",
        "license": "[CC0 1.0](LICENSE)",
    },
    "zh": {
        "file": "README_zh.md",
        "switch": '<a href="README.md">English</a> | <b>简体中文</b>',
        "tagline": "后训练的信号从哪里来？",
        "intro": (
            "大语言模型后训练主要消耗三类信号：**示范**（好的回答长什么样）、**偏好**（哪个回答更好）、"
            "**奖励/验证**（结果有多好）。本仓库专注于收录关于***如何获得这些信号***的工作（如任务、环境、"
            "验证器、评判器等）；不收录*如何消费这些信号*的工作（如训练算法等）。"
        ),
        "contents": "目录",
        "modules": "模块",
        "header": "| 名称 | 领域 | 日期 | 链接 | 简介 |",
        "contrib_title": "贡献",
        "contrib": (
            "欢迎贡献！请编辑 [`data/`](data/) 下的 JSON 文件，并运行 `python3 scripts/build_readme.py` "
            "重新生成中英文 README。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。"
        ),
        "note": "条目按 arXiv 首次提交日期倒序排列。",
        "license_title": "许可",
        "license": "[CC0 1.0](LICENSE)",
    },
}


def esc(s: str) -> str:
    return s.replace("|", "\\|")


def row(e: dict, lang: str) -> str:
    name = f"[**{esc(e['name'])}**](https://arxiv.org/abs/{e['arxiv']} \"{esc(e['title'])}\")"
    domain = e["domain"] if lang == "en" else DOMAIN_ZH[e["domain"]]
    links = [f"[![arXiv](https://img.shields.io/badge/arXiv-{e['arxiv'].replace('-', '--')}-b31b1b)](https://arxiv.org/abs/{e['arxiv']})"]
    if e.get("code"):
        links.append(f"[![Code](https://img.shields.io/badge/Code-black?logo=github)]({e['code']})")
    if e.get("data"):
        links.append(f"[![Data](https://img.shields.io/badge/Data-yellow?logo=huggingface)]({e['data']})")
    cells = [name, domain, e["date"], " ".join(links), esc(e[f"summary_{lang}"])]
    return "| " + " | ".join(cells) + " |"


def build(lang: str) -> str:
    t = TEXT[lang]
    total = sum(len(json.loads((ROOT / "data" / m["file"]).read_text(encoding="utf-8"))) for m in MODULES)
    out = [
        '<div align="center">',
        "",
        "<h1>Awesome Post-Training Signal</h1>",
        "",
        f"<p><i>{t['tagline']}</i></p>",
        "",
        '<a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>',
        f'<img src="https://img.shields.io/badge/papers-{total}-blue" alt="Papers">',
        '<a href="LICENSE"><img src="https://img.shields.io/badge/license-CC0%201.0-lightgrey" alt="License"></a>',
        '<a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs Welcome"></a>',
        "",
        f"<p>{t['switch']}</p>",
        "",
        "</div>",
        "",
        t["intro"],
        "",
        f"## {t['contents']}",
        "",
    ]
    for m in MODULES:
        out.append(f"- [{m['title_' + lang]}](#{m['anchor']})")
    out += [f"- [{t['contrib_title']}](#{t['contrib_title'].lower()})", ""]

    for m in MODULES:
        entries = json.loads((ROOT / "data" / m["file"]).read_text(encoding="utf-8"))
        entries.sort(key=lambda e: (e["date"], e["arxiv"]), reverse=True)
        out += [
            f'<a id="{m["anchor"]}"></a>',
            f"## {m['title_' + lang]}",
            "",
            m["desc_" + lang],
            "",
            f"> {t['note']}",
            "",
            t["header"],
            "|---|---|---|---|---|",
        ]
        out += [row(e, lang) for e in entries]
        out.append("")

    out += [f"## {t['contrib_title']}", "", t["contrib"], "", f"## {t['license_title']}", "", t["license"], ""]
    return "\n".join(out)


def main() -> None:
    for lang in ("en", "zh"):
        (ROOT / TEXT[lang]["file"]).write_text(build(lang), encoding="utf-8")
        print("wrote", TEXT[lang]["file"])


if __name__ == "__main__":
    main()
