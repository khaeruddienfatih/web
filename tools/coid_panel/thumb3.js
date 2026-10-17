const { chromium } = require(process.env.PWPATH);
const cfg = JSON.parse(process.env.CFG);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2200} });
  await ctx.route(/r2\.cloudflarestorage\.com/, async route => {
    try { const resp = await route.fetch(); await route.fulfill({ response: resp, headers: { ...resp.headers(), 'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'GET,HEAD,OPTIONS' } }); }
    catch(e){ await route.abort(); }
  });
  const p = await ctx.newPage();
  for (const c of cfg) {
    await p.goto(`https://elharamainwisata.co.id/secret-admin/travel-packages/${c.id}/edit`, {waitUntil:'domcontentloaded',timeout:60000}); await p.waitForTimeout(7000);
    const rm = p.locator('.filepond--action-remove-item');
    for (let i=0;i<4 && await p.locator('.filepond--item').count();i++){ await rm.first().click({force:true}).catch(()=>{}); await p.waitForTimeout(2500); }
    if (await p.locator('.filepond--item').count()) { console.log(c.id,'old thumbnail not removed; skip'); continue; }
    await p.locator('input.filepond--browser').first().setInputFiles(c.file);
    let ok=false; for (let i=0;i<25;i++){ await p.waitForTimeout(2000); const t=(await p.locator('.filepond--file-status').allInnerTexts()).join('|'); if(/Upload complete/i.test(t)&&!/Uploading/i.test(t)){ok=true;break;} }
    console.log(c.id,'upload ok:',ok);
    if(!ok){ console.log(c.id,'SKIP save'); continue; }
    await p.getByText('Facility',{exact:true}).first().click(); await p.waitForTimeout(1000);
    await p.getByRole('button',{name:'Submit'}).click({timeout:10000}); await p.waitForTimeout(5000);
    console.log(c.id,'notif', (await p.locator('.fi-no').allInnerTexts()).join('|'));
  }
  await b.close();
})();
