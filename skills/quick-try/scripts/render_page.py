"""Render a validated experience bundle as a portable, offline HTML notebook."""

from __future__ import annotations

import base64
import hashlib
import html
from pathlib import Path
from urllib.parse import quote, urlsplit


ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"

LABELS = {
    "en": {
        "notebook": "Experience notebook", "skip": "Skip to the experience",
        "model": "Model", "harness": "Coding agent", "product": "Product",
        "prompt": "Prompt collection", "self": "Explore yourself",
        "agent-demo": "Agent demonstration", "draft": "Draft",
        "blocked": "Needs preparation", "ready": "Ready to explore",
        "guide": "Experience guide", "observations": "Recorded walkthrough",
        "notes": "Your notes", "goal": "What you want to find out",
        "resources": "Time and resources", "context_details": "Time, requirements and reset", "preparation": "Preparation",
        "hands_on": "Your time", "cost": "Cost", "requirements": "What is needed",
        "available": "Available", "missing": "Missing", "unknown": "Not checked",
        "unavailable": "Unavailable", "reset": "Start over",
        "baseline": "Starting conditions", "target": "Original project",
        "version": "Version", "start": "Open the experience",
        "reference": "Open reference only", "not_ready": "This scene has not passed all readiness checks. Its link is a reference, not a verified starting point.",
        "no_entry": "An experience link has not been prepared yet.",
        "ready_note": "The author recorded checks for the entry, sample, core action, and reset. See the evidence before drawing conclusions.",
        "navigation": "Experience sections", "steps": "Choose a step",
        "step": "Step", "do": "What to do", "input": "Prepared input",
        "expected": "What to look for", "expected_note": "An expectation to investigate, not an observed result.",
        "variations": "Change something", "next": "Next step", "previous": "Previous step",
        "no_steps": "The author has not prepared steps yet. Use the goal and missing resources to continue planning.",
        "model_intro": "Use the same prepared input, then change one condition and compare the actual outputs.",
        "harness_intro": "Keep the task and starting repository visible. Inspect the changes and checks before judging the result.",
        "product_intro": "Work in the real product. Keep the sample task here and record the moments that help or get in your way.",
        "prompt_intro": "Keep the template, variables, and reference material together. Compare your generated results after each change.",
        "model_input": "Input and settings", "harness_input": "Task and sample repository",
        "product_input": "Task and sample workspace", "prompt_input": "Prompt and variables",
        "scope": "Agreed scope", "constraints": "Constraints", "capabilities": "Available ways to try it",
        "sources": "Useful reading", "first-party": "First-party source",
        "community": "Community experience", "accessed": "Checked",
        "limitations": "What this experience cannot establish", "next_steps": "Keep exploring",
        "no_sources": "No sources have been recorded yet.", "no_limits": "No limitations have been recorded. This is not evidence of unrestricted capability.",
        "no_next": "Add a question after your first attempt.",
        "observations_intro": "These are recorded attempts. Agent and user results stay separate; use the same starting conditions to try them yourself.",
        "empty_observations": "No attempt has been recorded. Expectations in the guide are not test results.",
        "agent": "Agent", "user": "User", "cli": "Command line", "api": "API",
        "browser": "Browser", "desktop": "Desktop", "manual": "Manual",
        "success": "Succeeded", "failure": "Failed", "partial": "Partial result",
        "action": "Action taken", "actual_input": "Input used", "observed": "What actually happened",
        "settings": "Conditions and settings", "evidence": "Evidence", "no_evidence": "No artifact is attached to this attempt.",
        "model_results": "Recorded outputs", "harness_results": "Changes and checks",
        "product_results": "Recorded interactions", "prompt_results": "Generated results",
        "verification": "Readiness checks", "verification_note": "These checks record the author's evidence. The page does not run the project or independently verify those claims.",
        "entry": "Entry works", "sample": "Sample is available", "core-action": "Core action works",
        "passed": "Passed", "failed": "Failed", "unverified": "Not verified",
        "verification_empty": "Readiness checks have not been recorded.",
        "artifacts": "Saved materials", "no_artifacts": "No materials have been saved yet.",
        "open_file": "Open saved file", "open_image": "Open full image",
        "private": "Local notebook · no automatic uploads", "offline": "Reading and notes work offline. Project and source links open only when you choose them.",
        "notes_intro": "Keep your own reactions alongside the evidence. Note what surprised you, what you changed, or what you want to try next.",
        "saved_notes": "Notes saved in this bundle", "no_notes": "No personal notes have been saved in the bundle yet.",
        "draft_note": "New note", "note_placeholder": "What did you notice? What would you change next?",
        "note_help": "Drafts are kept only in this open page. Export before refreshing or closing. Exporting downloads a file; it does not save into this bundle. Give the file to your agent to add it to the experience.",
        "export": "Export note", "import": "Import note file", "note_count": "characters",
        "js_notes": "JavaScript is off. Saved notes remain readable. Ask your agent to add a note to the bundle, or enable JavaScript to draft and export one here.",
        "import_help": "Import loads one matching note into the draft. It does not change saved notes or the source bundle.",
        "plan": "Preparation details", "nothing": "Not specified", "show_all": "All steps are available below.",
    },
    "zh-CN": {
        "notebook": "体验手记", "skip": "跳到体验内容",
        "model": "模型", "harness": "Coding Agent", "product": "产品",
        "prompt": "提示词库", "self": "自己探索", "agent-demo": "Agent 先示范",
        "draft": "准备中", "blocked": "需要补充准备", "ready": "可以开始体验",
        "guide": "体验指南", "observations": "操作与结果", "notes": "我的笔记",
        "goal": "这次想了解什么", "resources": "时间与资源", "context_details": "时间、条件与重置", "preparation": "准备时间",
        "hands_on": "体验时间", "cost": "费用", "requirements": "需要的条件",
        "available": "已具备", "missing": "缺少", "unknown": "尚未检查", "unavailable": "不可用",
        "reset": "重新开始", "baseline": "初始条件", "target": "原项目", "version": "版本",
        "start": "打开体验", "reference": "仅打开参考入口",
        "not_ready": "这个场景尚未通过全部可用性检查。链接只供参考，还不能作为已验证的体验入口。",
        "no_entry": "尚未准备体验入口。", "ready_note": "作者已记录入口、样例、核心操作和重置检查。请结合证据判断结果。",
        "navigation": "体验内容导航", "steps": "选择一步", "step": "步骤", "do": "怎么操作",
        "input": "准备好的输入", "expected": "观察什么",
        "expected_note": "这是待验证的预期，并非实际结果。", "variations": "试着改一改",
        "next": "下一步", "previous": "上一步", "no_steps": "尚未准备操作步骤。可以根据体验目标和缺少的资源继续完善方案。",
        "model_intro": "先使用准备好的输入，再改变一个条件，比较实际输出。",
        "harness_intro": "保留任务与仓库初始状态，检查实际改动和验证结果，再形成判断。",
        "product_intro": "在原产品里操作，对照这里的样例任务，记下顺畅和卡住的地方。",
        "prompt_intro": "把模板、变量和参考素材放在一起，比较每次改动后的真实生成结果。",
        "model_input": "输入与设置", "harness_input": "任务与样例仓库",
        "product_input": "任务与样例工作区", "prompt_input": "提示词与变量",
        "scope": "已约定的范围", "constraints": "约束", "capabilities": "可用的体验方式",
        "sources": "相关资料", "first-party": "一手资料", "community": "他人使用经验", "accessed": "查阅于",
        "limitations": "这次还不能验证什么", "next_steps": "继续探索",
        "no_sources": "尚未记录参考资料。", "no_limits": "尚未记录限制，这不代表能力不受限制。", "no_next": "第一次尝试后，可以补充一个想继续了解的问题。",
        "observations_intro": "这里保留真实操作记录，并标明由 Agent 还是用户完成。可以从相同初始条件开始，自己再试一次。",
        "empty_observations": "尚未记录任何实际尝试。指南中的预期不代表实测结果。",
        "agent": "Agent", "user": "用户", "cli": "命令行", "api": "API", "browser": "浏览器", "desktop": "桌面", "manual": "人工操作",
        "success": "成功", "failure": "失败", "partial": "部分完成", "action": "实际操作",
        "actual_input": "使用的输入", "observed": "实际发生了什么", "settings": "条件与设置",
        "evidence": "结果证据", "no_evidence": "这次操作尚未附带证据文件。",
        "model_results": "实际输出", "harness_results": "改动与检查", "product_results": "交互记录", "prompt_results": "生成结果",
        "verification": "可用性检查", "verification_note": "这些检查记录作者提供的证据。此页面不会运行项目，也不会独立验证这些结论。",
        "entry": "入口可用", "sample": "样例可用", "core-action": "核心操作可用", "passed": "通过", "failed": "未通过", "unverified": "未验证",
        "verification_empty": "尚未记录可用性检查。", "artifacts": "保存的材料", "no_artifacts": "尚未保存材料。",
        "open_file": "打开保存的文件", "open_image": "查看原图", "private": "本地手记 · 不会自动上传",
        "offline": "内容与笔记功能可离线使用。只有主动点击时才打开项目和资料链接。",
        "notes_intro": "在结果旁边留下自己的感受：哪里出乎意料、改了什么、接下来想试什么。",
        "saved_notes": "已保存到体验包的笔记", "no_notes": "体验包中尚未保存个人笔记。",
        "draft_note": "写一条笔记", "note_placeholder": "你观察到了什么？接下来想改变哪个条件？",
        "note_help": "草稿只保留在当前打开的页面中。刷新或关闭前请导出。导出仅下载文件，不会直接保存到体验包；可以把文件交给 Agent 加入这次体验。",
        "export": "导出笔记", "import": "导入笔记文件", "note_count": "个字符",
        "js_notes": "JavaScript 已关闭，仍可阅读已保存的笔记。可请 Agent 把笔记加入体验包，或启用 JavaScript 在此编写并导出。",
        "import_help": "导入会把同一体验的一条笔记加载到草稿，不会修改已保存的笔记或源文件。",
        "plan": "准备详情", "nothing": "尚未说明", "show_all": "以下可查看全部步骤。",
    },
}


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _url(value: str) -> str:
    """Keep remote URLs intact; encode literal local path punctuation once."""
    if urlsplit(value).scheme:
        return _escape(value)
    return _escape(quote(value, safe="/"))


