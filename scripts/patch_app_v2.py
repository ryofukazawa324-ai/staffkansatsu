from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Navigation and styling
s=s.replace('grid-template-columns:repeat(4,1fr);gap:7px;margin:14px 0;padding:7px','grid-template-columns:repeat(5,1fr);gap:7px;margin:14px 0;padding:7px',1)
s=s.replace('.grade-tabs{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:6px}', '.grade-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:6px}',1)
s=s.replace('.grade-tab{border:1px solid #d9dee8;background:#f7f9fc;color:#536079;border-radius:11px;padding:10px 6px;font-weight:800;font-size:12px}', '.grade-tab{border:1px solid #d9dee8;background:#f7f9fc;color:#536079;border-radius:11px;padding:9px 6px;font-weight:800;font-size:12px;line-height:1.25}.grade-tab span{display:block;font-size:14px}.grade-tab small{display:block;font-size:10px;margin-top:3px;font-weight:700}',1)
s=s.replace('.tabs{margin-left:-4px;margin-right:-4px}', '.tabs{margin-left:-4px;margin-right:-4px}.grade-tabs{grid-template-columns:repeat(2,1fr)}',1)
s=s.replace('日々の良い行動と改善期待行動を、半年単位で蓄積・振り返り。','6つの人事考課観点で行動を記録し、グレードに合わせて半年単位で振り返り。',1)
if 'href="policy.html"' not in s:
    s=s.replace('    <button class="tab" data-tab="summaryPanel">半年まとめ</button>\n    <button class="tab" data-tab="dataPanel">データ</button>', '    <button class="tab" data-tab="summaryPanel">半年まとめ</button>\n    <a class="tab" href="policy.html" style="text-decoration:none;text-align:center">育成方針</a>\n    <button class="tab" data-tab="dataPanel">データ</button>',1)

# Observation form: six appraisal criteria + factual supplements
old_form='''      <div class="field"><label for="obsGood">良い点</label><textarea id="obsGood" placeholder="例：レジ混雑に気づいて自発的に応援へ入った"></textarea></div>
      <div class="field"><label for="obsImprove">改善期待行動</label><textarea id="obsImprove" placeholder="例：自分で完結せず、周囲にも優先順位を共有して動けるとさらに良い"></textarea></div>
      <div class="field"><label for="obsFact">具体的な出来事・状況</label><textarea id="obsFact" placeholder="いつ・どんな状況で・どんな行動だったか"></textarea></div>
      <div class="field"><label for="obsNext">次回確認したいこと</label><textarea id="obsNext" placeholder="次に同じ状況があった時に確認するポイント"></textarea></div>'''
new_form='''      <div class="muted" style="margin-top:12px">現在グレードで求められる水準を基準に、当てはまる項目だけ記録します。</div>
      <div class="grid2">
        <div class="field"><label for="obsNo1">No.1であること</label><textarea id="obsNo1" placeholder="成果・高い基準・自分の領域で一番を目指す行動"></textarea></div>
        <div class="field"><label for="obsOpen">オープンであること</label><textarea id="obsOpen" placeholder="報告・相談・共有・周囲との連携"></textarea></div>
        <div class="field"><label for="obsJoy">喜びがあること</label><textarea id="obsJoy" placeholder="お客様や仲間の喜びにつながった行動"></textarea></div>
        <div class="field"><label for="obsInnovative">革新的であること</label><textarea id="obsInnovative" placeholder="改善・工夫・新しいやり方への挑戦"></textarea></div>
        <div class="field"><label for="obsDevelop">育成・どうにかできること</label><textarea id="obsDevelop" placeholder="人や課題に向き合い、成長・改善へ動かした行動"></textarea></div>
        <div class="field"><label for="obsAchieve">達成・成し遂げられること</label><textarea id="obsAchieve" placeholder="任されたことを最後までやり切り結果につなげた行動"></textarea></div>
      </div>
      <div class="field"><label for="obsFact">具体的な出来事・状況（任意）</label><textarea id="obsFact" placeholder="いつ・どんな状況で・何が起きたか"></textarea></div>
      <div class="field"><label for="obsNext">次回確認したいこと（任意）</label><textarea id="obsNext" placeholder="次に同じ状況があった時に確認するポイント"></textarea></div>'''
if old_form not in s:
    raise SystemExit('observation form block not found')
s=s.replace(old_form,new_form,1)

