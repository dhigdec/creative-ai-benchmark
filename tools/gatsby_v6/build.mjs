import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {gzipSync} from 'node:zlib';
import os from 'node:os';

const here=path.dirname(fileURLToPath(import.meta.url));
const repo=path.resolve(here,'../..');
const old=path.join(repo,'docs/gatsby-v5');
const dest=path.join(repo,'docs/gatsby-v6');
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const baseline=fs.readFileSync(path.join(old,'index.html'),'utf8');
const original=JSON.parse(baseline.match(/<script type="application\/json" id="data">([\s\S]*?)<\/script>/)[1]);
const decisions=JSON.parse(fs.readFileSync(path.join(here,'task-decisions.json')));
const craft=JSON.parse(fs.readFileSync(path.join(here,'craft-constraints.json')));
const sourceCache=path.join(here,'source-text.json');
if(!fs.existsSync(sourceCache))fs.copyFileSync('/tmp/gatsby-deep-sources.json',sourceCache);
const sources=JSON.parse(fs.readFileSync(sourceCache));
const csvInput=sources.filter(s=>s.file.endsWith('.csv')).map(s=>({id:s.task+'/'+s.file,text:s.text}));
const tables=JSON.parse(execFileSync('python3',['-c','import csv,io,json,sys; x=json.load(sys.stdin); print(json.dumps({a["id"]:list(csv.DictReader(io.StringIO(a["text"]))) for a in x},ensure_ascii=False))'],{input:JSON.stringify(csvInput),encoding:'utf8',maxBuffer:30e6}));
const clone=x=>JSON.parse(JSON.stringify(x));
const file=o=>path.basename(o.path);
const imageName=x=>/\.(png|jpe?g|webp|tiff?|heic)$/i.test(x);
const mediaName=x=>/\.(png|jpe?g|webp|tiff?|heic|svg|pdf|mov|mp4|webm|wav|mp3|m4a)$/i.test(x);
const slug=x=>String(x).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
const getSource=(id,name)=>sources.find(s=>s.task===id&&s.file===name)?.text||'';
const taskById=id=>original.tasks.find(t=>t.id===id);
const sourceRef=(t,name)=>{const a=t.assets.find(a=>a.filename===name);return a?{filename:name,url:a.public_url}:null;};
function treeHashes(root){const result={};function walk(p){for(const d of fs.readdirSync(p,{withFileTypes:true})){const f=path.join(p,d.name);if(d.isDirectory())walk(f);else result[path.relative(root,f)]=hash(fs.readFileSync(f));}}walk(root);return result;}
const protectedBefore=treeHashes(old);
fs.mkdirSync(dest,{recursive:true});
const changeLog=[];
const log=(t,category,detail)=>{t.revision.changes.push({category,detail});changeLog.push({task_id:t.id,category,detail});};
function record(table,row,values){return {table,row_number:row,values:clone(values),raw_values:clone(values)};}
function addOutput(t,{id,group,name,spec,source_record=null,source_image=null,content=[]}){
 assert(!t.outputs.some(o=>o.output_id===id),'Duplicate output '+t.id+'/'+id);
 const o={output_id:id,group_id:group,name,path:`deliverables/${id}.${spec.format}`,kind:spec.format==='mp4'?'video':spec.format==='pdf'?'document':'image',spec,source_record,source_image,required_content:content,acceptance_requirements:content,expert_review_criteria:[],status:'not_executed',added_in:'V6'};
 t.outputs.push(o);if(!t.groups.some(g=>g.id===group))t.groups.push({id:group,name,outputs:[],requirements:content});
 log(t,'scope',`Registered ${o.path}: ${name}.`);return o;
}
function addTechnical(t,o){
 const checks=[['file_exists',null,`${file(o)} is present.`],['decodable',o.spec.format,`${file(o)} opens as a valid ${o.spec.format.toUpperCase()} file.`]];
 for(const [k,unit]of [['width','pixels wide'],['height','pixels high'],['pages','pages'],['width_mm','mm wide'],['height_mm','mm high']])if(o.spec[k])checks.push([k,o.spec[k],`${file(o)} is ${o.spec[k]} ${unit}${k.endsWith('_mm')?' (within 0.2 mm)':''}.`]);
 for(const [op,value,condition]of checks)t.checks.push({output_id:o.output_id,type:'auto',condition,assertion:{op,equals:value,...(op.endsWith('_mm')?{tolerance:0.2}:{})},category:'file specification',reference_assets:[]});
}
function human(t,o,condition,{category='content',refs=[],requirement_id=null,element=null,page=null,evidence=null,expected_text=null}={}){
 t.checks.push({output_id:o.output_id,type:'human',condition:condition.startsWith(file(o))?condition:`${file(o)}${page?`, page ${page}`:''}: ${condition}`,category,reference_assets:refs.filter(Boolean),requirement_id,element,page,evidence,expected_text});
}
function resolveBrand(t){
 const b=t.brand,s=b.type_system.scale,r=b.type_system.rules;
 b.contract_version=`V6/${t.id}`;
 b.authority='This commission-specific V6 brand card governs newly authored design elements. Earlier source documents remain factual/artwork references; a V6 amendment resolves a named conflict. Values first introduced by a prior type card are adopted as benchmark production defaults, not attributed to the original client.';
 b.original_typography=b.typography;
 if(t.id==='LAYOUT-03'){
  Object.assign(s[0],{family:'IBM Plex Mono Regular',weight:'Regular',note:'Concentration. Exactly twice the product-name size. Numeric type is Plex Mono, not Spectral.'});
  r.splice(0,r.length,...r.filter(x=>!x.includes('Spectral Medium 500 sets')),'Spectral Medium 500 sets the wordmark and product names. Concentration and other figures use IBM Plex Mono Regular.');
 }
 if(t.id==='PHOTO-27')Object.assign(s[1],{family:'Whitney Semibold',weight:'Semibold',note:'Supporting subhead. Flavour names keep the separate two-line display treatment.'});
 if(t.id==='PHOTO-11'){
  Object.assign(s[0],{family:'Abril Fatface Regular',size:'32 pt',leading:'34 pt',note:'The 55 by 85 mm card uses a lowercase shade name at 32 pt on 34 pt; preserve spaces and wrap between words if needed. Screen baseline: 96 px on 102 px.'});
  b.signature_type_move='Lowercase shade names preserve their approved spaces; numbers use Söhne Mono.';
  r.splice(0,r.length,...r.filter(x=>!/(five times|one lowercase word|96 pt)/i.test(x)),'A shade name retains the approved words and spaces, rendered in lowercase. Print baseline is 32 pt on 34 pt; screen baseline is 96 px on 102 px.');
 }
 if(t.id==='LAYOUT-11'){
  Object.assign(s[0],{tracking:'0 em',note:'Names are flush left and may wrap at word boundaries inside safe margins. Keep the 3 pt Ember Red rule beneath the name. Poster names use 240 px on 250 px.'});
  s[1].note='Public Sans sets roles and access labels. The role table governs size and tracking; no forced justification.';
  r.splice(0,r.length,...r.filter(x=>!/force justified|trim edges|Never let a performer name wrap/.test(x)),'Names are flush left with 0 em tracking, wrapping at word boundaries inside safe margins. A 3 pt Ember Red rule sits below the name.');
  b.signature_type_move=b.type_system.signature_move='Large Syne Extra names sit flush left above a 3 pt Ember Red rule, inside safe margins. Names can wrap; the full approved name must remain visible.';
 }
 if(t.id==='LAYOUT-18')for(let i=0;i<r.length;i++)r[i]=r[i].replace(/11 pt[^.]*every format[^.]*/gi,'11 pt in print and 15 px on screen before format scaling');
 if(t.id==='LAYOUT-26'){for(const st of s)st.tracking='0 em';for(let i=0;i<r.length;i++)if(/tracking/i.test(r[i])&&/zero|0|negative/i.test(r[i]))r[i]='Text tracking is exactly 0 em; negative tracking is not allowed.';}
 if(t.id==='LAYOUT-34'){
  for(let i=0;i<r.length;i++)r[i]=r[i].replace(/at exactly 54 percent of its size/gi,'at 15 pt below a 28 pt common name on the large tag, or 9 pt below a 14 pt common name on a department tag');
  s[1].note='Botanical Latin below the common name. Large tag 15 pt on 17 pt; department tag 9 pt on 11 pt. Explicit sizes govern; no exact percentage ratio applies.';
 }
 if(t.id==='VECTOR-13')for(let i=0;i<r.length;i++)r[i]=r[i].replace(/Never outline Marian[^.]*/i,'Do not add a decorative outline effect to Marian; conversion to filled vector paths is permitted');
 if(t.id==='VECTOR-15')for(let i=0;i<r.length;i++)r[i]=r[i].replace(/oldstyle figures/gi,'the source Roman letterforms when the date is MCMXI');
 if(t.id==='MOTION-19'){
  for(let i=0;i<r.length;i++)r[i]=r[i].replace('scenario titles in Regular, and nothing else','scenario titles and scenario numerals in Regular');
  for(const st of s)st.note=st.note.replace('The school name is the only other Baskerville setting','The school name is the other Baskerville setting besides scenario titles and numerals').replace('reserved for the school name and scenario titles','reserved for the school name, scenario titles and scenario numerals');
  r.push('Step instructions use Inter.');
 }
 if(t.id==='PHOTO-11')b.type_system.signature_move=b.signature_type_move;
 if(t.id==='PHOTO-27')b.type_system.signature_move=b.signature_type_move;
 if(t.id==='LAYOUT-03')for(const obj of [b,b.type_system])for(const k of ['signature_type_move','signature_move'])if(obj[k])obj[k]=obj[k].replaceAll('set in Spectral Medium','set in IBM Plex Mono Regular');
 if(t.id==='LAYOUT-11')for(const obj of [b,b.type_system])for(const k of ['signature_type_move','signature_move'])if(obj[k])obj[k]=obj[k].replaceAll('trim edges','safe-margin edges');
 if(t.id==='LAYOUT-18')for(const obj of [b,b.type_system])for(const k of ['signature_type_move','signature_move'])if(obj[k])obj[k]=obj[k].replace('always 11 pt','11 pt in print or 15 px on screen before uniform format scaling, in');
 if(t.id==='LAYOUT-34')for(const obj of [b,b.type_system])for(const k of ['signature_type_move','signature_move'])if(obj[k])obj[k]='Common/Latin name sizes are 28/15 pt on large tags and 14/9 pt on department tags. Latin follows the common name on the next baseline. Only the botanical Latin is italic.';
 for(const st of s)st.note=(st.note||'').replace(/(?:Size|Leading|Tracking|Size and tracking) (?:not stated[^.]*|supplied)[.]?/gi,'V6 production default.').replace(/No size existed[^.]*\./gi,'V6 production default.');
 b.typography=s.map(st=>`${st.role}: ${st.family}; ${st.weight}; ${st.size} on ${st.leading}; tracking ${st.tracking}. ${st.note||''}`).join('\n');
 b.type_system.rules=r;
 const repeat={ 'PHOTO-02':'Spring counter-card campaign','LAYOUT-02':'Cold-case retail system','PHOTO-04':'Direct-booking image campaign','LAYOUT-08':'In-villa seasonal collateral','PHOTO-10':'Ecommerce apparel campaign','LAYOUT-04':'Wholesale print collection','PHOTO-12':'Consumer ceramic campaign','LAYOUT-18':'Wholesale relaunch','LAYOUT-11':'Performer credentials','LAYOUT-26':'Programme and wayfinding'};
 if(repeat[t.id])b.commission_identity=`${repeat[t.id]}: this is a commission-specific identity edition, not an implicit replacement for the other task's palette or typography.`;
 log(t,'typography','Made this task\'s corrected role table authoritative; kept source lettering separate from newly authored type.');
}
function scopeAdditions(t){
 const png=(w,h)=>({format:'png',width:w,height:h});
 const pdf=(w,h,p=1)=>({format:'pdf',width_mm:w,height_mm:h,pages:p});
 if(t.id==='MOTION-01'){
  addOutput(t,{id:'reel-cover',group:'reel-cover',name:'Second room reel cover',spec:png(1080,1920),source_image:'emberoak_hero_pass.jpg',content:['Second room now open','Book a table']});
  addOutput(t,{id:'window-poster',group:'window-poster',name:'Second room window poster',spec:pdf(420,594),source_image:'emberoak_hero_safety.jpg',content:['Second room now open','Book a table']});
  const txt=getSource(t.id,'emberoak_menu_callouts.txt');
  t.revision.content_sources.push({filename:'emberoak_menu_callouts.txt',text:txt});
  const dishes=[...txt.matchAll(/^(.+) - (\d+)\n([^\n]+)\n(Allergens: [^\n]+)/gm)];assert.equal(dishes.length,4);
  for(let i=1;i<=3;i++){const [,name,price,description,allergen]=dishes[i-1];addOutput(t,{id:`dish-callout-${i}`,group:'dish-callout',name:`Dish callout - ${name}`,spec:png(1080,1350),source_record:record('emberoak_menu_callouts.txt',i,{Dish:name,Price:`$${price}`,Allergens:allergen}),content:[`${name} - $${price}`,allergen]});}
 }
 if(t.id==='MOTION-02'){
  const rows=tables[t.id+'/ironwood_skus.csv'];assert(rows.length>=8);
  for(let i=0;i<8;i++)addOutput(t,{id:`bowl-module-${String(i+1).padStart(2,'0')}`,group:'bowl-module',name:`Lunch bowl product module - ${Object.values(rows[i])[0]}`,spec:png(1440,1800),source_record:{...record('ironwood_skus.csv',i+2,{...rows[i],Price:'$12'}),raw_values:clone(rows[i])},source_image:`ironwood_bowls_${String(i+1).padStart(2,'0')}.jpg`,content:['Complete bowl in frame.','No reference card.','Price $12.']});
  addOutput(t,{id:'lunch-line-sheet',group:'lunch-line-sheet',name:'Lunch range line sheet',spec:pdf(210,297,2),content:['Eight bowl names and their approved SKU data in source order; four bowls per page.']});
  addOutput(t,{id:'film-cover',group:'film-cover',name:'Ironwood lunch film cover',spec:png(1920,1080),source_image:'ironwood_bowls_01.jpg',content:['Ironwood Kitchen','$12']});
 }
 if(t.id==='MOTION-05'){
  for(let i=1;i<=8;i++)addOutput(t,{id:`residence-hero-${String(i).padStart(2,'0')}`,group:'residence-hero',name:`Blue-hour residence hero ${i}`,spec:png(1920,1080),source_image:`sterlingrow_residence_still_${String(i).padStart(2,'0')}.jpg`,content:['Truthful residence view; no fabricated feature.']});
  addOutput(t,{id:'viewing-brochure',group:'viewing-brochure',name:'Sterling Row viewing brochure',spec:pdf(210,297,6),content:['Development cover; approved residence facts; viewing action.','Viewings by appointment.']});
  addOutput(t,{id:'residence-film-cover',group:'residence-film-cover',name:'Sterling Row film cover',spec:png(1920,1080),source_image:'sterlingrow_residence_still_01.jpg',content:['Sterling Row','Viewings by appointment.']});
 }
 if(t.id==='MOTION-06')addOutput(t,{id:'lesson-cover',group:'lesson-cover',name:'Lesson 4 course cover',spec:png(1920,1080),content:['Lesson 4','Reconciling the Numbers','Operations Analytics for Working Managers']});
 if(t.id==='LAYOUT-25'){
  const individuals=t.outputs.filter(o=>o.source_record);const names=[...new Set(individuals.map(o=>o.source_record.values.Producer))];assert.equal(names.length,11);
  for(const name of names){const members=individuals.filter(o=>o.source_record.values.Producer===name);const o=addOutput(t,{id:'producer-run-'+slug(name),group:'producer-run',name:`Producer mailing file - ${name}`,spec:pdf(210,297,members.length),content:[`Only ${name}'s households, in approved source-row order.`]});o.page_sources=members.map((x,i)=>({page:i+1,output_id:x.output_id,source_page:1}));}
 }
}
function correctedFacts(t){
 if(t.id==='MOTION-01')for(const o of t.outputs.filter(o=>['reel-cover','window-poster'].includes(o.output_id)))o.approved_copy_records=['Second room now open','Book a table'].map((text,i)=>({field:i?'Booking action':'Headline',text,source:'',row_number:i+1}));
 if(t.id==='MOTION-02'){
  const rows=tables[t.id+'/ironwood_skus.csv'].slice(0,8);
  const sheet=t.outputs.find(o=>o.output_id==='lunch-line-sheet');
  sheet.page_content=rows.map((r,i)=>({page:Math.floor(i/4)+1,subject:r['Bowl Name'],source_file:r.Image,fields:{'Bowl Name':r['Bowl Name'],Price:'$12',Macros:r.Macros,Allergens:r.Allergens}}));
  sheet.required_content=['Pages 1 and 2 show bowls 1-4 and 5-8 respectively, in ironwood_skus.csv order. A bowl entry contains its named photo, bowl name, $12 price, full macro line and full allergen line. The long description is not printed in the line sheet.'];
  t.outputs.find(o=>o.output_id==='film-cover').approved_copy_records=['Ironwood Kitchen','$12'].map((text,i)=>({field:i?'Price':'Name',text,source:'ironwood_skus.csv',row_number:i+1}));
 }
 if(t.id==='MOTION-05'){
  const brochure=t.outputs.find(o=>o.output_id==='viewing-brochure'),rows=tables[t.id+'/sterlingrow_units.csv'];
  brochure.page_content=rows.map((r,i)=>({page:Math.floor(i/3)+2,subject:r.Unit,source_file:null,fields:Object.fromEntries(Object.entries(r).filter(([k])=>k!=='Picture'))}));
  const note=getSource(t.id,'sterlingrow_brand_note.txt');
  const disclosures=[...note.matchAll(/DISCLOSURE [12]: "([^"]+)"/g)].map(m=>m[1]);assert.equal(disclosures.length,2);
  brochure.required_content=['Page 1: Sterling Row and Nine residences. No hurry., with sterlingrow_residence_still_08.jpg.','Pages 2-4: three unit records per page, in sterlingrow_units.csv order; typography-led factual entries, no invented unit photograph. Include both full disclosure lines on each of these pages.','Page 5: Nine residences. Full floor. Sold one at a time, to buyers in no hurry., with sterlingrow_residence_still_04.jpg.','Page 6: Viewings by appointment. and both full disclosure lines.'];
  brochure.approved_copy_records=[{field:'Cover title',text:'Sterling Row',page:1},{field:'Tagline',text:'Nine residences. No hurry.',page:1},{field:'Development statement',text:'Nine residences. Full floor. Sold one at a time, to buyers in no hurry.',page:5},{field:'Viewing action',text:'Viewings by appointment.',page:6},...[2,3,4,6].flatMap(page=>disclosures.map((text,i)=>({field:`Disclosure ${i+1}`,text,page})))].map((r,i)=>({...r,source:'sterlingrow_brand_note.txt',row_number:i+1}));
  t.outputs.find(o=>o.output_id==='residence-film-cover').approved_copy_records=['Sterling Row','Viewings by appointment.'].map((text,i)=>({field:i?'Viewing action':'Name',text,source:'',row_number:i+1}));
 }
 if(t.id==='PHOTO-04'){
  const rows=tables[t.id+'/rates_2027.csv'];const names={oliveto:'Casa Oliveto',scogliera:'Casa Scogliera',verranza:'Casa Verranza'};
  for(const o of t.outputs.filter(o=>o.group_id==='booking-hero')){
   const key=o.output_id.replace('booking-hero-','');const i=rows.findIndex(r=>r.House===names[key]&&r.Season==='S2');const values={...rows[i],Season:'High Summer',Sleeps:key==='scogliera'?'10':rows[i].Sleeps,Photo:key==='scogliera'?'scogliera_terrace.jpg':`${key}_pool.jpg`};
   o.source_record={...record('rates_2027.csv',i+2,values),raw_values:clone(rows[i])};o.source_image=values.Photo;o.required_content=[values.House,'High Summer',`EUR ${values['Nightly Rate (EUR)']} per night`,'7-night minimum','Book direct'];
  }
  t.revision.approved_records=rows.map((r,i)=>({row_number:i+2,values:{...r,Season:{S1:'Spring',S2:'High Summer',S3:'Autumn'}[r.Season],Sleeps:r.House==='Casa Scogliera'?'10':r.Sleeps,Photo:r.House.replace('Casa ','').toLowerCase()+'_pool.jpg'}})).filter(r=>r.values.House!=='Casa Fienile');
 }
 if(t.id==='MOTION-18'){
  const replace=x=>typeof x==='string'?x.replaceAll('Friday, October 17, 2026','Saturday, October 17, 2026'):Array.isArray(x)?x.map(replace):x&&typeof x==='object'?Object.fromEntries(Object.entries(x).map(([k,v])=>[k,replace(v)])):x;
  t.outputs=replace(t.outputs);t.checks=replace(t.checks);
  t.revision.approved_copy={date:'Saturday, October 17, 2026',authority:'V6 preserves the numeric event date and corrects the weekday.'};
 }
 const episodeSource={'MOTION-10':'daydrift_season4.csv'}[t.id];
 if(episodeSource){const rows=tables[t.id+'/'+episodeSource];const covers=t.outputs.filter(o=>o.group_id==='short-cover');covers.forEach((o,i)=>{const ep=[2,5,8][i],index=rows.findIndex(r=>Number(r.Episode)===ep);o.source_record=record(episodeSource,index+2,rows[index]);o.source_image=`daydrift_ep${String(ep).padStart(2,'0')}.mp4`;o.name=`Episode ${ep} cover - ${rows[index].Title}`;o.required_content=[rows[index].Title,rows[index].Guest,rows[index]['Recording Date'],rows[index]['Sponsor Line']];});}
 if(t.id==='MOTION-06'){
  const rows=tables[t.id+'/meridian_captions.csv'];t.revision.approved_teaching_rows=['12:05','14:20'].map(tc=>{const i=rows.findIndex(r=>r.Timecode===tc);assert(i>=0);return record('meridian_captions.csv',i+2,rows[i]);});
  for(const o of t.outputs.filter(x=>x.spec.format==='mp4'))o.approved_copy_records=(o.output_id==='lesson'?t.revision.approved_teaching_rows:t.revision.approved_teaching_rows.slice(1)).map(r=>({field:'Teaching card',text:r.values.Caption,source:r.table,row_number:r.row_number}));
  t.outputs.find(o=>o.output_id==='lesson-cover').approved_copy_records=['Lesson 4','Reconciling the Numbers','Operations Analytics for Working Managers'].map((text,i)=>({field:['Lesson label','Topic','Course name'][i],text,source:'meridian_lesson4_outline.txt',row_number:i+1}));
 }
 if(t.id==='MOTION-14'){
  const episodes=[...getSource(t.id,'halden_episode_copy.txt').matchAll(/^(\d+)\. (.+)\n\s+Published: (.+)\n\s+Standfirst: (.+)/gm)];assert.equal(episodes.length,8);
  t.outputs.filter(o=>o.group_id==='episode-cover').forEach((o,i)=>{const [,number,title,date,standfirst]=episodes[i];o.source_record=record('halden_episode_copy.txt',i+1,{Title:title,'Published date':date,Standfirst:standfirst,'Channel URL':'www.haldendiaries.tv'});o.source_image=`halden_still_0${number}.jpg`;o.name=`Episode ${number} cover - ${title}`;o.required_content=[title,date,standfirst,'www.haldendiaries.tv'];});
 }
}
function rawOutput(t,o){
 return ['PHOTO-06','PHOTO-18'].includes(t.id)||['sku-cutout','clinical-lead','residence-hero'].includes(o.group_id)||(['svg'].includes(o.spec.format)&&!['machine-plate','door-plate','release-label','pack-label'].includes(o.group_id));
}
function makePageSources(t){
 for(const o of t.outputs){
  if(o.page_sources)continue;
  const peers=t.outputs.filter(x=>x.group_id===o.group_id&&x.output_id!==o.output_id&&x.spec.pages===1&&x.source_record);
  if(o.spec.format==='pdf'&&o.spec.pages>1&&o.spec.pages===peers.length&&!o.source_record){o.page_sources=peers.map((x,i)=>({page:i+1,output_id:x.output_id,source_page:1}));}
 }
}
function bindAssets(t,o){
 const relevant=t.checks.filter(c=>c.output_id===o.output_id);
 const direct=[...new Set(relevant.flatMap(c=>c.reference_assets||[]).map(a=>a.filename).filter(imageName))];
 let selected=o.source_image||null;
 if(!selected&&direct.length===1)selected=direct[0];
 if(t.id==='LAYOUT-25'&&o.source_record){const p=slug(o.source_record.values.Producer).replaceAll('-','_');selected=t.assets.find(a=>a.filename.endsWith('/'+p+'.jpg'))?.filename||null;}
 if(selected)assert(t.assets.some(a=>a.filename===selected),'Missing selected source '+t.id+'/'+selected);
 const eligible=t.assets.filter(a=>a.state!=='superseded_retained_for_provenance'&&mediaName(a.filename));
 const candidates=(direct.length?direct:eligible.filter(a=>imageName(a.filename)||/\.(mov|mp4|webm)$/i.test(a.filename)).map(a=>a.filename));
 o.source_image=selected;
 o.asset_contract={
  selection:selected?'fixed':'bounded creative choice',
  source_files:(selected?[selected]:candidates).map(n=>sourceRef(t,n)).filter(Boolean),
  supporting_files:eligible.filter(a=>!candidates.includes(a.filename)&&a.filename!==selected).map(a=>sourceRef(t,a.filename)),
  subject:o.source_record?Object.entries(o.source_record.values).filter(([k])=>!/photo|path|file|image/i.test(k)).slice(0,2).map(([k,v])=>`${k}: ${v}`).join('; '):o.name,
  selection_rule:selected?`Use ${selected}. Cropping is allowed only while the required subject/details remain visible.`:`Choose from the individually named source files for ${o.name}. Match the named subject/record; an unrelated person, product, property or event is not an allowed alternative. Record the exact file for each image slot/page/time range in the source handoff. A missing matching image uses a typography-led layout only where this task's amendment permits it; otherwise report a source limitation.`,
  permission_rule:'Task exclusions and consent/licensing restrictions take precedence over an asset appearing in this list.'
 };
}
function colourContract(t,o){
 if(rawOutput(t,o))return {applicable:false,reason:'Source media or recovered artwork: no new graphic palette is imposed. Follow source-fidelity and production-ink requirements instead.'};
 const colours=t.brand.palette;const luminance=p=>{const x=p.hex.replace('#','');return .2126*parseInt(x.slice(0,2),16)+.7152*parseInt(x.slice(2,4),16)+.0722*parseInt(x.slice(4,6),16);};
 const sorted=[...colours].sort((a,b)=>luminance(a)-luminance(b));
 return {applicable:true,allowed:colours,mandatory_roles:{default_text:sorted[0],default_light_ground:sorted.at(-1)},optional:colours.filter(x=>x!==sorted[0]&&x!==sorted.at(-1)),distribution:'Default body/fine-print text uses the darkest palette colour on a light palette ground. Reverse that pair for a dark-ground design. Explicit named element colours in the task rules override this default. Other palette colours are optional accents, not a requirement to use the entire palette.',opacity_percent:100,tints:false,gradients:false,blending_mode:'normal',exceptions:'Photographs, original artwork, physical substrate colour, source-media lighting, transparency cutouts and antialiased edge pixels are not palette swatches. A supplied physical ink specification overrides a screen HEX preview for production ink.',inspection:'Compare authored fill/stroke settings in the editable source. For raster exports inspect solid interior pixels in sRGB, allowing 2/255 per channel for rounding; do not sample antialiased edges. Print uses the declared colour-managed conversion, not literal RGB pixel equality.'};
}
function formatRoles(t,o){
 if(rawOutput(t,o)||o.page_sources)return [];
 let scale=clone(t.brand.type_system.scale);
 if(t.id==='VECTOR-14')scale=scale.filter(s=>!s.family.includes('hand drawn numerals'));
 if(t.id==='MOTION-20'&&o.group_id!=='studio-service'){
  if(/lunara/i.test(o.name))scale=clone(taskById('PHOTO-24').brand.type_system.scale);
  else scale=[{role:'Added client headline',family:'Inter Medium',weight:'Medium',size:'48 px',leading:'56 px',tracking:'0 em',note:'Existing client wordmark stays artwork.'},{role:'Added client caption / price',family:'Inter Regular',weight:'Regular',size:'24 px',leading:'32 px',tracking:'0 em',note:'Neutral V6 caption system. Studio Engravers is not used.'}];
 }
 return scale.map((s,i)=>{
  const unit=o.spec.format==='pdf'?'pt':'px';const sourceUnit=s.size.includes('pt')?'pt':'px';
  const base=parseFloat(s.size),leading=parseFloat(s.leading),factor=sourceUnit===unit?1:unit==='pt'?0.75:3*Math.min(o.spec.width||1080,o.spec.height||1080)/1080;
  let size=base*factor,space=leading*factor;
  if(sourceUnit!==unit){const explicit=(s.note||'').match(new RegExp('([0-9.]+) '+unit+'(?: on ([0-9.]+) '+unit+')?'));if(explicit){size=Number(explicit[1]);space=explicit[2]?Number(explicit[2]):size*(leading/base);}else if(unit==='px'&&i>=2){size=Math.max(size,24*factor/3);space=size*(leading/base);}}
  if(t.id==='LAYOUT-34'&&o.group_id==='department-run'){if(i===0){size=14;space=16;}if(i===1){size=9;space=11;}}
  if(o.output_id==='lunch-line-sheet'){[size,space]=[[24,28],[12,14],[10,14],[9,12]][i]||[size,space];}
  if(o.output_id==='viewing-brochure'){[size,space]=[[30,34],[18,22],[10.5,15],[8,11]][i]||[size,space];}
  const n=parseFloat(String(s.tracking).replace(/minus /i,'-').replace(/plus /i,''));
  const em=Number.isFinite(n)?(/\bem\b/.test(s.tracking)?n:n/1000):null;
  return {...s,role_id:`role-${i+1}`,resolved_size:`${Number(size.toFixed(2))} ${unit}`,resolved_leading:`${Number(space.toFixed(2))} ${unit}`,resolved_tracking:em===null?s.tracking:`${em} em`,applicability:'Style rule for this role when present. A role not required by the content plan may be omitted; its absence passes the style-only check, not a separate required-content check.',format_policy:'The resolved size/leading in this output table are the V6 values. They supersede a reference-scale example for another format. Wrap at word boundaries instead of cutting required text. Source artwork lettering is not retypeset.',format_factor:formatFactor(o,s),reference_size:s.size,reference_leading:s.leading};
 });
}
function formatFactor(o,s){
 const print=o.spec.format==='pdf';const unit=String(s.size).includes('pt')?'pt':'px';
 if(print&&unit==='px')return {factor:0.75,conversion:'px to pt at the V6 reference of 96 px per inch; an explicit print equivalent in the role note overrides this conversion.'};
 if(!print&&unit==='pt')return {factor:3*Math.min(o.spec.width||1080,o.spec.height||1080)/1080,conversion:'V6 screen adaptation: 3 px per print point at a 1080 px short edge, scaled to the actual short edge. Body and fine print have a 24 px baseline minimum. An explicit screen equivalent in the role note overrides this default.'};
 return {factor:1,conversion:'Use the supplied unit without conversion; explicit format-specific notes take precedence.'};
}
function craftApplies(t,o,p){
 if(o.page_sources)return false;
 const g=o.group_id,video=o.spec.format==='mp4',svg=o.spec.format==='svg';
 if(/print PDF/i.test(p)&&o.spec.format!=='pdf')return false;
 if(t.id==='VECTOR-12'&&/distinct layer/.test(p)&&!svg)return false;
 if(/wall label|Wall-label/.test(p)&&g!=='wall-label')return false;
 if(/Campaign poster\/feed\/story/.test(p)&&!['campaign-poster','campaign-feed','campaign-story'].includes(g))return false;
 if(/video|film|frames|closing card/i.test(p)&&!video&&t.id.startsWith('MOTION'))return false;
 if(/cover title|cover date|cover URL|episode cover/i.test(p)&&!g.includes('cover'))return false;
 if(/paper-bib/.test(p)&&g!=='member-bib')return false;
 if(/heat-transfer/.test(p)&&!['number','letter'].includes(g))return false;
 if(/department subset/.test(p)&&g!=='department-run')return false;
 if(/gang-sheet/.test(p)&&g!=='gang-sheet')return false;
 if(/shelf-ink|production ink|production tint|production gradient|production artwork/i.test(p)&&!svg&&t.id.startsWith('VECTOR'))return false;
 if(/studio service heading/.test(p)&&g!=='studio-service')return false;
 if(/unavailable product cell/.test(p)&&g!=='campaign-board')return false;
 if(/garment discharge/.test(p)&&!['graphics-sheet','lookbook'].includes(g))return false;
 if(/before photograph/.test(p)&&g!=='case-study')return false;
 if(/dish tile/.test(p)&&g!=='menu-tile')return false;
 if(rawOutput(t,o)&&/type|text|font|tracking|headline|wordmark text|price|numeric|caption|italic|rule is|rule below|rule under/i.test(p)&&!['PHOTO-06','PHOTO-18'].includes(t.id))return false;
 return true;
}

