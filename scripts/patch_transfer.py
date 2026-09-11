from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''    <div class="card">
      <h3>バックアップ</h3>
      <div class="privacy">観察データはこのブラウザ端末内に保存され、GitHubリポジトリには保存されません。ブラウザデータ削除や端末変更に備えて定期的なバックアップがおすすめです。</div>
      <div class="btnrow">
        <button id="backupBtn" class="btn good">JSONバックアップ</button>
        <label class="btn secondary" for="restoreFile">バックアップ復元</label>
        <input id="restoreFile" type="file" accept=".json">
        <button id="csvBtn" class="btn secondary">CSV出力</button>
      </div>
    </div>'''
new='''    <div class="card">
      <h3>他の端末へ引き継ぐ</h3>
      <div class="privacy">スタッフ・グレード・観察記録をパスワードで暗号化した「引き継ぎコード」にできます。公開GitHubには保存されません。コードとパスワードは別々に管理してください。</div>
      <div class="field"><label for="transferPassword">引き継ぎ用パスワード</label><input id="transferPassword" type="password" autocomplete="new-password" placeholder="8文字以上を推奨"></div>
      <div class="btnrow">
        <button id="makeTransferBtn" class="btn good">引き継ぎコードを作る</button>
        <button id="copyTransferBtn" class="btn secondary">コードをコピー</button>
      </div>
      <div class="field"><label for="transferCode">引き継ぎコード</label><textarea id="transferCode" placeholder="作成したコード、または別端末から持ってきたコードをここに貼り付け"></textarea></div>
      <button id="restoreTransferBtn" class="btn primary block">この端末に復元</button>
      <div id="transferStatus" class="notice">新端末では、同じパスワードと引き継ぎコードを入力して復元します。</div>
    </div>

    <div class="card">
      <h3>バックアップ</h3>
      <div class="privacy">従来のJSONバックアップも利用できます。ブラウザデータ削除や端末変更に備えて定期的なバックアップがおすすめです。</div>
      <div class="btnrow">
        <button id="backupBtn" class="btn good">JSONバックアップ</button>
        <label class="btn secondary" for="restoreFile">バックアップ復元</label>
        <input id="restoreFile" type="file" accept=".json">
        <button id="csvBtn" class="btn secondary">CSV出力</button>
      </div>
    </div>'''
if old not in s: raise SystemExit('backup block not found')
s=s.replace(old,new,1)
needle="""  function backup(){const data={version:1,exportedAt:new Date().toISOString(),staff,records,importSettings};download(`staff-kansatsu-backup-${nowISO()}.json`,JSON.stringify(data,null,2))}
  async function restore(file){try{const data=JSON.parse(await file.text());if(!Array.isArray(data.staff)||!Array.isArray(data.records))throw new Error('対応するバックアップ形式ではありません');if(!confirm(`スタッフ ${data.staff.length}名、記録 ${data.records.length}件で現在のデータを置き換えますか？`))return;staff=data.staff;records=data.records;importSettings=data.importSettings||{start:'',end:'',exclude:''};persist();saveJSON(KEYS.import,importSettings);normalizeStaff();loadImportFields();renderAll();alert('バックアップを復元しました。')}catch(e){alert('復元できませんでした：'+(e?.message||e))}}
"""
insert="""  function backup(){const data={version:1,exportedAt:new Date().toISOString(),staff,records,importSettings};download(`staff-kansatsu-backup-${nowISO()}.json`,JSON.stringify(data,null,2))}
  async function restore(file){try{const data=JSON.parse(await file.text());if(!Array.isArray(data.staff)||!Array.isArray(data.records))throw new Error('対応するバックアップ形式ではありません');if(!confirm(`スタッフ ${data.staff.length}名、記録 ${data.records.length}件で現在のデータを置き換えますか？`))return;staff=data.staff;records=data.records;importSettings=data.importSettings||{start:'',end:'',exclude:''};persist();saveJSON(KEYS.import,importSettings);normalizeStaff();loadImportFields();renderAll();alert('バックアップを復元しました。')}catch(e){alert('復元できませんでした：'+(e?.message||e))}}
  const bytesToB64=bytes=>{let out='';for(let i=0;i<bytes.length;i+=0x8000)out+=String.fromCharCode(...bytes.subarray(i,i+0x8000));return btoa(out)};
  const b64ToBytes=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
  async function transferKey(password,salt,usage){const raw=await crypto.subtle.importKey('raw',new TextEncoder().encode(password),'PBKDF2',false,['deriveKey']);return crypto.subtle.deriveKey({name:'PBKDF2',salt,iterations:180000,hash:'SHA-256'},raw,{name:'AES-GCM',length:256},false,usage)}
  async function makeTransferCode(){const pass=$('transferPassword').value;if(pass.length<6){alert('引き継ぎ用パスワードを6文字以上で入力してください。');return}try{$('transferStatus').className='notice';$('transferStatus').textContent='引き継ぎコードを作成しています…';const salt=crypto.getRandomValues(new Uint8Array(16)),iv=crypto.getRandomValues(new Uint8Array(12)),key=await transferKey(pass,salt,['encrypt']),data={version:2,exportedAt:new Date().toISOString(),staff,records,importSettings},plain=new TextEncoder().encode(JSON.stringify(data)),encrypted=new Uint8Array(await crypto.subtle.encrypt({name:'AES-GCM',iv},key,plain)),payload={v:2,s:bytesToB64(salt),i:bytesToB64(iv),d:bytesToB64(encrypted)};$('transferCode').value='SK2.'+bytesToB64(new TextEncoder().encode(JSON.stringify(payload)));$('transferStatus').className='notice good';$('transferStatus').textContent=`引き継ぎコードを作成しました。スタッフ ${staff.length}名・記録 ${records.length}件を含みます。`;await copyText($('transferCode').value,'引き継ぎコードをコピーしました。')}catch(e){$('transferStatus').className='notice warn';$('transferStatus').textContent='作成できませんでした：'+(e?.message||e)}}
  async function restoreTransferCode(){const pass=$('transferPassword').value,code=$('transferCode').value.trim();if(!pass||!code){alert('パスワードと引き継ぎコードを入力してください。');return}try{$('transferStatus').className='notice';$('transferStatus').textContent='コードを確認しています…';if(!code.startsWith('SK2.'))throw new Error('対応する引き継ぎコードではありません');const payload=JSON.parse(new TextDecoder().decode(b64ToBytes(code.slice(4)))),salt=b64ToBytes(payload.s),iv=b64ToBytes(payload.i),cipher=b64ToBytes(payload.d),key=await transferKey(pass,salt,['decrypt']),plain=await crypto.subtle.decrypt({name:'AES-GCM',iv},key,cipher),data=JSON.parse(new TextDecoder().decode(plain));if(!Array.isArray(data.staff)||!Array.isArray(data.records))throw new Error('データ形式が正しくありません');if(!confirm(`スタッフ ${data.staff.length}名、記録 ${data.records.length}件でこの端末のデータを置き換えますか？`)){$('transferStatus').textContent='復元をキャンセルしました。';return}staff=data.staff;records=data.records;importSettings=data.importSettings||{start:'',end:'',exclude:''};persist();saveJSON(KEYS.import,importSettings);normalizeStaff();loadImportFields();renderAll();$('transferStatus').className='notice good';$('transferStatus').textContent='この端末への引き継ぎが完了しました。';alert('引き継ぎが完了しました。')}catch(e){$('transferStatus').className='notice warn';$('transferStatus').textContent='復元できませんでした。パスワードまたはコードを確認してください。'}}
"""
if needle not in s: raise SystemExit('backup functions not found')
s=s.replace(needle,insert,1)
oldbind="""$('applyImportSettingsBtn').onclick=saveImportSettings;$('backupBtn').onclick=backup;$('restoreFile').onchange=e=>{const f=e.target.files?.[0];if(f)restore(f);e.target.value=''};$('csvBtn').onclick=exportCSV;"""
newbind="""$('applyImportSettingsBtn').onclick=saveImportSettings;$('makeTransferBtn').onclick=makeTransferCode;$('copyTransferBtn').onclick=()=>copyText($('transferCode').value,'引き継ぎコードをコピーしました。');$('restoreTransferBtn').onclick=restoreTransferCode;$('backupBtn').onclick=backup;$('restoreFile').onchange=e=>{const f=e.target.files?.[0];if(f)restore(f);e.target.value=''};$('csvBtn').onclick=exportCSV;"""
if oldbind not in s: raise SystemExit('event bind block not found')
s=s.replace(oldbind,newbind,1)
for x in ['makeTransferCode','restoreTransferCode','transferPassword','transferCode','SK2.']:
    if x not in s: raise SystemExit('missing '+x)
p.write_text(s)
