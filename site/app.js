const base = document.body.dataset.base || './';
const $ = (q) => document.querySelector(q);
const $$ = (q) => [...document.querySelectorAll(q)];
const fmt = (x, digits = 2) => Number(x).toFixed(digits);
const esc = (s) => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
const svg = (w,h,content,label) => `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(label)}" xmlns="http://www.w3.org/2000/svg">${content}</svg>`;
const text = (x,y,s,cls='chart-label',anchor='start') => `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${esc(s)}</text>`;
const line = (x1,y1,x2,y2,cls='gridline') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"/>`;
const path = (points) => points.map((p,i)=>`${i?'L':'M'}${p[0].toFixed(2)},${p[1].toFixed(2)}`).join(' ');

function rates(data) {
  if (!$('#rate-charts')) return;
  let observed = false, animation = null;
  const range = $('#rate-scale'), button = $('#play-rates');
  function draw(announce = true) {
    const c = 2 ** Number(range.value);
    $('#scale-value').textContent = `${fmt(c)}× / ${fmt(1/c)}×`;
    $('#km-value').textContent = `${fmt(data.rates.km*c)} / min`;
    $('#kp-value').textContent = `${fmt(data.rates.kp/c)} / min`;
    range.setAttribute('aria-valuetext', `${fmt(c)} times the transcription rate and ${fmt(1/c)} times the translation rate`);
    const w = Math.max(280, $('#rate-charts').clientWidth - 32), stacked = w < 450;
    const pw = stacked ? w : (w-24)/2, ph = 176, h = stacked ? ph*2+24 : ph+8;
    let out = '';
    [0,1].forEach((col) => {
      const x0 = stacked ? 0 : col*(pw+24), y0 = stacked ? col*(ph+24) : 0;
      const x = t => x0+34+t/160*(pw-49), ymax = col ? 4.4 : 1.1;
      const y = a => y0+ph-33-a/ymax*(ph-70);
      out += text(x0+34,y0+16,col?'mRNA · intermediate':'Protein · output','plot-title');
      const ticks = col ? [0,2,4] : [0,.5,1];
      for (const t of ticks) out += line(x0+34,y(t),x0+pw-15,y(t)) + text(x0+27,y(t)+4,String(t),'chart-label','end');
      for (const t of [0,80,160]) out += text(x(t),y0+ph-17,String(t),'chart-label','middle');
      out += text(x0+pw/2,y0+ph,'Time (minutes)','chart-label','middle');
      const values = col?data.mrna:data.protein, max = Math.max(...values);
      if (!col || observed) {
        out += `<path class="plot-reference" d="${path(values.map((v,i)=>[x(data.t[i]),y(v/max)]))}"/>`;
        out += `<path class="plot-alternative" d="${path(values.map((v,i)=>[x(data.t[i]),y(v/max*(col?c:1))]))}"/>`;
      } else {
        out += `<rect x="${x0+33}" y="${y0+30}" width="${pw-47}" height="${ph-63}" fill="#edf0e9" fill-opacity=".96"/>`;
        out += text(x0+(pw+18)/2,y0+81,'Not measured','plot-title','middle');
        out += text(x0+(pw+18)/2,y0+100,'Add the second channel','chart-label','middle');
      }
    });
    $('#rate-charts').innerHTML = svg(w,h,out,'Protein stays the same as the two production rates trade off. The mRNA trace changes in proportion to transcription. Vertical axes are relative to each reference peak.');
    if (announce) $('#rate-verdict').textContent = observed ? (Math.abs(c-1)<.01 ? 'These are the reference rates. Move the slider to compare another setting.' : `The protein traces still coincide. The mRNA trace is ${fmt(c)}× the reference.`) : 'Protein alone cannot distinguish these rate settings.';
  }
  function stop(){if(animation)cancelAnimationFrame(animation);animation=null;button.textContent='▶ Animate';button.setAttribute('aria-pressed','false');draw();}
  function frame(time){range.value=String(1.65*Math.sin(time/2300));draw(false);animation=requestAnimationFrame(frame);}
  button.addEventListener('click',()=>{if(animation){stop();return;}button.textContent='Ⅱ Pause';button.setAttribute('aria-pressed','true');animation=requestAnimationFrame(frame);});
  range.addEventListener('input',()=>{stop();draw();});
  $$('[data-channel]').forEach(b=>b.addEventListener('click',()=>{observed=b.dataset.channel==='both';$$('[data-channel]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));draw();}));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  reduceMotion.addEventListener('change',()=>{if(reduceMotion.matches)stop();});
  new ResizeObserver(()=>draw(false)).observe($('#rate-charts'));
  draw();
}

function recovery(data) {
  if (!$('#recovery-chart')) return;
  const select=$('#signal-noise');
  select.innerHTML=data.snrs.map(v=>`<option value="${v}" ${v===2?'selected':''}>${v}${v===data.snrs[0]?' · stronger signal':v===data.snrs.at(-1)?' · weaker signal':''}</option>`).join('');
  function draw(){
    const snr=Number(select.value), w=Math.max(280,$('#recovery-chart').clientWidth-30), h=245;
    const x=r=>48+(r-data.rhos[0])/(data.rhos.at(-1)-data.rhos[0])*(w-68), y=v=>196-v/.8*151;
    let out=text(48,20,'Recovery score','plot-title');
    for(const t of [0,.2,.4,.6,.8])out+=line(48,y(t),w-20,y(t))+text(39,y(t)+4,t.toFixed(1),'chart-label','end');
    for(const r of data.rhos)out+=text(x(r),215,String(r),'chart-label','middle');
    out+=text((w+25)/2,240,'Shared-component mixing weight ρ','chart-label','middle');
    for(const [method,color] of [['raw','#9e7965'],['deflate1','#367869']]){
      const rows=data.rows.filter(r=>r.method===method&&r.snr===snr).sort((a,b)=>a.rho-b.rho);
      out+=`<path d="${path(rows.map(r=>[x(r.rho),y(r.normalized_recovery)]))}" stroke="${color}" stroke-width="2.3" fill="none"/>`;
      rows.forEach(r=>out+=`<circle cx="${x(r.rho)}" cy="${y(r.normalized_recovery)}" r="3.8" fill="${color}"><title>ρ ${r.rho}; signal/noise ${snr}; ${method==='raw'?'raw':'shared component removed'}: ${r.normalized_recovery.toFixed(3)}</title></circle>`);
    }
    $('#recovery-chart').innerHTML=svg(w,h,out,`Measured normalized network recovery at signal-to-noise ratio ${snr}, before and after removing the largest shared component.`);
    const target=data.rhos.includes(.7)?.7:data.rhos.at(-2), a=data.rows.find(r=>r.method==='raw'&&r.snr===snr&&r.rho===target), b=data.rows.find(r=>r.method==='deflate1'&&r.snr===snr&&r.rho===target);
    $('#network-verdict').textContent=`At shared weight ${target}: raw ${fmt(a.normalized_recovery)} → component removed ${fmt(b.normalized_recovery)}.`;
  }
  select.addEventListener('change',draw);new ResizeObserver(draw).observe($('#recovery-chart'));draw();
}

function colorTransfer() {
  if (!$('#color-request')) return;
  const colors={triangle:['blue','purple'],cross:['purple','peach']};
  $$('[data-color-shape]').forEach(button=>button.addEventListener('click',()=>{
    const shape=button.dataset.colorShape,[from,to]=colors[shape];
    $('#color-request').innerHTML=`<strong>Requested change:</strong> ${from} → ${to}`;
    const descriptions={input:`Original ${from} ${shape}`,target3:`Requested ${to} ${shape} with the same shape`,
      shift3:`Fixed-pattern result: ${shape} stays mostly ${from}`,prediction3:`Color-rule result: ${shape} becomes the requested ${to}`,
      'shift3-error':`Error map for the fixed pixel pattern, highlighting the missed ${shape} outline`,
      'prediction3-error':'Error map for the color rule: black throughout at this scale'};
    $$('[data-color-image]').forEach(img=>{img.src=base+`assets/color-${shape}-${img.dataset.colorImage}.png`;img.alt=descriptions[img.dataset.colorImage];});
    $$('[data-color-shape]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  }));
}
colorTransfer();

function brightness(data) {
  if (!$('#image-seed')) return;
  let index=0, interval=null;
  function draw(){
    const d=data[Number($('#image-seed').value)], sample=d.samples[index];
    for(const [id,key] of [['input','ratio_input'],['target','ratio_target'],['copy','ratio_unchanged'],['edit','ratio_prediction']])$('#image-'+id).src=base+'assets/'+sample.images[key];
    $$('[data-example]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.example)===index)));
    $('#image-verdict').textContent=`Run ${d.seed+1} · Example ${index+1}. Both copies use the same model. Compare them with the target to see what the brightness edit changes.`;
  }
  function stop(){clearInterval(interval);interval=null;$('#cycle-images').textContent='▶ Cycle examples';$('#cycle-images').setAttribute('aria-pressed','false');}
  $('#image-seed').addEventListener('change',draw);
  $$('[data-example]').forEach(b=>b.addEventListener('click',()=>{stop();index=Number(b.dataset.example);draw();}));
  $('#cycle-images').addEventListener('click',()=>{if(interval){stop();return;}interval=setInterval(()=>{index=(index+1)%3;draw();},2000);$('#cycle-images').textContent='Ⅱ Pause';$('#cycle-images').setAttribute('aria-pressed','true');});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  reduceMotion.addEventListener('change',()=>{if(reduceMotion.matches)stop();});draw();
}

function benchmarks(data){
  if(!$('#benchmark-chart'))return;
  function draw(){
    const key=$('#benchmark-dataset').value,d=data[key],w=Math.max(290,$('#benchmark-chart').clientWidth-30),h=266;
    const left=w<450?125:166, right=48, scale=v=>v/.8*(w-left-right);
    const rows=[...d.methods].sort((a,b)=>b.mean-a.mean);
    let out='';
    for(const t of [0,.2,.4,.6,.8])out+=line(left+scale(t),20,left+scale(t),225)+text(left+scale(t),244,String(t),'benchmark-axis','middle');
    rows.forEach((r,i)=>{const y=35+i*43,label=w<450&&r.id==='lagged_genie3_rf'?'Lagged forest':r.label;out+=text(left-10,y+4,label,'benchmark-label','end');out+=`<rect x="${left}" y="${y-10}" width="${scale(r.mean)}" height="20" rx="1" fill="${r.id==='dmd_operator'?'#b95238':'#367869'}"/>`;out+=text(left+scale(r.mean)+8,y+4,fmt(r.mean,3),'benchmark-label');});
    out+=text((w+left-right)/2,264,'Mean average precision','benchmark-axis','middle');
    $('#benchmark-chart').innerHTML=svg(w,h,out,`${key==='dream4'?'DREAM4':'BoolODE'} results. `+rows.map(r=>`${r.label}: ${fmt(r.mean,3)}`).join('. '));
    $('#benchmark-caption').textContent=key==='dream4'?'Five 10-gene networks, time-ordered samples. Lagged random forest has the highest aggregate score.':'Eighteen simulated single-cell datasets, ordered by pseudotime. Lagged LASSO has the highest aggregate score.';
  }
  $('#benchmark-dataset').addEventListener('change',draw);new ResizeObserver(draw).observe($('#benchmark-chart'));draw();
}

function inputDesign(data){
  if(!$('#pulse-chart'))return;
  let protocol='three_pulses';
  const names={M2:'mRNA production',M3:'protein production'};
  function draw(){
    const truth=$('#true-mechanism').value;
    const d=data.traces.find(r=>r.truth===truth&&r.protocol===protocol);
    const w=Math.max(280,$('#pulse-chart').clientWidth-30), h=284;
    const x=t=>44+t/300*(w-62), peak=Math.max(...data.traces.filter(r=>r.truth===truth).flatMap(r=>[...r.protein,...r.rivalProtein]));
    const y=p=>177-p/peak*133;
    let out=text(44,19,'Protein · fraction of reference peak','plot-title');
    for(const tick of [0,.5,1,1.5]){
      const py=y(tick*d.reference_peak);
      if(py>=32)out+=line(44,py,w-18,py)+text(36,py+4,fmt(tick,1),'chart-label','end');
    }
    out+=`<path class="plot-reference" d="${path(d.t.map((t,i)=>[x(t),y(d.protein[i])]))}"/>`;
    out+=`<path class="plot-alternative" d="${path(d.t.map((t,i)=>[x(t),y(d.rivalProtein[i])]))}"/>`;
    out+=text(44,206,'Transcription input','plot-title');
    const steps=[];d.levels.forEach((u,i)=>{steps.push([x(d.edges[i]),240-u*12],[x(d.edges[i+1]),240-u*12]);});
    out+=`<path d="${path(steps)}" fill="none" stroke="#367869" stroke-width="2"/>`;
    for(const t of [0,100,200,300])out+=text(x(t),260,String(t),'chart-label','middle');
    out+=text((w+26)/2,281,'Time (minutes)','chart-label','middle');
    $('#pulse-chart').innerHTML=svg(w,h,out,`${protocol==='constant'?'Constant input':'Three pulses'}, with feedback on ${names[truth]}. The rival mechanism refits four parameters.`);
    const counts=data.summary.filter(r=>r.truth===truth&&r.kappa===.02);
    for(const [id,p] of [['constant-count','constant'],['pulse-count','three_pulses']]){
      const r=counts.find(x=>x.protocol===p);$('#'+id).innerHTML=`${r.correct} <small>/ ${r.n}</small>`;
    }
    $('#pulse-verdict').textContent=`Correct model selections when feedback slows ${names[truth]}. Shown above: ${protocol==='constant'?'constant input':'three pulses'}.`;
  }
  $$('[data-protocol]').forEach(b=>b.addEventListener('click',()=>{protocol=b.dataset.protocol;$$('[data-protocol]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));draw();}));
  $('#true-mechanism').addEventListener('change',draw);new ResizeObserver(draw).observe($('#pulse-chart'));draw();
}

fetch(base+'assets/study-data.json').then(r=>{if(!r.ok)throw Error('Study data unavailable');return r.json();}).then(d=>{rates(d.model);recovery(d.network);brightness(d.brightness);benchmarks(d.benchmarks);inputDesign(d.inputDesign);}).catch(()=>{
  $$('button, input, select').forEach(x=>x.disabled=true);
  const p=document.createElement('p');p.className='copy-note';p.textContent='Interactive data could not load. The saved figures and study notes remain available.';$('main').prepend(p);
});