function migrateChecks(t,oldChecks){
 const staleType=/\b(typeface|serif|sans|font family|Tiempos|Frutiger|headline font|caption font|font is)\b/i;
 const typeExceptions=/wordmark.*sans|mark.*sans/i;
 const oldRunFields=['answer','status','verified_at','artifact_url','evidence_reference'];
 const seen=new Set();let retired=0;
 for(const oldCheck of oldChecks){
  const o=t.outputs.find(o=>o.output_id===oldCheck.output_id);if(!o)continue;
  let condition=oldCheck.check||oldCheck.pass_condition||oldCheck.requirement||'';
  if(/^The delivery contains\b/.test(condition)){retired++;continue;}
  if(oldCheck.type==='human'&&staleType.test(condition)&&!typeExceptions.test(condition)){retired++;continue;}
  if(t.id==='MOTION-14'&&/voiceover.*audible|halden_recap_vo/i.test(condition)){retired++;continue;}
  if(['MOTION-09','MOTION-10'].includes(t.id)&&/alarm chirp|sponsor read|spoken|dialogue|interview audio/i.test(condition)){retired++;continue;}
  if(t.id==='MOTION-11'&&/condensed/.test(condition)){retired++;continue;}
  if(t.id==='PHOTO-11'&&/one lowercase word|five times|96 pt/.test(condition)){retired++;continue;}
  if(t.id==='PHOTO-11'&&/Amber Hour/.test(condition)&&/concept-colour notice/.test(condition)){retired++;continue;}
  if(t.id==='MOTION-06')condition=condition.replace('the largest text on screen','the largest informational text on screen, excluding the decorative lesson numeral,').replace('larger than every other line in its frame','larger than the other instructional lines in its frame, excluding the decorative lesson numeral');
  if(t.id==='MOTION-10'&&/interview-short-idea-\d\.mp4/.test(condition)){retired++;continue;}
  if(t.id==='PHOTO-04'&&/Each villa identity|Every rate|season labels.*Spring|approved rate in rates/.test(condition)){retired++;continue;}
  if(t.id==='MOTION-18')condition=condition.replaceAll('Friday, October 17, 2026','Saturday, October 17, 2026');
  let split=null;
  if(t.id==='PHOTO-11'&&/All seven approved shade names/.test(condition))split=t.outputs.filter(x=>x.group_id==='shade-card'&&x.source_record).map(x=>`${file(o)} shows the shade name ${JSON.stringify(Object.entries(x.source_record.values).find(([k])=>/shade.*name|^shade$/i.test(k))?.[1]||x.name.replace(/^.* - /,''))}.`);
  if(t.id==='PHOTO-25'&&/all three sub-brands/.test(condition))split=['Vantage','Umbra','Forge'].map(x=>`${file(o)} shows the ${x} sub-brand.`);
  if(t.id==='VECTOR-01'&&/all three recovered marks/.test(condition))split=t.outputs.filter(x=>x.group_id==='recovered-mark').map(x=>`${file(o)} includes the mark from ${file(x)}.`);
  if(t.id==='VECTOR-04'&&/all six stickers/.test(condition))split=t.outputs.filter(x=>['recovered-sticker','new-sticker'].includes(x.group_id)).map(x=>`${file(o)} includes the sticker from ${file(x)}.`);
  if(t.id==='VECTOR-10'&&/all six garment applications/.test(condition))split=t.outputs.filter(x=>x.group_id==='garment-crest').map(x=>`${file(o)} shows the garment application for ${file(x)}.`);
  if(t.id==='LAYOUT-10'&&/all three parts/.test(condition))split=['arc of small-caps letters','oil lamp inside the ring','thin inner rule'].map(x=>`${file(o)} retains the ${x} shown in eastgate_crest_sign.jpg.`);
  if(t.id==='LAYOUT-12'&&/all three poster directions/.test(condition))split=['Type-led','Image-led','Graphic-led'].map(x=>`${file(o)} includes the ${x} poster direction.`);
  if(t.id==='LAYOUT-22')condition=condition.replace(' complete, all four digits present',' without a clipped digit');
  const c=clone(oldCheck);for(const f of oldRunFields)delete c[f];
  c.legacy_check_id=c.check_id;delete c.check_id;
  c.condition=condition;c.category=c.type==='auto'?'file/data specification':'retained task requirement';
  c.reference_assets=(c.reference_assets||[]).filter(a=>t.assets.some(x=>x.filename===a.filename));
  for(const part of split||[condition]){const key=[c.output_id,c.type,part].join('|');if(seen.has(key)){retired++;continue;}seen.add(key);t.checks.push({...c,condition:part});}
 }
 log(t,'verifiers',`Retired ${retired} duplicate, batch-completeness or superseded conditions; retained output-specific facts and technical checks.`);
}

