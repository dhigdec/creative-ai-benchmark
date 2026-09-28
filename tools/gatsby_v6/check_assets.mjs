import fs from 'node:fs';
import path from 'node:path';
import {execFileSync,execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {fileURLToPath} from 'node:url';
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const root=path.join(repo,'docs/gatsby-v6');
const tasks=fs.readdirSync(path.join(root,'tasks')).map(id=>JSON.parse(execFileSync('unzip',['-p',path.join(root,'tasks',id,'TASK_PACKAGE.zip'),'TASK_SPEC.json'],{maxBuffer:15e6})));
const urls=new Map();for(const t of tasks)for(const a of t.assets){if(!urls.has(a.public_url))urls.set(a.public_url,[]);urls.get(a.public_url).push({task:t.id,file:a.filename});}
const previousPath=path.join(root,'verification/PUBLIC_ASSET_QA.json');
const previous=process.argv.includes('--retry-failed')&&fs.existsSync(previousPath)?JSON.parse(fs.readFileSync(previousPath)):null;
const results=previous?previous.results.filter(r=>r.status===200&&!r.redirected):[];
const good=new Set(results.map(r=>r.url));
const queue=[...urls.keys()].filter(url=>!good.has(url));let next=0,done=0;
const run=promisify(execFile);
async function check(url){let last;for(let attempt=0;attempt<3;attempt++){try{const {stdout}=await run('curl',['--silent','--show-error','--head','--max-time','20',url],{maxBuffer:64000});const lines=stdout.trim().split(/\r?\n/);const statuses=lines.filter(x=>x.startsWith('HTTP/'));const status=Number(statuses.at(-1)?.split(' ')[1]);const header=name=>lines.findLast(x=>x.toLowerCase().startsWith(name+':'))?.split(':').slice(1).join(':').trim();last={status,content_type:header('content-type'),bytes:Number(header('content-length')),redirected:status>=300&&status<400};if(status<429)break;}catch(e){last={status:0,error:e.code};}await new Promise(r=>setTimeout(r,(attempt+1)*800));}return {url,...last,uses:urls.get(url)};}
async function worker(){while(next<queue.length){const url=queue[next++];results.push(await check(url));done++;if(done%200===0)console.log(`${done}/${queue.length} public assets checked`);}}
await Promise.all(Array.from({length:12},worker));
results.sort((a,b)=>a.url.localeCompare(b.url));
const failed=results.filter(r=>r.status!==200||r.redirected);const report={checked_at:new Date().toISOString(),method:'Anonymous HTTP HEAD; read-only; no media content downloaded',asset_entries:tasks.reduce((s,t)=>s+t.assets.length,0),unique_urls:results.length,public_ok:results.length-failed.length,failed:failed.length,results};
fs.writeFileSync(path.join(root,'verification/PUBLIC_ASSET_QA.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({...report,results:failed.slice(0,3)}));if(failed.length)process.exitCode=1;
