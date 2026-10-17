const { chromium } = require(process.env.PWPATH);
const ids = process.env.IDS.split(',').map(Number);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2200} });
  await ctx.route(/r2\.cloudflarestorage\.com/, async route => { try { const r = await route.fetch(); await route.fulfill({ response: r, headers:{...r.headers(),'access-control-allow-origin':'*'} }); } catch(e){ await route.abort(); } });
  const p = await ctx.newPage();
  for (const id of ids) {
    await p.goto(`https://elharamainwisata.co.id/secret-admin/travel-packages/${id}/edit`, {waitUntil:'domcontentloaded',timeout:60000}); await p.waitForTimeout(7000);
    const sw = p.locator('button[role=switch]').first();
    const before = await sw.getAttribute('aria-checked');
    if (before!=='true') { await sw.click(); await p.waitForTimeout(800); }
    const after = await sw.getAttribute('aria-checked');
    await p.getByText('Facility',{exact:true}).first().click(); await p.waitForTimeout(1000);
    await p.getByRole('button',{name:'Submit'}).click({timeout:10000}); await p.waitForTimeout(5000);
    console.log(id,'visible',before,'->',after,'|',(await p.locator('.fi-no').allInnerTexts()).join('|'));
  }
  await b.close();
})();