function outputChecks(t,o){
 if(o.added_in==='V6')addTechnical(t,o);
 if(o.page_sources){
  for(const p of o.page_sources)human(t,o,`Page ${p.page} reproduces ${t.outputs.find(x=>x.output_id===p.output_id).path}, page ${p.source_page}, without changing its content.`,{category:'page equivalence',requirement_id:`${o.output_id}/page-${p.page}`,page:p.page,evidence:'Compare exported page content to the named individual file; an unchecked assembly manifest is insufficient.'});
  return;
 }
 const revisedContent=['PHOTO-04','MOTION-01','MOTION-02','MOTION-10','MOTION-14'].includes(t.id);
 if(o.source_record&&!rawOutput(t,o)&&revisedContent){
  for(const [field,value]of Object.entries(o.source_record.values)){
   if(value===null||value===''||/photo|image|picture|headshot|file|path|status|consent|internal|include|exclude|withdraw|department|tier|emergency|producer.*code|template/i.test(field))continue;
   if(t.id==='PHOTO-04'&&!['House','Season','Sleeps'].includes(field))continue;
   if(t.id==='MOTION-10'&&!['Episode','Title','Guest','Recording Date','Sponsor Line'].includes(field))continue;
   const isName=/name|title|house|shade|flavour|flavor|headline|dish/i.test(field);
   const extended=String(value).length>180;
   human(t,o,extended?`${field} matches the approved text below from ${o.source_record.table}, row ${o.source_record.row_number}.`:`${field} reads ${JSON.stringify(String(value))}${isName?' (letter case follows the named text role)':''}.`,{category:'record content',element:field,requirement_id:`${o.output_id}/field/${field}`,refs:[sourceRef(t,o.source_record.table)],expected_text:extended?String(value):null});
  }
 }
 for(const r of o.approved_copy_records||[])human(t,o,r.text.length>180?`${r.field} matches the exact approved copy below.`:`${r.field} reads ${JSON.stringify(r.text)}.`,{category:'approved copy',page:r.page,refs:[sourceRef(t,r.source)],requirement_id:o.output_id+'/copy/'+r.row_number,expected_text:r.text.length>180?r.text:null});
 for(const entry of o.page_content||[]){
  for(const [field,value]of Object.entries(entry.fields))human(t,o,`${entry.subject}: ${field} reads ${JSON.stringify(String(value))}.`,{category:'page content',page:entry.page});
  if(entry.source_file)human(t,o,`${entry.subject}'s photo is ${entry.source_file}.`,{category:'page source',page:entry.page,refs:[sourceRef(t,entry.source_file)]});
 }
 if(t.id==='PHOTO-04'){
  human(t,o,'Casa Fienile is not offered.',{category:'scope exclusion'});
  if(o.group_id==='booking-hero'){
   human(t,o,`The nightly rate reads "EUR ${o.source_record.values['Nightly Rate (EUR)']} per night".`,{category:'seasonal rate',refs:[sourceRef(t,'rates_2027.csv')]});
   human(t,o,'The booking action reads "Book direct".',{category:'approved copy'});
   human(t,o,'The minimum stay reads "7-night minimum".',{category:'approved copy'});
  }else{
   for(const r of t.revision.approved_records){const v=r.values;human(t,o,`${v.House}'s ${v.Season} rate is EUR ${v['Nightly Rate (EUR)']} per night.`,{category:'seasonal rate',refs:[sourceRef(t,'rates_2027.csv')],requirement_id:o.output_id+'/rate/'+r.row_number});human(t,o,`${v.House}'s ${v.Season} minimum stay is ${v['Minimum Stay']} nights.`,{category:'minimum stay',refs:[sourceRef(t,'rates_2027.csv')],requirement_id:o.output_id+'/minimum-stay/'+r.row_number});}
   for(const house of ['Casa Verranza','Casa Oliveto','Casa Scogliera']){const r=t.revision.approved_records.find(r=>r.values.House===house);human(t,o,`${house}'s capacity is ${r.values.Sleeps} guests.`,{category:'capacity'});}
   for(const [house,name,page]of [['Casa Verranza','verranza_pool.jpg',2],['Casa Oliveto','oliveto_pool.jpg',3],['Casa Scogliera','scogliera_pool.jpg',4]])human(t,o,`The ${house} image is taken from ${name}.`,{category:'source identity',page,refs:[sourceRef(t,name)]});
  }
 }
 if(t.id==='PHOTO-11'){
  if(o.output_id==='shade-card-r004')human(t,o,'The unchanged Amber Hour physical sample is not labelled as a concept.',{category:'sample identity'});
  else human(t,o,'The concept notice reads "CONCEPT COLOR - SAMPLE APPROVAL REQUIRED".',{category:'concept disclosure'});
 }
 if(o.asset_contract.source_files.length){
  const files=o.asset_contract.source_files;
  if(o.source_image)human(t,o,`The pictured subject comes from ${o.source_image}.`,{category:'source identity',element:o.asset_contract.subject,refs:files,requirement_id:o.output_id+'/source'});
  else human(t,o,`The selected source filename for its named subject is listed in this output's permitted-source table.`,{category:'source selection',element:o.asset_contract.subject,refs:files,requirement_id:o.output_id+'/source',evidence:'The table names individual files; identify the exact chosen filename per image slot/page/time range in source-handoff.json and visually match that source to this output.'});
 }
 if(o.colour_contract.applicable){
  const ref=[{filename:'V6 colour contract for '+file(o),url:`tasks/${t.id}/TASK_PACKAGE.zip#TASK_SPEC.json`}];
  for(const [rid,p]of [['palette','Authored flat graphic colours belong to the named V6 palette or an explicit physical-ink exception.'],['opacity','Authored text/fill/stroke opacity is 100%.'],['tints','An undeclared graphic tint is absent.'],['gradient','An authored graphic gradient is absent.'],['blend','Authored graphic layers use normal blending.']])human(t,o,p,{category:'colour',element:'Authored graphics; original source imagery is exempt',refs:ref,requirement_id:o.output_id+'/colour/'+rid,evidence:o.colour_contract.inspection});
  const colours=o.colour_contract.mandatory_roles;
  human(t,o,`Body text on an authored light ground uses ${colours.default_text.name} (${colours.default_text.hex}), unless a named element rule specifies another palette colour.`,{category:'colour role',requirement_id:o.output_id+'/colour/body',evidence:'Applies to body and fine-print text on an authored light ground; source-image text and dark-ground reversal are exempt.'});
 }
 if(t.id==='VECTOR-14'&&o.group_id==='member-bib')human(t,o,"The bib number uses the recovered hand-drawn Ironway numeral artwork, not a typed numeral.",{category:'artwork identity'});
 for(const r of o.typography_contract){
  for(const [field,label]of [['family','font'],['weight','weight'],['resolved_tracking','tracking']])human(t,o,`${r.role} ${label} is ${r[field]} when this role is used.`,{category:'typography',element:r.role,requirement_id:o.output_id+'/'+r.role_id+'/'+field,evidence:'Inspect the exported text layer or the matching editable source linked in source-handoff.json. A self-declared font name alone is not proof.'});
  human(t,o,`${r.role} size is ${r.resolved_size} when this role is used.`,{category:'typography size',element:r.role,requirement_id:o.output_id+'/'+r.role_id+'/size',evidence:'The output-specific resolved size governs; reference examples for other formats do not override it.'});
  human(t,o,`${r.role} line spacing is ${r.resolved_leading} when this role is used.`,{category:'typography leading',element:r.role,requirement_id:o.output_id+'/'+r.role_id+'/leading',evidence:'Inspect the matching editable text layer; a flattened font claim alone is not evidence.'});
 }
 for(const [i,p]of craft[t.id].entries())if(craftApplies(t,o,p))human(t,o,p,{category:'task craft constraint',requirement_id:`${t.id}/craft-${i+1}/${o.output_id}`,evidence:'Apply to the named element when that element is present or required. Source lettering and optional-role absence follow the contract exemptions.'});
 if(o.spec.format==='mp4'){
  const music=o.spec.audio==='music';
  human(t,o,'Speech is absent from the soundtrack.',{category:'audio',requirement_id:o.output_id+'/no-speech'});
  if(music){const beds=t.assets.filter(a=>/bed.*\.(wav|mp3)|\b.*_bed\./i.test(a.filename));human(t,o,`The music is ${beds.length===1?beds[0].filename:'the supplied cleared instrumental track named in this output\'s source handoff'}.`,{category:'audio source',refs:beds.map(a=>sourceRef(t,a.filename)),requirement_id:o.output_id+'/music-source'});}
  const isAnimation=['channel-animation'].includes(o.group_id);if(!isAnimation){human(t,o,'A frozen or looped source clip is not used to pad the runtime.',{category:'motion coverage',requirement_id:o.output_id+'/no-padding'});}
 }
}

