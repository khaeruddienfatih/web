const { chromium } = require(process.env.PWPATH);
const cfg = JSON.parse(process.env.CFG); // [{id, which:'std'|'arb'}]
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2400} });
  await ctx.route(/r2\.cloudflarestorage\.com/, async route => { try { const r = await route.fetch(); await route.fulfill({ response: r, headers:{...r.headers(),'access-control-allow-origin':'*'} }); } catch(e){ await route.abort(); } });
  const p = await ctx.newPage();
  for (const c of cfg) {
    await p.goto(`https://elharamainwisata.co.id/secret-admin/haji-packages/${c.id}/edit`, {waitUntil:'domcontentloaded',timeout:60000}); await p.waitForTimeout(7000);
    await p.getByText('Itinerary',{exact:true}).first().click(); await p.waitForTimeout(2000);
    const boxes = p.locator('label:visible').filter({has:p.locator('input[type=checkbox]')}).filter({hasText:/Dzulhijjah/});
    const n = await boxes.count();
    // std entries are the first 19 Dzulhijjah labels, arbain the last 21
    const lo = c.which==='std' ? 0 : n-21, hi = c.which==='std' ? 19 : n;
    for (let i=0;i<n;i++){ const cb=boxes.nth(i).locator('input[type=checkbox]'); const want=(i>=lo&&i<hi); if ((await cb.isChecked())!==want) await cb.setChecked(want); }
    const checked = await boxes.evaluateAll(ls=>ls.filter(l=>l.querySelector('input').checked).map(l=>l.innerText.trim().split('\n')[0]));
    console.log(c.id,c.which,'dz labels',n,'checked',checked.length,'|',checked[0],'...',checked[checked.length-1]);
    await p.getByText('Facility',{exact:true}).first().click(); await p.waitForTimeout(1000);
    await p.getByRole('button',{name:'Submit'}).click({timeout:10000}); await p.waitForTimeout(5000);
    console.log(c.id,'notif',(await p.locator('.fi-no').allInnerTexts()).join('|'));
  }
  await b.close();
})();
