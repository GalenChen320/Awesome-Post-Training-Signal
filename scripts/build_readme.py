"""Generate README.md / README_zh.md, per-topic pages (topics/*.md) and the website (docs/index.html)
from data/*.json.

Usage: python3 scripts/build_readme.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODULES = [
    {
        "file": "environment_synthesis.json",
        "slug": "environment-synthesis",
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
        "suffix": "",
        "other_suffix": "_zh",
        "switch": '<b>English</b> | <a href="{other}">简体中文</a>',
        "tagline": "Where do post-training signals come from?",
        "intro": (
            "LLM post-training mainly consumes three kinds of signals: **demonstrations** (what a good response "
            "looks like), **preferences** (which response is better), and **rewards / verification** (how good an "
            "outcome is). This repository focuses on works about ***how to obtain these signals*** (e.g. tasks, "
            "environments, verifiers, judges); it does not cover works about *how to consume them* (e.g. training "
            "algorithms)."
        ),
        "contents": "Contents",
        "cols_main": ["Name", "Domain", "Date", "Affiliations", "Links"],
        "cols_topic": ["Name", "Domain", "Date", "Affiliations", "Links", "Summary"],
        "detail": "Full list with summaries",
        "back": "Back to main page",
        "contrib_title": "Contributing",
        "contrib": (
            "Contributions are welcome! Please edit the JSON files under [`data/`](data/) and run "
            "`python3 scripts/build_readme.py` to regenerate all pages. See [CONTRIBUTING.md](CONTRIBUTING.md)."
        ),
        "note": "Entries are sorted by first arXiv submission date (newest first). Up to three affiliations are listed per paper.",
        "license_title": "License",
        "license": "[CC0 1.0](LICENSE)",
    },
    "zh": {
        "suffix": "_zh",
        "other_suffix": "",
        "switch": '<a href="{other}">English</a> | <b>简体中文</b>',
        "tagline": "后训练的信号从哪里来？",
        "intro": (
            "大语言模型后训练主要消耗三类信号：**示范**（好的回答长什么样）、**偏好**（哪个回答更好）、"
            "**奖励/验证**（结果有多好）。本仓库专注于收录关于***如何获得这些信号***的工作（如任务、环境、"
            "验证器、评判器等）；不收录*如何消费这些信号*的工作（如训练算法等）。"
        ),
        "contents": "目录",
        "cols_main": ["名称", "领域", "日期", "单位", "链接"],
        "cols_topic": ["名称", "领域", "日期", "单位", "链接", "简介"],
        "detail": "查看含简介的完整列表",
        "back": "返回主页",
        "contrib_title": "贡献",
        "contrib": (
            "欢迎贡献！请编辑 [`data/`](data/) 下的 JSON 文件，并运行 `python3 scripts/build_readme.py` "
            "重新生成所有页面。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。"
        ),
        "note": "条目按 arXiv 首次提交日期倒序排列；每篇论文至多列出前三个单位。",
        "license_title": "许可",
        "license": "[CC0 1.0](LICENSE)",
    },
}


def esc(s: str) -> str:
    return s.replace("|", "\\|")


def load(m: dict) -> list:
    entries = json.loads((ROOT / "data" / m["file"]).read_text(encoding="utf-8"))
    entries.sort(key=lambda e: (e["date"], e["arxiv"]), reverse=True)
    return entries


def row(e: dict, lang: str, with_summary: bool) -> str:
    name = f"[**{esc(e['name'])}**](https://arxiv.org/abs/{e['arxiv']} \"{esc(e['title'])}\")"
    domain = e["domain"] if lang == "en" else DOMAIN_ZH[e["domain"]]
    affs = "<br>".join(esc(a) for a in e.get("affiliations", [])[:3]) or "-"
    links = [f"[![arXiv](https://img.shields.io/badge/arXiv-{e['arxiv']}-b31b1b)](https://arxiv.org/abs/{e['arxiv']})"]
    if e.get("code"):
        links.append(f"[![Code](https://img.shields.io/badge/Code-black?logo=github)]({e['code']})")
    if e.get("data"):
        links.append(f"[![Data](https://img.shields.io/badge/Data-yellow?logo=huggingface)]({e['data']})")
    cells = [name, domain, e["date"], affs, " ".join(links)]
    if with_summary:
        cells.append(esc(e[f"summary_{lang}"]))
    return "| " + " | ".join(cells) + " |"


def table(entries: list, lang: str, with_summary: bool) -> list:
    cols = TEXT[lang]["cols_topic" if with_summary else "cols_main"]
    return ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)] + [row(e, lang, with_summary) for e in entries]


def topic_path(m: dict, lang: str) -> str:
    return f"topics/{m['slug']}{TEXT[lang]['suffix']}.md"


def header(lang: str, other_href: str, prefix: str, total: int) -> list:
    t = TEXT[lang]
    return [
        '<div align="center">',
        "",
        "<h1>Awesome Post-Training Signal</h1>",
        "",
        f"<p><i>{t['tagline']}</i></p>",
        "",
        '<a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>',
        f'<img src="https://img.shields.io/badge/papers-{total}-blue" alt="Papers">',
        f'<a href="{prefix}LICENSE"><img src="https://img.shields.io/badge/license-CC0%201.0-lightgrey" alt="License"></a>',
        f'<a href="{prefix}CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs Welcome"></a>',
        "",
        f"<p>{t['switch'].format(other=other_href)}</p>",
        "",
        "</div>",
        "",
    ]


def build_main(lang: str, data: dict) -> str:
    t = TEXT[lang]
    total = sum(len(v) for v in data.values())
    out = header(lang, f"README{t['other_suffix']}.md", "", total)
    out += [t["intro"], "", f"## {t['contents']}", ""]
    for m in MODULES:
        out.append(f"- [{m['title_' + lang]}](#{m['slug']})")
    out += [f"- [{t['contrib_title']}](#{t['contrib_title'].lower()})", ""]

    for m in MODULES:
        out += [
            f'<a id="{m["slug"]}"></a>',
            f"## {m['title_' + lang]}",
            "",
            m["desc_" + lang],
            "",
            f"> {t['note']} **[{t['detail']} →]({topic_path(m, lang)})**",
            "",
        ]
        out += table(data[m["slug"]], lang, with_summary=False)
        out.append("")

    out += [f"## {t['contrib_title']}", "", t["contrib"], "", f"## {t['license_title']}", "", t["license"], ""]
    return "\n".join(out)


def build_topic(m: dict, lang: str, entries: list) -> str:
    t = TEXT[lang]
    other = Path(topic_path(m, "zh" if lang == "en" else "en")).name
    out = header(lang, other, "../", len(entries))
    out += [
        f"## {m['title_' + lang]}",
        "",
        f"[← {t['back']}](../README{t['suffix']}.md)",
        "",
        m["desc_" + lang],
        "",
        f"> {t['note']}",
        "",
    ]
    out += table(entries, lang, with_summary=True)
    out.append("")
    return "\n".join(out)


def md_inline(s: str) -> str:
    """Tiny Markdown-to-HTML for intro/description text (bold, italic, links, code)."""
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


SITE_TEXT = {
    "en": {
        "search": "Search name, title, affiliation, summary ...",
        "all": "All",
        "none": "No matching papers.",
        "showing": "Showing {n} / {m} papers",
        "aff": "Affiliations (up to three)",
        "footer": "Generated from [`data/`](https://github.com/GalenChen320/Awesome-Post-Training-Signal/tree/main/data). "
                  "Contributions welcome on [GitHub](https://github.com/GalenChen320/Awesome-Post-Training-Signal). License: CC0 1.0.",
    },
    "zh": {
        "search": "搜索名称、标题、单位、简介……",
        "all": "全部",
        "none": "没有匹配的论文。",
        "showing": "显示 {n} / {m} 篇",
        "aff": "单位（至多三个）",
        "footer": "由 [`data/`](https://github.com/GalenChen320/Awesome-Post-Training-Signal/tree/main/data) 自动生成。"
                  "欢迎在 [GitHub](https://github.com/GalenChen320/Awesome-Post-Training-Signal) 上贡献。许可：CC0 1.0。",
    },
}


def build_site(data: dict) -> str:
    payload = {
        "domain_zh": DOMAIN_ZH,
        "i18n": {
            lang: {
                **{k: v for k, v in SITE_TEXT[lang].items() if k != "footer"},
                "tagline": TEXT[lang]["tagline"],
                "intro_html": md_inline(TEXT[lang]["intro"]),
                "footer_html": md_inline(SITE_TEXT[lang]["footer"]),
            }
            for lang in ("en", "zh")
        },
        "modules": [
            {
                "slug": m["slug"],
                "title_en": m["title_en"],
                "title_zh": m["title_zh"],
                "desc_en_html": md_inline(m["desc_en"]),
                "desc_zh_html": md_inline(m["desc_zh"]),
                "entries": data[m["slug"]],
            }
            for m in MODULES
        ],
    }
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    template = (ROOT / "scripts" / "site_template.html").read_text(encoding="utf-8")
    return template.replace("__DATA__", blob)


def write(rel: str, content: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("wrote", rel)


def main() -> None:
    data = {m["slug"]: load(m) for m in MODULES}
    for lang in ("en", "zh"):
        write(f"README{TEXT[lang]['suffix']}.md", build_main(lang, data))
        for m in MODULES:
            write(topic_path(m, lang), build_topic(m, lang, data[m["slug"]]))
    write("docs/index.html", build_site(data))
    write("docs/.nojekyll", "")


if __name__ == "__main__":
    main()
