import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
const base=process.env.DEMO_URL||'http://127.0.0.1:4382';
const out=new URL('../results/browser/',import.meta.url);
await mkdir(out,{recursive:true});
const browser=await chromium.launch({channel:process.env.BROWSER_CHANNEL||'msedge',headless:true});
const report=[];
try {
  for(const [name,viewport] of [['desktop',{width:1440,height:1060}],['mobile',{width:390,height:844}]]) {
    const page=await browser.newPage({viewport});const errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto(base);
    await page.locator('#model option[value="TNN_reconstruct"]').waitFor({state:'attached'});
    await page.locator('#pid').selectOption('46');
    await page.locator('#case').selectOption('outage');
    await page.locator('#seek').evaluate(e=>{e.value=Math.floor(+e.max/2);e.dispatchEvent(new Event('input',{bubbles:true}));});
    assert.match(await page.locator('#status').innerText(),/已知输入缺失/);
    await page.getByRole('button',{name:'揭晓实测温度',exact:true}).click();
    assert.equal(await page.locator('#scores tr').count(),5);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
    for(const path of ['/data/kaggle-pmsm.zip','/data/kaggle-metadata.json','/.env','/.git/config','/results/tnn-author.pt','/../LICENSE']) {
      assert.equal((await page.request.get(base+path)).status(),404);
    }
    await page.getByRole('button',{name:'播放',exact:true}).click();
    await page.getByRole('button',{name:'暂停',exact:true}).click();
    await page.screenshot({path:new URL(`${name}.png`,out).pathname.replace(/^\/(\w:)/,'$1'),fullPage:true});
    assert.deepEqual(errors,[]);
    report.push({viewport:name,passed:true,console_errors:errors});
    await page.close();
  }
} finally { await browser.close(); }
await writeFile(new URL('report.json',out),JSON.stringify(report,null,2));
console.log(JSON.stringify(report));
