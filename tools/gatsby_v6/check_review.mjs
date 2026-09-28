import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require('/Users/dhiren/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const root=path.join(repo,'docs/gatsby-v6');
const out=path.join(root,'verification');
const base=process.env.GATSBY_TEST_URL||pathToFileURL(path.join(root,'index.html')).href;
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
async function choose(id){await page.evaluate(id=>{location.hash=id;},id);await page.waitForFunction(id=>document.querySelector('#heading .meta')?.textContent.includes(id)&&document.querySelector('#tabs').children.length===8,id);}
async function section(name){await page.locator(`[data-section="${name}"]`).click();}
try{
 await page.goto(base);await page.locator('[data-section="Brief"]').waitFor();
 const ids=await page.locator('[data-task]').evaluateAll(xs=>xs.map(x=>x.dataset.task));assert.equal(ids.length,100);
 for(const [i,id]of ids.entries()){
  await choose(id);
  for(const name of ['Brief','Brand','Outputs','Auto verifiers','Human verifiers','V6 changes','Trajectory']){
   await section(name);const text=await page.locator('#content').innerText();assert(text.length>80,`${id}/${name} blank`);assert(!/\bundefined\b|\bNaN\b/.test(text),`${id}/${name} invalid value`);
  }
  if((i+1)%20===0)console.log(`Rendered ${i+1}/100 task contracts`);
 }
 await choose('PHOTO-04');await section('Human verifiers');
 await page.locator('#output-filter').selectOption('booking-hero-verranza');await page.locator('#check-search').fill('High Summer');await page.waitForTimeout(250);
 assert((await page.locator('.verifier-table').innerText()).includes('High Summer'));
 await page.screenshot({path:path.join(out,'desktop-verifiers.png')});
 await section('Brief');const downloadPromise=page.waitForEvent('download');await page.locator('[data-task-file="TASK_SPEC.json"]').click();const download=await downloadPromise;assert.equal(download.suggestedFilename(),'TASK_SPEC.json');const json=JSON.parse(fs.readFileSync(await download.path()));assert.equal(json.id,'PHOTO-04');assert.equal(json.revision.edition,'V6');
 await section('Assets');const images=page.locator('.asset-card img');await images.first().waitFor();
 await page.waitForFunction(()=>[...document.querySelectorAll('.asset-card img')].slice(0,4).every(i=>i.complete&&i.naturalWidth>0),null,{timeout:45000});
 await page.screenshot({path:path.join(out,'desktop-assets.png')});
 await page.setViewportSize({width:390,height:844});await section('Human verifiers');await page.screenshot({path:path.join(out,'mobile-verifiers.png')});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile horizontal overflow');
 await section('Assets');await page.screenshot({path:path.join(out,'mobile-assets.png')});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile assets overflow');
 await page.locator('#search').fill('Verranza');assert((await page.locator('[data-task]').count())>=1);await page.locator('#search').fill('');
 assert.deepEqual(errors,[]);
 const report={status:'passed',tasks_rendered:100,sections_per_task:7,downloaded_json_valid:true,desktop:[1440,1000],mobile:[390,844],public_image_sample:'PHOTO-04 first four previews loaded',javascript_errors:errors,test_url:base.startsWith('file:')?'local V6 file':base};
 fs.writeFileSync(path.join(out,'BROWSER_QA.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
}finally{await browser.close();}