function sourceHandoff(t){
 const designs=t.outputs.filter(o=>!rawOutput(t,o)&&!o.page_sources);
 if(!designs.length)return;
 const o=addOutput(t,{id:'source-handoff',group:'source-handoff',name:'Editable-source and selected-asset index',spec:{format:'json'},content:['One entry per designed output: exact export filename, editable source file or public read-only design URL, selected input filenames with page/slot/time range, and source-to-export version association.','Do not include passwords, tokens or expiring signed URLs.']});
 o.kind='source_index';o.typography_contract=[];o.colour_contract={applicable:false,reason:'Machine-readable source index.'};o.asset_contract={selection:'not applicable',source_files:[],supporting_files:[],subject:'Editable source references'};addTechnical(t,o);
 for(const d of designs){human(t,o,`The ${file(d)} entry opens its matching editable design source.`,{category:'editable source',element:d.output_id,requirement_id:'source-handoff/'+d.output_id,evidence:'Open the actual local source or public design URL and compare it to the exported file; an unsupported claim or broken/private link fails.'});}
 t.source_handoff_schema={format:'array',entry:{output_file:'Exact registered export filename',source:'Relative path to a delivered editable file, or public read-only Adobe Express/design document URL',version:'Export-matching document/page/version',assets:[{filename:'Exact permitted source filename',slot:'Named image slot, page or time range'}]},privacy:'No secrets, credentials or temporary signed URLs.',role_evidence:'Typography can be inspected in the source document. The index is a locator, not evidence that a font or layout actually passed.'};
}
function finalizeChecks(t){
 const seq=new Map(),seen=new Set();const final=[];
 for(const c of t.checks){
  const o=t.outputs.find(o=>o.output_id===c.output_id);assert(o,'Unknown output');
  let condition=c.condition||c.check||c.pass_condition;
  if(!condition.includes(file(o)))condition=`${file(o)}: ${condition}`;
  const key=[o.output_id,c.type,condition].join('|');if(seen.has(key))continue;seen.add(key);
  const prefix=c.type==='auto'?'A':'H',k=o.output_id+'/'+prefix;seq.set(k,(seq.get(k)||0)+1);
  const row={check_id:`${t.id}/${o.output_id}/${prefix}${String(seq.get(k)).padStart(3,'0')}`,output_id:o.output_id,type:c.type,check:condition,category:c.category||'task requirement',answer_type:'yes_no',allowed_answers:['Yes','No'],pass_answer:'Yes',status:'not_assessed',artifact_name:o.name,artifact_file:file(o),reference_assets:c.reference_assets||[]};
  for(const f of ['assertion','requirement_id','element','page','evidence','expected_text','legacy_check_id','k_id'])if(c[f]!==undefined&&c[f]!==null)row[f]=c[f];
  final.push(row);
 }
 t.checks=final;
}