# Grade system
s=re.sub(r"const GRADE_OPTIONS=.*?(?=\n\n  function cryptoId)", """const GRADE_OPTIONS=[{v:'1',l:'ただしく覚える'},{v:'2',l:'ひとりでできる'},{v:'3',l:'先頭に立って引っ張る'},{v:'4',l:'よく守り、よく攻める'},{v:'5',l:'仕組みをつくり組織を束ねる'},{v:'6',l:'新しい価値を作る'}];
  const gradeLabel=v=>{const g=GRADE_OPTIONS.find(x=>x.v===String(v));return g?`G${g.v} ${g.l}`:(v?String(v):'未設定')};
  function renderGradeTabs(containerId,inputId,value){const host=$(containerId),input=$(inputId);if(!host||!input)return;const normalized=GRADE_OPTIONS.some(g=>g.v===String(value))?String(value):'';input.value=normalized;host.innerHTML=GRADE_OPTIONS.map(g=>`<button type=\"button\" class=\"grade-tab ${input.value===g.v?'active':''}\" data-grade-choice=\"${g.v}\"><span>G${g.v}</span><small>${esc(g.l)}</small></button>`).join('');host.querySelectorAll('[data-grade-choice]').forEach(b=>b.onclick=()=>{input.value=b.dataset.gradeChoice;host.querySelectorAll('.grade-tab').forEach(x=>x.classList.toggle('active',x===b))})}""", s, count=1, flags=re.S)

old_norm="function normalizeStaff(){const seen=new Set();staff=staff.filter(s=>{s.id=String(s.id||cryptoId());s.name=String(s.name||'').trim();s.grade=String(s.grade||'').trim();s.active=s.active!==false;if(!s.name||seen.has(s.name))return false;seen.add(s.name);return true});saveJSON(KEYS.staff,staff)}"
new_norm="function normalizeStaff(){const seen=new Set(),legacy={新人:'2',社員:'2',中堅:'3',熟練:'3'};staff=staff.filter(s=>{s.id=String(s.id||cryptoId());s.name=String(s.name||'').trim();s.grade=String(s.grade||'').trim();if(legacy[s.grade])s.grade=legacy[s.grade];if(!GRADE_OPTIONS.some(g=>g.v===s.grade))s.grade='2';s.active=s.active!==false;if(!s.name||seen.has(s.name))return false;seen.add(s.name);return true});saveJSON(KEYS.staff,staff)}"
if old_norm not in s: raise SystemExit('normalizeStaff not found')
s=s.replace(old_norm,new_norm,1)
s=s.replace("staff.push({id:cryptoId(),name,grade:'',active:true,source:'shift'})","staff.push({id:cryptoId(),name,grade:'2',active:true,source:'shift'})",1)
s=s.replace("${esc(s.name)}${s.grade?`（${esc(s.grade)}）`:''}","${esc(s.name)}${s.grade?`（${esc(gradeLabel(s.grade))}）`:''}",1)
s=s.replace("${s.grade?`グレード ${esc(s.grade)} ・ `:''}","${s.grade?`${esc(gradeLabel(s.grade))} ・ `:''}",1)

# Record handling
s=re.sub(r"  function saveRecord\(\).*?\n  function clearRecordForm\(clearStaff=true\).*?\n  function deleteRecord", """  function saveRecord(){const staffId=$('obsStaff').value,date=$('obsDate').value;if(!staffId){alert('スタッフを選択してください。');return}if(!date){alert('日付を入力してください。');return}const no1=$('obsNo1').value.trim(),open=$('obsOpen').value.trim(),joy=$('obsJoy').value.trim(),innovative=$('obsInnovative').value.trim(),develop=$('obsDevelop').value.trim(),achieve=$('obsAchieve').value.trim(),fact=$('obsFact').value.trim(),next=$('obsNext').value.trim();if(!no1&&!open&&!joy&&!innovative&&!develop&&!achieve){alert('6つの観察項目のうち1つ以上入力してください。');return}const st=findStaff(staffId),grade=$('obsGrade').value.trim()||'2';if(st&&st.grade!==grade)st.grade=grade;records.push({id:cryptoId(),date,staffId,staffName:st?.name||'',grade,no1,open,joy,innovative,develop,achieve,fact,next,createdAt:new Date().toISOString()});persist();clearRecordForm(false);renderAll();alert('観察記録を保存しました。')}
  function clearRecordForm(clearStaff=true){['obsNo1','obsOpen','obsJoy','obsInnovative','obsDevelop','obsAchieve','obsFact','obsNext'].forEach(id=>$(id).value='');if(clearStaff)$('obsStaff').selectedIndex=0;syncGradeFromStaff()}
  function deleteRecord""", s, count=1, flags=re.S)

