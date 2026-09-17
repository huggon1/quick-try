import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { pathToFileURL, fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';

// Optional development dependencies; the skill's renderer does not need Node or Playwright.
const { chromium } = await import(process.env.QUICK_TRY_PLAYWRIGHT || 'playwright');
assert(process.argv[2], 'Usage: node tests/browser_smoke.mjs <existing-bundle> [new-output-directory]');
const source = path.resolve(process.argv[2]);
const area = process.argv[3] ? path.resolve(process.argv[3]) : await fs.mkdtemp(path.join(os.tmpdir(),'experience-browser-'));
if (process.argv[3]) await fs.mkdir(area); // Never replace existing validation output.
const bundle = path.join(area, 'bundle');
await fs.cp(source, bundle, {recursive:true});
const manifest = JSON.parse(await fs.readFile(path.join(bundle,'experience.json'),'utf8'));
const script = fileURLToPath(new URL('../scripts/experience.py',import.meta.url));
const python = process.env.QUICK_TRY_PYTHON || 'python3';
execFileSync(python,[script,'render',bundle]);
const browser = await chromium.launch({headless:true, ...(process.env.QUICK_TRY_CHROMIUM ? {executablePath:process.env.QUICK_TRY_CHROMIUM} : {})});
const results = [];
try {
  const context = await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
  const page = await context.newPage();
  const requests=[], errors=[];
  page.on('request',r=>{if(/^https?:/.test(r.url())) requests.push(r.url());});
  page.on('pageerror',e=>errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error') errors.push(m.text());});
  await page.goto(pathToFileURL(path.join(bundle,'index.html')).href);
  assert(await page.locator('body').evaluate(e=>e.classList.contains('enhanced')));
  assert.equal(await page.locator('[data-panel]:visible').count(),1);
  assert.equal(await page.locator('.step-card:visible').count(),1);
  assert.equal(await page.locator('h1').textContent(),manifest.title);
  for(const step of manifest.steps) {
    await page.locator(`[data-step-link="step-${step.id}"]`).click();
    await page.locator(`#step-${step.id}`).waitFor({state:'visible'});
    assert.equal(await page.locator('.step-card:visible').count(),1);
  }
  results.push('All prepared steps remain selectable and individually readable.');
  await page.locator('#tab-observations').click();
  await page.locator('#observations').waitFor({state:'visible'});
  assert.equal(await page.locator('#tab-observations').getAttribute('aria-selected'),'true');
  await page.locator('#tab-observations').focus();
  await page.keyboard.press('ArrowRight');
  await page.locator('#notes').waitFor({state:'visible'});
  assert.equal(await page.locator('#tab-notes').getAttribute('aria-selected'),'true');
  results.push('Tabs and keyboard navigation work with their accessible selected states.');
  const maliciousText = '观察：日期调整以后需要再次排序。 <img src=x onerror="alert(1)">\n这是用户的笔记。';
  await page.locator('#note-text').fill(maliciousText);
  const exported = page.waitForEvent('download');
  await page.locator('#export-note').click();
  const download = await exported;
  const notePath = path.join(area,'exported-note.json');
  await download.saveAs(notePath);
  const envelope = JSON.parse(await fs.readFile(notePath,'utf8'));
  assert.equal(envelope.note.text,maliciousText);
  assert.equal(envelope.experience_id,manifest.id);
  assert.equal(JSON.parse(await fs.readFile(path.join(bundle,'experience.json'),'utf8')).notes.length,manifest.notes.length);
  results.push('Note export downloads the exact text without modifying canonical files.');
  const upload = async(value)=>page.locator('#import-note').setInputFiles({name:'note.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(value))});
  await page.locator('#note-text').fill('Keep this draft.');
  await upload({...envelope, experience_id:'wrong-experience'});
  await page.waitForFunction(()=>document.querySelector('#note-status').dataset.error==='true');
  assert.equal(await page.locator('#note-text').inputValue(),'Keep this draft.');
  const statusBefore = await page.locator('#note-status').textContent();
  page.once('dialog',d=>d.dismiss());
  await upload(envelope);
  await page.waitForFunction(before=>document.querySelector('#note-status').textContent!==before,statusBefore);
  assert.equal(await page.locator('#note-text').inputValue(),'Keep this draft.');
  page.once('dialog',d=>d.accept());
  await upload(envelope);
  await page.waitForFunction(expected=>document.querySelector('#note-text').value===expected,maliciousText);
  assert.equal(await page.locator('img[src="x"]').count(),0);
  await upload({...envelope,note:{...envelope.note,created_at:'2026-02-30T00:00:00Z'}});
  await page.waitForFunction(()=>document.querySelector('#note-status').dataset.error==='true');
  assert.equal(await page.locator('#note-text').inputValue(),maliciousText);
  results.push('Wrong-experience, invalid-date and canceled imports preserve the current draft; markup stays literal.');
  execFileSync(python,[script,'import-notes',bundle,notePath]);
  await page.reload();
  await page.locator('#tab-notes').click();
  assert((await page.locator('.saved-notes').textContent()).includes(maliciousText));
  assert.equal(await page.locator('img[src="x"]').count(),0);
  results.push('Exported browser notes import through the CLI and survive regeneration and reload.');
  await page.locator('#tab-guide').click();
  await page.evaluate(()=>window.scrollTo(0,0));
  for(const width of [1440,768,390]) {
    await page.setViewportSize({width,height:1000});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),`horizontal overflow at ${width}`);
    await page.screenshot({path:path.join(area,`guide-${width}.png`),fullPage:true});
  }
  await page.locator('#tab-observations').click();
  for(const width of [1440,390]) {
    await page.setViewportSize({width,height:1000});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),`observation overflow at ${width}`);
    await page.screenshot({path:path.join(area,`observations-${width}.png`),fullPage:true});
  }
  results.push('Guide and observations fit desktop, tablet and mobile viewports without horizontal overflow.');
  const nojs = await browser.newContext({javaScriptEnabled:false,viewport:{width:1440,height:1000}});
  const staticPage = await nojs.newPage();
  await staticPage.goto(pathToFileURL(path.join(bundle,'index.html')).href);
  assert.equal(await staticPage.locator('[data-panel]:visible').count(),3);
  assert.equal(await staticPage.locator('.step-card:visible').count(),manifest.steps.length);
  assert.equal(await staticPage.locator('.note-editor:visible').count(),0);
  assert((await staticPage.locator('.saved-notes').textContent()).includes(maliciousText));
  results.push('Without JavaScript, all steps, observations and saved notes remain visible.');
  assert.deepEqual(requests,[]);
  assert.deepEqual(errors,[]);
  results.push('No HTTP requests, JavaScript exceptions or browser console errors occurred.');
  await fs.writeFile(path.join(area,'results.json'),JSON.stringify({source,checks:results},null,2)+'\n');
  console.log(JSON.stringify({passed:results.length,output:area,checks:results},null,2));
} finally {await browser.close();}