function compactReferences(t){
 const names=new Set(t.assets.map(a=>a.filename));
 const clean=a=>names.has(a.filename)?{filename:a.filename}:a;
 for(const c of t.checks)c.reference_assets=c.reference_assets.map(clean);
 for(const o of t.outputs){
  o.asset_contract.source_files=o.asset_contract.source_files.map(clean);
  o.asset_contract.supporting_files=o.asset_contract.supporting_files.map(clean);
 }
}

const revised=[];
for(const source of original.tasks){
 assert(decisions[source.id]?.length&&craft[source.id]?.length,'Missing authored policy '+source.id);
 const t=clone(source),oldChecks=t.checks;t.checks=[];
 t.revision={edition:'V6',date:'2026-09-27',baseline_url:`https://dhigdec.github.io/creative-ai-benchmark/gatsby-v5/#${t.id}`,decisions:decisions[t.id],changes:[],content_sources:[],authority_order:['Explicit V6 amendments and output-specific approved values','V6 output register and assigned source records','V6 commission-specific brand role/colour contracts','Original client copy and artwork sources for unchanged facts and identity','Historic templates/reference designs for context only'],creative_freedom:'Layout, composition and source selection remain open only within the declared per-output contract. Do not invent missing facts, people, products or permissions.',legacy_scope:'The V6 output register is the complete delivery. Older requests not included there are not additional deliverables; retained missing items have now been registered.'};
 if(t.run)t.historical_run={edition:'V5',url:t.revision.baseline_url,completed_at:t.run.completed_at,note:'Historical run only. Not evaluated against the revised V6 contract.'};delete t.run;
 for(const o of t.outputs){for(const k of ['verification','artifact_url','bytes','sha256','verified_at','drive_folder_url','actual_pixels','actual_pages'])delete o[k];o.status='not_executed';o.record_field_policy='source_record.values are the V6 scoring values; raw_values are preserved provenance and may contain superseded export defects.';}
 resolveBrand(t);scopeAdditions(t);correctedFacts(t);migrateChecks(t,oldChecks);makePageSources(t);
 for(const o of t.outputs){bindAssets(t,o);o.colour_contract=colourContract(t,o);o.typography_contract=formatRoles(t,o);outputChecks(t,o);}
 sourceHandoff(t);
 const oldBoilerplate='Use the supplied approved copy and factual records. Permission restrictions in the owner\'s notes take precedence over inclusion in a source table.';
 t.brief=t.brief.replaceAll(oldBoilerplate,'Permission and consent exclusions remain binding. For other conflicts, use the explicit V6 amendments and the approved values in the output register.');
 t.brief+='\n\nProduction decisions for this edition\n'+decisions[t.id].map(x=>'- '+x).join('\n')+'\n\nThe V6 output register below is the complete handoff. Its per-output content, asset, colour and typography contracts are part of this brief. Historical templates do not add unregistered deliverables. Use the source handoff for editable designs and exact chosen-source references; do not include credentials.';
 for(const g of t.groups){g.outputs=t.outputs.filter(o=>o.group_id===g.id).map(o=>o.output_id);}
 t.groups=t.groups.filter(g=>g.outputs.length);
 t.readiness={contract_status:'revised_not_executed',asset_status:'Existing public inputs retained; media identity/quality is not newly certified by this contract revision.',connector_status:'Not re-executed against the V6 contracts.',expert_review_status:'Independent review pending',blockers:[]};
 log(t,'brief','Added the task-specific production decisions and a declared source-authority order.');
 log(t,'colour','Added per-output palette applicability, default roles, optional accents and explicit opacity/tint/blending rules.');
 log(t,'format','Where a print-only role needs a screen equivalent, the resolved output table uses 3 px per print point at a 1080 px short edge and a 24 px body/fine-print floor at that baseline. Explicit screen values take precedence.');
 log(t,'assets','Retained original S3 assets and added fixed-source or bounded-choice contracts naming individual files.');
 finalizeChecks(t);compactReferences(t);revised.push(t);
}

