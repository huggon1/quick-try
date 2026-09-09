/* Progressive enhancement only. Bundle data is never executable JavaScript. */
(() => {
  "use strict";

  const messages = {
    en: {
      count: "characters",
      empty: "Write a note before exporting.",
      tooLong: "This note is too long. Keep it within 20,000 characters.",
      exported: "Note download started. Check that the file was saved, then give it to your agent to add to this bundle. The source files have not changed.",
      exportFailed: "The browser could not export the note. Copy your text before leaving this page.",
      invalid: "This file is not a valid experience note. Choose a JSON note exported from this page.",
      mismatch: "This note belongs to a different experience. Open its original notebook to import it.",
      tooLarge: "This file is larger than 2 MiB. Choose a single exported note file.",
      replace: "Replace your unexported draft with this note? Cancel to export your current draft first.",
      imported: "Note loaded into the draft. Saved notes and source files have not changed. Export any edits before leaving.",
      canceled: "Import canceled. Your draft is unchanged.",
      readFailed: "The file could not be read. Your draft is unchanged.",
    },
    "zh-CN": {
      count: "个字符",
      empty: "请先写一条笔记再导出。",
      tooLong: "笔记过长，请控制在 20,000 个字符以内。",
      exported: "已发起笔记下载。确认文件保存后，可以交给 Agent 加入体验包，源文件尚未修改。",
      exportFailed: "浏览器无法导出笔记。离开页面前请复制草稿内容。",
      invalid: "这不是有效的体验笔记文件。请选择从此页面导出的 JSON 笔记。",
      mismatch: "这条笔记属于另一次体验。请打开对应的体验页再导入。",
      tooLarge: "文件大于 2 MiB，请选择单条导出的笔记文件。",
      replace: "要用导入的笔记替换尚未导出的草稿吗？取消后可以先导出当前草稿。",
      imported: "笔记已加载到草稿。已保存的笔记和源文件没有变化；离开前请导出你的修改。",
      canceled: "已取消导入，草稿未修改。",
      readFailed: "无法读取文件，草稿未修改。",
    },
  };
  const text = messages[document.body.dataset.language] || messages.en;
  const panels = Array.from(document.querySelectorAll("[data-panel]"));
  const tabs = Array.from(document.querySelectorAll("[data-panel-link]"));
  const stepCards = Array.from(document.querySelectorAll(".step-card"));
  const stepLinks = Array.from(document.querySelectorAll("[data-step-link]"));
  const navigation = document.querySelector(".page-nav");
  let selectedStep = stepCards[0] ? stepCards[0].id : null;

  function showPanel(id) {
    panels.forEach((panel) => { panel.hidden = panel.id !== id; });
    tabs.forEach((tab) => {
      const selected = tab.dataset.panelLink === id;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
  }

  function showStep(id) {
    if (!stepCards.some((step) => step.id === id)) return;
    selectedStep = id;
    stepCards.forEach((step) => { step.hidden = step.id !== id; });
    stepLinks.forEach((link) => {
      if (link.dataset.stepLink === id) link.setAttribute("aria-current", "step");
      else link.removeAttribute("aria-current");
    });
  }

  function routeHash(scroll) {
    let hash;
    try { hash = decodeURIComponent(window.location.hash.slice(1)); }
    catch (_) { hash = "guide"; }
    const target = document.getElementById(hash || "guide");
    const panel = target && (target.matches("[data-panel]") ? target : target.closest("[data-panel]"));
    if (panel) showPanel(panel.id);
    else if (!hash) showPanel("guide");
    const step = target && target.closest(".step-card");
    showStep(step ? step.id : selectedStep);
    if (scroll && target) {
      target.scrollIntoView({ block: "start", behavior: "auto" });
      if (target.matches(".step-card, .observation, .artifact")) target.focus({ preventScroll: true });
    }
  }

  navigation.setAttribute("role", "tablist");
  tabs.forEach((tab) => {
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-controls", tab.dataset.panelLink);
    tab.addEventListener("keydown", (event) => {
      const index = tabs.indexOf(tab);
      let nextIndex;
      if (event.key === "ArrowRight") nextIndex = (index + 1) % tabs.length;
      else if (event.key === "ArrowLeft") nextIndex = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === "Home") nextIndex = 0;
      else if (event.key === "End") nextIndex = tabs.length - 1;
      else return;
      event.preventDefault();
      tabs[nextIndex].focus();
      tabs[nextIndex].click();
    });
  });
  panels.forEach((panel) => {
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("aria-labelledby", "tab-" + panel.id);
    panel.tabIndex = 0;
  });
  document.body.classList.add("enhanced");
  showPanel("guide");
  showStep(selectedStep);
  routeHash(false);
  window.addEventListener("hashchange", () => routeHash(true));
  document.addEventListener("click", (event) => {
    const link = event.target instanceof Element && event.target.closest("a[href^='#']");
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    // Clicking an already-selected hash does not emit hashchange.
    if (link.getAttribute("href") === window.location.hash) routeHash(true);
  });

  // Keep the goal and entry visible on phones without putting every resource
  // ahead of the guide. The HTML starts open so no-JS readers lose no content.
  const contextDetails = document.querySelector(".context-details");
  const narrowViewport = window.matchMedia("(max-width: 760px)");
  function applyContextLayout() { contextDetails.open = !narrowViewport.matches; }
  applyContextLayout();
  if (narrowViewport.addEventListener) narrowViewport.addEventListener("change", applyContextLayout);
  else narrowViewport.addListener(applyContextLayout);

  const editor = document.querySelector(".note-editor");
  const draft = document.getElementById("note-text");
  const status = document.getElementById("note-status");
  const count = document.getElementById("note-count");
  const fileInput = document.getElementById("import-note");
  const experienceId = document.body.dataset.experienceId;
  const maxCharacters = 20000;
  let exportedText = "";
  let importedNote = null;
  let importSequence = 0;
  editor.hidden = false;

  function dirty() { return draft.value !== exportedText; }
  function tell(message, error = false) {
    status.textContent = message;
    status.dataset.error = String(error);
  }
  function characterCount(value) { return Array.from(value).length; }
  function updateCount() { count.textContent = String(characterCount(draft.value)) + " / 20,000 " + text.count; }
  draft.addEventListener("input", () => { updateCount(); tell(""); });
  window.addEventListener("beforeunload", (event) => {
    if (!dirty()) return;
    event.preventDefault();
    event.returnValue = "";
  });

  document.getElementById("export-note").addEventListener("click", () => {
    if (!draft.value.trim()) { tell(text.empty, true); draft.focus(); return; }
    if (characterCount(draft.value) > maxCharacters) { tell(text.tooLong, true); return; }
    const note = importedNote && importedNote.text === draft.value ? importedNote : {
      id: "note-" + Date.now(),
      created_at: new Date().toISOString(),
      text: draft.value,
    };
    const envelope = { schema_version: 1, experience_id: experienceId, note };
    let downloadUrl;
    try {
      const blob = new Blob([JSON.stringify(envelope, null, 2) + "\n"], { type: "application/json" });
      downloadUrl = URL.createObjectURL(blob);
      const download = document.createElement("a");
      download.href = downloadUrl;
      download.download = experienceId + "-" + note.id + ".json";
      document.body.appendChild(download);
      download.click();
      download.remove();
      exportedText = draft.value;
      importedNote = note;
      tell(text.exported);
    } catch (_) {
      tell(text.exportFailed, true);
    } finally {
      if (downloadUrl) window.setTimeout(() => URL.revokeObjectURL(downloadUrl), 60000);
    }
  });

  function isObject(value) { return value !== null && typeof value === "object" && !Array.isArray(value); }
  function exactKeys(value, keys) {
    return isObject(value) && Object.keys(value).length === keys.length && keys.every((key) => Object.prototype.hasOwnProperty.call(value, key));
  }
  function validTimestamp(value) {
    if (typeof value !== "string") return false;
    const parts = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(?:Z|([+-])(\d{2}):(\d{2}))$/.exec(value);
    if (!parts || !Number.isFinite(Date.parse(value))) return false;
    const year = Number(parts[1]);
    const month = Number(parts[2]);
    const day = Number(parts[3]);
    const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
    const monthDays = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    return year > 0 && month >= 1 && month <= 12 && day >= 1 && day <= monthDays[month - 1] && Number(parts[4]) < 24 && Number(parts[5]) < 60 && Number(parts[6]) < 60 && (!parts[7] || (Number(parts[8]) < 24 && Number(parts[9]) < 60));
  }
  function validNoteEnvelope(value) {
    if (!exactKeys(value, ["schema_version", "experience_id", "note"]) || value.schema_version !== 1 || typeof value.experience_id !== "string") return false;
    const note = value.note;
    return exactKeys(note, ["id", "created_at", "text"]) && typeof note.id === "string" && /^[a-z0-9][a-z0-9-]{0,95}$/.test(note.id) && validTimestamp(note.created_at) && typeof note.text === "string" && note.text.trim().length > 0 && characterCount(note.text) <= maxCharacters && !/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(note.text);
  }
  fileInput.addEventListener("change", async () => {
    const file = fileInput.files && fileInput.files[0];
    const sequence = ++importSequence;
    fileInput.value = "";
    if (!file) return;
    if (file.size > 2 * 1024 * 1024) { tell(text.tooLarge, true); return; }
    let envelope;
    try {
      envelope = JSON.parse(await file.text());
    } catch (_) {
      if (sequence === importSequence) tell(text.readFailed, true);
      return;
    }
    if (sequence !== importSequence) return;
    if (!validNoteEnvelope(envelope)) { tell(text.invalid, true); return; }
    if (envelope.experience_id !== experienceId) { tell(text.mismatch, true); return; }
    if (dirty() && draft.value.trim() && draft.value !== envelope.note.text && !window.confirm(text.replace)) {
      tell(text.canceled);
      return;
    }
    // Only plain text enters the editor. Never insert imported HTML or execute it.
    draft.value = envelope.note.text;
    exportedText = draft.value;
    importedNote = envelope.note;
    updateCount();
    tell(text.imported);
    draft.focus();
  });
})();
