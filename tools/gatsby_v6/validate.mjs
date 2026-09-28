import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const root=path.join(repo,'docs/gatsby-v6');
const old=path.join(repo,'docs/gatsby-v5');
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const preserved=JSON.parse(fs.readFileSync(path.join(root,'V5_PRESERVATION.json')));
for(const [p,h]of Object.entries(preserved.files))assert.equal(hash(fs.readFileSync(path.join(old,p))),h,`V5 modified: ${p}`);
const baseline=JSON.parse(fs.readFileSync(path.join(old,'index.html'),'utf8').match(/<script type="application\/json" id="data">([\s\S]*?)<\/script>/)[1]);
const tasks=baseline.tasks.map(t=>JSON.parse(execFileSync('unzip',['-p',path.join(root,'tasks',t.id,'TASK_PACKAGE.zip'),'TASK_SPEC.json'],{maxBuffer:15e6})));
assert.equal(tasks.length,100);
const ids=new Set(),issues=[],coverage=[];
for(const t of tasks){
 const original=baseline.tasks.find(x=>x.id===t.id);assert.deepEqual(t.assets,original.assets,t.id+' original assets changed');
 assert(!t.run,t.id+' inherited a completed run');assert.equal(t.revision.edition,'V6');
 const outputs=new Map(t.outputs.map(o=>[o.output_id,o]));assert.equal(outputs.size,t.outputs.length);
 const refNames=new Set(t.assets.map(a=>a.filename));
 for(const o of t.outputs){
  assert.equal(o.status,'not_executed');assert(!o.verification&&!o.artifact_url,'Stale output verdict');
  for(const source of o.asset_contract.source_files)assert(refNames.has(source.filename),t.id+' missing asset '+source.filename);
  if(o.source_image)assert(refNames.has(o.source_image));
  for(const p of o.page_sources||[]){assert(outputs.has(p.output_id));assert(p.output_id!==o.output_id);assert(p.page<=o.spec.pages);}
  for(const r of o.typography_contract){assert(Number.isFinite(parseFloat(r.resolved_size)),t.id+' size '+r.resolved_size);assert(Number.isFinite(parseFloat(r.resolved_leading)));}
  const checks=t.checks.filter(c=>c.output_id===o.output_id);assert(checks.some(c=>c.type==='auto'&&c.assertion?.op==='file_exists'),t.id+'/'+o.output_id+' missing file check');
  if(o.typography_contract.length)assert(checks.some(c=>c.category==='typography'));
  if(o.colour_contract.applicable)assert(o.page_sources?.length||checks.filter(c=>c.category==='colour').length>=5,t.id+'/'+o.output_id+' colour coverage');
  coverage.push({task:t.id,output_id:o.output_id,file:o.path,automatic:checks.filter(c=>c.type==='auto').length,human:checks.filter(c=>c.type==='human').length,type_roles:o.typography_contract.length,colour_contract:o.colour_contract.applicable,page_equivalence:(o.page_sources||[]).length});
 }
 for(const c of t.checks){
  assert(!ids.has(c.check_id),'Duplicate check '+c.check_id);ids.add(c.check_id);const o=outputs.get(c.output_id);assert(o,'Invalid output ref');
  assert.equal(c.artifact_file,path.basename(o.path));assert(c.check.includes(c.artifact_file),'Unnamed artifact');
  assert.equal(c.status,'not_assessed');assert(!c.answer&&!c.verified_at,'Inherited result');assert.deepEqual(c.allowed_answers,['Yes','No']);
  assert(!/\b(undefined|NaN|null)\b/.test(c.check),'Invalid check value');
  assert(!/^The delivery contains\b/.test(c.check),'Unsplit package completeness');
  for(const r of c.reference_assets)assert(refNames.has(r.filename)||r.filename.startsWith('V6 '),'Unresolvable reference '+r.filename);
  if(/\b(?:all (?:three|four|five|six|seven|eight|nine|ten|\d+)|every (?:card|file|output)|each (?:card|file|output)|all room rates|all rates)\b/i.test(c.check))issues.push({task:t.id,id:c.check_id,issue:'Check remaining batch/quantified wording',condition:c.check});
  if(c.check.length>440)issues.push({task:t.id,id:c.check_id,issue:'Long condition: move extended source copy into a separate expected-text reference',condition:c.check});
 }
 assert.equal(t.revision.decisions.length,2);
 for(const g of t.groups)assert.deepEqual(g.outputs,t.outputs.filter(o=>o.group_id===g.id).map(o=>o.output_id));
}
const get=id=>tasks.find(t=>t.id===id);
const count=(id,group)=>get(id).outputs.filter(o=>o.group_id===group).length;
assert.equal(count('MOTION-01','dish-callout'),3);assert.equal(count('MOTION-02','bowl-module'),8);assert.equal(count('MOTION-05','residence-hero'),8);assert.equal(count('MOTION-06','lesson-cover'),1);assert.equal(count('LAYOUT-25','producer-run'),11);
assert(get('PHOTO-04').outputs.filter(o=>o.group_id==='booking-hero').every(o=>o.source_record.values.Season==='High Summer'&&o.source_image));
assert(!get('MOTION-14').checks.some(c=>/voiceover.*audible|halden_recap_vo/.test(c.check)));
assert(!get('MOTION-18').checks.some(c=>c.check.includes('Friday, October 17, 2026')));
assert(get('MOTION-18').checks.some(c=>c.check.includes('Saturday, October 17, 2026')));
assert.equal(get('LAYOUT-03').brand.type_system.scale[0].family,'IBM Plex Mono Regular');
assert.equal(get('PHOTO-27').brand.type_system.scale[1].family,'Whitney Semibold');
assert(get('PHOTO-18').outputs.every(o=>o.typography_contract.length===0));
assert(get('PHOTO-06').outputs.every(o=>o.typography_contract.length===0));
assert.deepEqual(get('MOTION-10').outputs.filter(o=>o.group_id==='short-cover').map(o=>o.source_record.values.Episode),['2','5','8']);
assert(!get('MOTION-10').checks.some(c=>/interview-short-idea-\d\.mp4/.test(c.check)));
assert(get('MOTION-06').outputs.find(o=>o.output_id==='lesson').approved_copy_records.some(r=>r.text==='Post each movement once, in date order. One line, one cause.'));
assert.equal(get('MOTION-14').outputs.filter(o=>o.group_id==='episode-cover'&&o.source_record&&o.source_image).length,3);
assert(get('PHOTO-04').checks.filter(c=>c.category==='seasonal rate'&&c.output_id==='villa-collection').length===9);
assert.equal(get('LAYOUT-11').brand.type_system.scale[0].tracking,'0 em');
assert(get('LAYOUT-26').brand.type_system.scale.every(s=>s.tracking==='0 em'));
const report={status:'structural checks passed',tasks:tasks.length,outputs:coverage.length,checks:ids.size,duplicate_check_ids:0,invalid_output_references:0,old_assets_unchanged:true,v5_files_preserved:Object.keys(preserved.files).length,inherited_pass_results:0,regression_checks:'passed',wording_review_candidates:issues.length,not_claimed:['New task executions','Connector feasibility certification','Independent visual approval of source media or future deliverables']};
fs.mkdirSync(path.join(root,'verification'),{recursive:true});
fs.writeFileSync(path.join(root,'verification/CONTRACT_VALIDATION.json'),JSON.stringify(report,null,2)+'\n');
fs.writeFileSync(path.join(root,'verification/OUTPUT_COVERAGE.json'),JSON.stringify(coverage,null,2)+'\n');
fs.writeFileSync(path.join(root,'verification/WORDING_REVIEW.json'),JSON.stringify(issues,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
console.log(JSON.stringify(issues.slice(0,15),null,2));