function write(p,value){fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,typeof value==='string'||Buffer.isBuffer(value)?value:JSON.stringify(value,null,2)+'\n');}
const manifest={edition:'V6',published_url:'https://dhigdec.github.io/creative-ai-benchmark/gatsby-v6/',preserved_url:'https://dhigdec.github.io/creative-ai-benchmark/gatsby-v5/',baseline_sha256:hash(baseline),tasks:revised.length,outputs:revised.reduce((n,t)=>n+t.outputs.length,0),checks:revised.reduce((n,t)=>n+t.checks.length,0),status:'contract revision; tasks not newly executed',old_source_assets_modified:false,v5_files_unchanged:true};
const catalog={edition:'V6',tasks:revised.map(t=>({id:t.id,title:t.title,code:t.code,family:t.family,output_count:t.outputs.length,check_count:t.checks.length})),manifest};
const stage=fs.mkdtempSync(path.join(os.tmpdir(),'gatsby-v6-package-'));
for(const t of revised){
 const p=path.join(dest,'tasks',t.id);
 write(path.join(p,'TASK_DATA.js'),'window.GATSBY_LOAD_COMPRESSED('+JSON.stringify(t.id)+','+JSON.stringify(gzipSync(JSON.stringify(t),{level:9}).toString('base64'))+');\n');
 const files={'TASK_SPEC.json':t,'BRIEF.md':`# ${t.title}\n\n${t.brief}\n`,'VERIFIERS.json':t.checks,'ASSET_MANIFEST.json':t.assets,'OUTPUT_REGISTER.json':t.outputs,'REVISION.json':t.revision,'DELIVERABLES.md':`# ${t.id}: delivery register\n\n`+t.outputs.map(o=>`## ${o.name}\n\n- File: \`${o.path}\`\n- Specification: ${JSON.stringify(o.spec)}\n- Content: ${Array.isArray(o.required_content)?o.required_content.join(' '):o.required_content}\n`).join('\n')};
 for(const [name,value]of Object.entries(files)){write(path.join(stage,t.id,name),value);if(fs.existsSync(path.join(p,name)))fs.unlinkSync(path.join(p,name));}
 const archive=path.join(p,'TASK_PACKAGE.zip');if(fs.existsSync(archive))fs.unlinkSync(archive);
 execFileSync('zip',['-q','-j',archive,...Object.keys(files).map(n=>path.join(stage,t.id,n))]);
}
fs.rmSync(stage,{recursive:true});
write(path.join(dest,'catalog.js'),'window.GATSBY_V6='+JSON.stringify(catalog)+';\n');
write(path.join(dest,'TASKS_V6_ALL100.json'),revised);
const zip=path.join(dest,'ALL100_TASKS.zip');
if(fs.existsSync(zip))fs.unlinkSync(zip);
execFileSync('zip',['-q','-j',zip,path.join(dest,'TASKS_V6_ALL100.json')]);
fs.unlinkSync(path.join(dest,'TASKS_V6_ALL100.json'));
write(path.join(dest,'CHANGES_ALL100.json'),changeLog);write(path.join(dest,'PUBLICATION_MANIFEST.json'),manifest);
write(path.join(dest,'CHANGES_ALL100.md'),'# Gatsby V6 changes\n\nV5 is preserved. These are task-contract amendments, not claims of new execution.\n\n'+revised.map(t=>`## ${t.id}: ${t.title}\n\n${t.revision.decisions.map(d=>'- '+d).join('\n')}\n\n${t.revision.changes.map(c=>'- '+c.category+': '+c.detail).join('\n')}`).join('\n\n'));
write(path.join(dest,'V5_PRESERVATION.json'),{index_sha256:hash(baseline),files:protectedBefore});
write(path.join(dest,'.nojekyll'),'');
const logo=baseline.match(/<header><img src="([^"]+)"/)[1];write(path.join(dest,'deccan-logo.png'),Buffer.from(logo.split(',')[1],'base64'));
assert.deepEqual(treeHashes(old),protectedBefore,'V5 changed');
console.log(JSON.stringify(manifest,null,2));