def _text(value: str, class_name: str = "text") -> str:
    return f'<p class="{class_name}">{_escape(value)}</p>'


def _list(items: list[str], empty: str = "") -> str:
    if not items:
        return _text(empty, "muted text") if empty else ""
    return '<ul class="text-list">' + "".join(f"<li>{_escape(item)}</li>" for item in items) + "</ul>"


def _hash_source(content: str) -> str:
    return "'sha256-" + base64.b64encode(hashlib.sha256(content.encode("utf-8")).digest()).decode("ascii") + "'"


def render_page(data: dict) -> str:
    """Return HTML for validated data; do not execute or fetch anything in it."""
    labels = LABELS[data["language"]]
    t = lambda key: _escape(labels[key])
    css = (ASSET_DIR / "page.css").read_text(encoding="utf-8")
    js = (ASSET_DIR / "page.js").read_text(encoding="utf-8")
    csp = (
        "default-src 'none'; base-uri 'none'; object-src 'none'; form-action 'none'; "
        "connect-src 'none'; img-src 'self' file:; "
        f"style-src {_hash_source(css)}; script-src {_hash_source(js)}"
    )
    badge = lambda value: f'<span class="badge badge-{_escape(value)}">{t(value)}</span>'
    link = lambda url, label, cls="": (
        f'<a class="{cls}" href="{_url(url)}" target="_blank" rel="noopener noreferrer">'
        f'{_escape(label)}<span class="external" aria-hidden="true"> ↗</span></a>'
    )
    field = lambda label, value, cls="": (
        f'<div class="field {cls}"><h4>{t(label)}</h4>{_text(value or labels["nothing"])}</div>'
    )
    artifact_by_id = {item["id"]: item for item in data["artifacts"]}
    step_by_id = {item["id"]: item for item in data["steps"]}

    entry = data["entry"]
    if entry:
        entry_html = link(entry["url"], labels["start"] if data["status"] == "ready" else labels["reference"], "entry-link")
        entry_html += _text(entry["label"], "entry-caption")
    else:
        entry_html = _text(labels["no_entry"], "muted text")
    entry_html += _text(labels["ready_note"] if data["status"] == "ready" else labels["not_ready"], "entry-help")

    requirements = "".join(
        f'<li><div class="requirement-label"><strong>{_escape(item["name"])}</strong>{badge(item["status"])}</div>{_text(item["detail"], "small text")}</li>'
        for item in data["requirements"]
    )
    capabilities = "".join(
        f'<li><div class="requirement-label"><strong>{_escape(item["name"])}</strong>{badge(item["status"])}</div>{_text(item["detail"], "small text")}</li>'
        for item in data["capabilities"]
    )
    step_nav = "".join(
        f'<a href="#step-{_escape(step["id"])}" data-step-link="step-{_escape(step["id"])}"><span class="step-number">{index:02d}</span><span>{_escape(step["title"])}</span></a>'
        for index, step in enumerate(data["steps"], 1)
    )
    steps = []
    for index, step in enumerate(data["steps"], 1):
        controls = []
        if index > 1:
            previous_id = data["steps"][index - 2]["id"]
            controls.append(f'<a class="step-back" href="#step-{_escape(previous_id)}">← {t("previous")}</a>')
        if index < len(data["steps"]):
            next_id = data["steps"][index]["id"]
            controls.append(f'<a href="#step-{_escape(next_id)}">{t("next")} →</a>')
        steps.append(
            f'<article class="step-card" id="step-{_escape(step["id"])}" tabindex="-1">'
            f'<p class="eyebrow">{t("step")} {index:02d} / {len(data["steps"]):02d}</p><h3>{_escape(step["title"])}</h3>'
            + field("do", step["instruction"], "instruction")
            + field(data["kind"] + "_input", step["input"], "prepared-input")
            + f'<div class="expected field"><h4>{t("expected")}</h4>{_text(step["expected"] or labels["nothing"])}<p class="caption">{t("expected_note")}</p></div>'
            + (f'<div class="field variations"><h4>{t("variations")}</h4>{_list(step["variations"])}</div>' if step["variations"] else "")
            + '<nav class="step-controls">' + "".join(controls) + '</nav></article>'
        )

    sources = "".join(
        f'<article class="source" id="source-{_escape(source["id"])}"><div class="source-meta">{t(source["kind"])} · {t("accessed")} <time datetime="{_escape(source["accessed"])}">{_escape(source["accessed"])}</time></div>'
        + f'<h4>{link(source["url"], source["title"])}</h4>' + _text(source["context"]) + '</article>'
        for source in data["sources"]
    ) or _text(labels["no_sources"], "muted text")

    observations = []
    for observation in data["observations"]:
        evidence_links = "".join(
            f'<a class="evidence-link" href="#artifact-{_escape(artifact_id)}">{_escape(artifact_by_id[artifact_id]["label"])}</a>'
            for artifact_id in observation["artifact_ids"]
        ) or _text(labels["no_evidence"], "muted small")
        step = step_by_id[observation["step_id"]]
        observations.append(
            f'<article class="observation" id="observation-{_escape(observation["id"])}" tabindex="-1">'
            f'<div class="observation-meta"><span class="actor actor-{_escape(observation["actor"])}">{t(observation["actor"])}</span><span>{t(observation["method"])}</span>'
            f'<time datetime="{_escape(observation["recorded_at"])}">{_escape(observation["recorded_at"])}</time>{badge(observation["outcome"])}</div>'
            f'<h3><a href="#step-{_escape(step["id"])}">{_escape(step["title"])}</a></h3>'
            + field("action", observation["action"])
            + field("actual_input", observation["input"], "prepared-input")
            + field("observed", observation["observed"], "actual-result")
            + field("settings", observation["settings"])
            + f'<div class="field"><h4>{t("evidence")}</h4><div class="evidence-links">{evidence_links}</div></div></article>'
        )
    verification = []
    for check in data["verification"]:
        refs = " ".join(
            f'<a href="#observation-{_escape(observation_id)}">{_escape(observation_id)}</a>'
            for observation_id in check["observation_ids"]
        )
        verification.append(
            f'<li><div class="requirement-label"><strong>{t(check["check"])}</strong>{badge(check["status"])}</div>'
            + _text(check["detail"]) + f'<div class="check-evidence">{refs}</div></li>'
        )
    artifacts = []
    for artifact in data["artifacts"]:
        if artifact["kind"] == "image":
            preview = f'<a href="{_url(artifact["path"])}" target="_blank" rel="noopener noreferrer"><img src="{_url(artifact["path"])}" alt="{_escape(artifact["label"])}" loading="lazy" decoding="async"></a>'
            artifact_link = link(artifact["path"], labels["open_image"])
        else:
            preview = '<span class="file-marker" aria-hidden="true">↗</span>'
            artifact_link = link(artifact["path"], labels["open_file"])
        artifacts.append(
            f'<figure class="artifact artifact-{_escape(artifact["kind"])}" id="artifact-{_escape(artifact["id"])}" tabindex="-1">{preview}'
            f'<figcaption><strong>{_escape(artifact["label"])}</strong><code>{_escape(artifact["path"])}</code>{artifact_link}</figcaption></figure>'
        )
    notes = "".join(
        f'<article class="saved-note"><time datetime="{_escape(note["created_at"])}">{_escape(note["created_at"])}</time>{_text(note["text"])}</article>'
        for note in data["notes"]
    ) or _text(labels["no_notes"], "muted text")
    page_navigation = "".join(
        f'<a id="tab-{key}" href="#{key}" data-panel-link="{key}">{t(key)}'
        + (f'<span class="nav-count">{len(data["observations"])}</span>' if key == "observations" else "") + '</a>'
        for key in ("guide", "observations", "notes")
    )
    return f'''<!doctype html>
<html lang="{_escape(data["language"])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{_escape(csp)}">
<meta name="referrer" content="no-referrer">
<title>{_escape(data["title"])} · {t("notebook")}</title>
<style>{css}</style>
</head>
<body data-experience-id="{_escape(data["id"])}" data-language="{_escape(data["language"])}" data-kind="{_escape(data["kind"])}">
<a class="skip-link" href="#main">{t("skip")}</a>
<header class="masthead"><a class="wordmark" href="#guide"><span class="notebook-mark" aria-hidden="true">↗</span>{t("notebook")}</a><span class="privacy">{t("private")}</span></header>
<div class="workspace">
<aside class="context-rail" aria-label="{t("goal")}">
<div class="rail-heading"><span class="eyebrow">{t(data["kind"])}</span>{badge(data["status"])}</div>
<section class="goal"><h2>{t("goal")}</h2>{_text(data["goal"] or labels["nothing"])}</section>
<section class="entry">{entry_html}</section>
<details class="context-details" open><summary>{t("context_details")}</summary>
<section><h2>{t("resources")}</h2><dl class="resource-list">{''.join(f'<div><dt>{t(key)}</dt><dd>{_escape(data["budget"][key] or labels["nothing"])}</dd></div>' for key in ("preparation", "hands_on", "cost"))}</dl></section>
<section><h2>{t("requirements")}</h2><ul class="requirements">{requirements}</ul></section>
<section><h2>{t("baseline")}</h2>{_text(data["baseline"] or labels["nothing"], "small text")}</section>
<section class="reset"><h2>{t("reset")}</h2>{_text(data["reset"] or labels["nothing"], "small text")}</section>
</details>
</aside>
<main id="main" tabindex="-1">
<div class="title-block"><p class="eyebrow">{t(data["mode"])}</p><h1>{_escape(data["title"])}</h1>{_text(data["summary"], "summary text")}<div class="target-meta">{link(data["target"]["url"], data["target"]["name"] or labels["target"])}<span>{t("version")}: {_escape(data["target"]["version"] or labels["nothing"])}</span></div></div>
<nav class="page-nav" aria-label="{t("navigation")}">{page_navigation}</nav>
<section id="guide" data-panel="guide" class="content-panel" aria-labelledby="guide-title">
<div class="section-heading"><h2 id="guide-title">{t("guide")}</h2>{_text(labels[data["kind"] + "_intro"], "section-intro")}</div>
<div class="step-workspace"><nav class="step-nav" aria-label="{t("steps")}">{step_nav}</nav><div class="step-content">{''.join(steps) or _text(labels["no_steps"], "empty-state")}</div></div>
<section class="support-section"><h3>{t("sources")}</h3><div class="sources">{sources}</div></section>
<section class="support-section"><h3>{t("limitations")}</h3>{_list(data["limitations"], labels["no_limits"])}</section>
<section class="support-section"><h3>{t("next_steps")}</h3>{_list(data["next_steps"], labels["no_next"])}</section>
<details class="preparation"><summary>{t("plan")}</summary><h3>{t("scope")}</h3>{_text(data["authorization"]["scope"] or labels["nothing"])}<h4>{t("constraints")}</h4>{_list(data["authorization"]["constraints"], labels["nothing"])}<h3>{t("capabilities")}</h3><ul class="requirements">{capabilities}</ul></details>
</section>
<section id="observations" data-panel="observations" class="content-panel" aria-labelledby="observations-title">
<div class="section-heading"><h2 id="observations-title">{t(data["kind"] + "_results")}</h2>{_text(labels["observations_intro"], "section-intro")}</div>
<div class="observations">{''.join(observations) or _text(labels["empty_observations"], "empty-state")}</div>
<section class="support-section"><h3>{t("verification")}</h3>{_text(labels["verification_note"], "muted text")}<ul class="verification-list">{''.join(verification)}</ul>{_text(labels["verification_empty"], "muted text") if not verification else ''}</section>
<section class="support-section"><h3>{t("artifacts")}</h3><div class="artifact-grid">{''.join(artifacts) or _text(labels["no_artifacts"], "muted text")}</div></section>
</section>
<section id="notes" data-panel="notes" class="content-panel" aria-labelledby="notes-title">
<div class="section-heading"><h2 id="notes-title">{t("notes")}</h2>{_text(labels["notes_intro"], "section-intro")}</div>
<div class="note-editor" hidden><label for="note-text">{t("draft_note")}</label><textarea id="note-text" rows="9" placeholder="{t("note_placeholder")}" aria-describedby="note-help"></textarea><p id="note-help" class="caption">{t("note_help")}</p><div class="note-actions"><button id="export-note" type="button">{t("export")}</button><label class="import-button" for="import-note">{t("import")}</label><input id="import-note" class="file-input" type="file" accept=".json,application/json"><span id="note-count" class="caption">0 / 20,000 {t("note_count")}</span></div><p class="caption">{t("import_help")}</p><p id="note-status" class="note-status" aria-live="polite" role="status"></p></div>
<noscript><p class="empty-state">{t("js_notes")}</p></noscript>
<section class="saved-notes support-section"><h3>{t("saved_notes")}</h3>{notes}</section>
</section>
<footer>{t("offline")}</footer>
</main>
</div>
<script>{js}</script>
</body>
</html>
'''