# Recent records
s=re.sub(r"  function renderRecent\(\).*?\n\n  function renderPeriods", """  function renderRecent(){const arr=[...records].sort((a,b)=>(b.date+b.createdAt).localeCompare(a.date+a.createdAt)).slice(0,20);if(!arr.length){$('recentRecords').innerHTML='<div class=\"empty\">まだ観察記録がありません。</div>';return}$('recentRecords').innerHTML=arr.map(r=>{const st=findStaff(r.staffId),name=st?.name||r.staffName||'不明',sections=[['No.1であること',r.no1],['オープンであること',r.open],['喜びがあること',r.joy],['革新的であること',r.innovative],['育成・どうにかできること',r.develop],['達成・成し遂げられること',r.achieve],['具体的な出来事・状況',r.fact],['次回確認',r.next],['旧記録：良い点',r.good],['旧記録：改善期待行動',r.improve]].filter(x=>x[1]);return`<article class=\"record\"><div class=\"record-top\"><div><span class=\"badge\">${esc(periodFor(r.date).key.endsWith('H1')?'上期':'下期')}</span><h4>${esc(name)} ${r.grade?`<span class=\"badge good\">${esc(gradeLabel(r.grade))}</span>`:''}</h4><div class=\"record-date\">${esc(r.date)}</div></div><button class=\"iconbtn\" data-delete-record=\"${esc(r.id)}\">削除</button></div>${sections.map(x=>`<div class=\"record-section\"><b>${x[0]}</b><div>${esc(x[1])}</div></div>`).join('')}</article>`}).join('');$('recentRecords').querySelectorAll('[data-delete-record]').forEach(b=>b.onclick=()=>deleteRecord(b.dataset.deleteRecord))}

  function renderPeriods""", s, count=1, flags=re.S)

# Summary rendering
s=re.sub(r"  function renderSummary\(\).*?\n\n  function summaryText", """  function renderSummary(){const key=$('periodSelect').value,rs=getPeriodRecords(key),ids=[...new Set(rs.map(r=>r.staffId))];if(!ids.length){$('summaryList').innerHTML='<div class=\"empty\">この期間の観察記録はありません。</div>';return}$('summaryList').innerHTML=ids.map(id=>{const prs=rs.filter(r=>r.staffId===id).sort((a,b)=>a.date.localeCompare(b.date)),st=findStaff(id),name=st?.name||prs[0]?.staffName||'不明',latestGrade=[...prs].reverse().find(r=>r.grade)?.grade||st?.grade||'2';const legacy=compactLines(prs.flatMap(r=>[r.good,r.improve]));return`<section class=\"summary-person\"><div class=\"summary-head\"><div><strong>${esc(name)}</strong><div class=\"muted\">記録 ${prs.length}件</div></div><span class=\"badge\">${esc(gradeLabel(latestGrade))}</span></div><div class=\"summary-box\"><div class=\"summary-item\"><strong>No.1であること</strong><div>${esc(compactLines(prs.map(r=>r.no1)))}</div></div><div class=\"summary-item\"><strong>オープンであること</strong><div>${esc(compactLines(prs.map(r=>r.open)))}</div></div><div class=\"summary-item\"><strong>喜びがあること</strong><div>${esc(compactLines(prs.map(r=>r.joy)))}</div></div><div class=\"summary-item\"><strong>革新的であること</strong><div>${esc(compactLines(prs.map(r=>r.innovative)))}</div></div><div class=\"summary-item\"><strong>育成・どうにかできること</strong><div>${esc(compactLines(prs.map(r=>r.develop)))}</div></div><div class=\"summary-item\"><strong>達成・成し遂げられること</strong><div>${esc(compactLines(prs.map(r=>r.achieve)))}</div></div><div class=\"summary-item\"><strong>具体的な出来事</strong><div>${esc(compactLines(prs.map(r=>r.fact)))}</div></div><div class=\"summary-item\"><strong>次回確認</strong><div>${esc(compactLines(prs.map(r=>r.next)))}</div></div>${legacy!=='—'?`<div class=\"summary-item\"><strong>旧形式の記録</strong><div>${esc(legacy)}</div></div>`:''}</div></section>`}).join('')}

  function summaryText""", s, count=1, flags=re.S)

