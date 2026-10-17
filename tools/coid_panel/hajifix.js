const { chromium } = require(process.env.PWPATH);
const cfg = JSON.parse(process.env.CFG);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2600} });
  await ctx.route(/r2\.cloudflarestorage\.com/, async route => { try { const r = await route.fetch(); await route.fulfill({ response: r, headers:{...r.headers(),'access-control-allow-origin':'*'} }); } catch(e){ await route.abort(); } });
  const p = await ctx.newPage();
  await p.goto(`https://elharamainwisata.co.id/secret-admin/haji-packages/${cfg.id}/edit`, {waitUntil:'domcontentloaded',timeout:60000}); await p.waitForTimeout(7000);
  if (cfg.name) { await p.fill('input[id="form.name"]', cfg.name); }
  if (cfg.description) { await p.fill('textarea[id="form.description"]', cfg.description); }
  if (cfg.thumb) {
    const rm = p.locator('.filepond--action-remove-item');
    for (let i=0;i<3 && await rm.count();i++){ await rm.first().click({force:true}).catch(()=>{}); await p.waitForTimeout(3000); }
    await p.locator('input.filepond--browser').first().setInputFiles(cfg.thumb);
    let ok=false; for (let i=0;i<25;i++){ await p.waitForTimeout(2000); const t=(await p.locator('.filepond--file-status').allInnerTexts()).join('|'); if(/Upload complete/i.test(t)&&!/Uploading/i.test(t)){ok=true;break;} }
    console.log('thumb upload ok:',ok); if(!ok){ console.log('ABORT: thumbnail not uploaded'); await b.close(); process.exit(0); }
  }
  await p.getByText('Package Type',{exact:true}).first().click(); await p.waitForTimeout(1200);
  const keysSel = 'input[id^="form.package_types."][id$=".room_option"]';
  const count = async()=> (await p.$$(keysSel)).length;
  while (await count() < 3) { const n=await count(); await p.getByRole('button',{name:'Add to package types'}).click(); await p.waitForFunction(([s,n])=>document.querySelectorAll(s).length>n,[keysSel,n],{timeout:20000}); await p.waitForTimeout(500); }
  const ids = await p.$$eval(keysSel, es=>es.map(e=>e.id.replace('.room_option','')));
  const rooms=[['Sekamar Berempat',4,'quad'],['Sekamar Bertiga',3,'triple'],['Sekamar Berdua',2,'double']];
  for (let i=0;i<3;i++) {
    const k=ids[i], [nm,ro,pk]=rooms[i];
    const set=async(f,v)=>{ const el=p.locator(`input[id="${k}.${f}"]`); await el.fill(''); await el.fill(String(v)); };
    await set('name',nm); await set('dp_amount',4000); await set('room_option',ro);
    for (const [f,v] of Object.entries(cfg.text)) await set(f,v);
    const pr=p.locator(`input[id="${k}.price"]`); await pr.fill(''); await pr.type(String(cfg[pk])); await p.waitForTimeout(400);
    const dp=p.locator(`input[id="${k}.discount_percent"]`); const want=Number(cfg[pk]).toLocaleString('en-US');
    for (let t=0;t<4;t++){ await dp.fill('1'); await p.waitForTimeout(1200); await dp.fill('0'); await p.keyboard.press('Tab'); await p.waitForTimeout(1800); if ((await p.locator(`input[id="${k}.discount_price"]`).inputValue())===want) break; }
  }
  const vals = await p.$$eval('input[id^="form.package_types."]', es=>es.filter(e=>e.type!=='hidden').map(e=>e.id.split('.').slice(-1)[0]+'='+e.value));
  console.log(vals.join(' | '));
  // facility hotels
  await p.getByText('Facility',{exact:true}).first().click(); await p.waitForTimeout(1500);
  const boxes = p.locator('label:visible').filter({has:p.locator('input[type=checkbox]')});
  const n = await boxes.count();
  for (let i=0;i<n;i++){ const lb=boxes.nth(i); const t=(await lb.innerText()).trim(); const cb=lb.locator('input[type=checkbox]'); const want=cfg.hotels.some(h=>t.toLowerCase().includes(h.toLowerCase())); if ((await cb.isChecked())!==want) await cb.setChecked(want); }
  console.log('hotels checked:', (await boxes.evaluateAll(ls=>ls.filter(l=>l.querySelector('input').checked).map(l=>l.innerText.trim()))));
  if (process.env.SAVE==='1') { await p.getByRole('button',{name:'Submit'}).click({timeout:10000}); await p.waitForTimeout(5000); console.log('notif', (await p.locator('.fi-no').allInnerTexts()).join('|')); }
  await b.close();
})();