# Copy/AI summary
s=re.sub(r"  function summaryText\(ai=false\).*?\n  async function copyText", """  function summaryText(ai=false){const key=$('periodSelect').value,p=periodOptions().find(x=>x.key===key),rs=getPeriodRecords(key),ids=[...new Set(rs.map(r=>r.staffId))],blocks=ids.map(id=>{const prs=rs.filter(r=>r.staffId===id).sort((a,b)=>a.date.localeCompare(b.date)),st=findStaff(id),name=st?.name||prs[0]?.staffName||'不明',current=[...prs].reverse().find(r=>r.grade)?.grade||st?.grade||'2',lines=[`【${name} / ${gradeLabel(current)}】`];prs.forEach(r=>{lines.push(`\\n${r.date}${r.grade?` / ${gradeLabel(r.grade)}`:''}`);if(r.no1)lines.push(`No.1であること：${r.no1}`);if(r.open)lines.push(`オープンであること：${r.open}`);if(r.joy)lines.push(`喜びがあること：${r.joy}`);if(r.innovative)lines.push(`革新的であること：${r.innovative}`);if(r.develop)lines.push(`育成・どうにかできること：${r.develop}`);if(r.achieve)lines.push(`達成・成し遂げられること：${r.achieve}`);if(r.fact)lines.push(`出来事・状況：${r.fact}`);if(r.next)lines.push(`次回確認：${r.next}`);if(r.good)lines.push(`旧記録・良い点：${r.good}`);if(r.improve)lines.push(`旧記録・改善期待行動：${r.improve}`)});return lines.join('\\n')});const base=`${p?.label||key} スタッフ観察記録\\n記録件数：${rs.length}件\\n\\n${blocks.join('\\n\\n--------------------\\n\\n')}`;if(!ai)return base;return`以下は${p?.label||key}のスタッフ観察記録です。人物への決めつけではなく、記載された具体的行動だけを根拠に振り返ってください。現在グレードに対して期待される水準を基準に相対的に見てください。\\n\\n人事考課の観点は、No.1であること／オープンであること／喜びがあること／革新的であること／育成・どうにかできること／達成・成し遂げられること、の6項目です。\\n\\n各スタッフについて、\\n・6項目それぞれの記録から確認できる強み\\n・現在グレードに対して不足している行動\\n・前半から後半への変化や成長\\n・次の一段を目指すための具体的行動を3つ\\n・リーダーとしての支援・声かけ\\nを整理してください。記録だけから昇格・降格を断定せず、根拠が少ない項目は「記録不足」としてください。\\n\\n${base}`}
  async function copyText""", s, count=1, flags=re.S)

# Manual staff default and CSV
s=s.replace("function addStaff(){const name=$('manualName').value.trim(),grade=$('manualGrade').value.trim();","function addStaff(){const name=$('manualName').value.trim(),grade=$('manualGrade').value.trim()||'2';",1)
s=s.replace("renderGradeTabs('manualGradeTabs','manualGrade','');renderAll()","renderGradeTabs('manualGradeTabs','manualGrade','2');renderAll()",1)
s=re.sub(r"  function exportCSV\(\).*?\n  function deleteAll", """  function exportCSV(){const header=['日付','期間','スタッフ','グレード','No.1であること','オープンであること','喜びがあること','革新的であること','育成・どうにかできること','達成・成し遂げられること','具体的な出来事・状況','次回確認','旧形式：良い点','旧形式：改善期待行動'],lines=[header.map(csvCell).join(',')];[...records].sort((a,b)=>a.date.localeCompare(b.date)).forEach(r=>{const st=findStaff(r.staffId),p=periodFor(r.date);lines.push([r.date,p.label,st?.name||r.staffName||'',gradeLabel(r.grade),r.no1,r.open,r.joy,r.innovative,r.develop,r.achieve,r.fact,r.next,r.good,r.improve].map(csvCell).join(','))});download(`staff-kansatsu-${nowISO()}.csv`,'\\uFEFF'+lines.join('\\r\\n'),'text/csv')}
  function deleteAll""", s, count=1, flags=re.S)
s=s.replace("$('obsDate').value=nowISO();renderGradeTabs('manualGradeTabs','manualGrade','');", "$('obsDate').value=nowISO();renderGradeTabs('manualGradeTabs','manualGrade','2');",1)

# Verification
needed=['obsNo1','obsOpen','obsJoy','obsInnovative','obsDevelop','obsAchieve','新しい価値を作る','No.1であること','gradeLabel','policy.html']
missing=[x for x in needed if x not in s]
if missing:
    raise SystemExit('patch incomplete: '+','.join(missing))

p.write_text(s)
