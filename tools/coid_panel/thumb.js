const { chromium } = require(process.env.PWPATH);
const cfg = JSON.parse(process.env.CFG); // [{id, file}]
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2200} });
  const p = await ctx.newPage();
  for (const c of cfg) {
    await p.goto(`https://elharamainwisata.co.id/secret-admin/travel-packages/${c.id}/edit`, {waitUntil:'domcontentloaded',timeout:60000}); await p.waitForTimeout(5000);
    // remove existing file
    const rm = p.locator('.filepond--action-remove-item');
    const n = await rm.count();
    for (let i=0;i<n;i++) { await rm.first().click().catch(()=>{}); await p.waitForTimeout(1500); }
    await p.locator('input.filepond--browser').first().setInputFiles(c.file);
    let ok=false;
    for (let i=0;i<20;i++){ await p.waitForTimeout(2000); const t=(await p.locator('.filepond--file-status').allInnerTexts()).join('|'); if(/Upload complete/i.test(t) && !/Uploading/i.test(t)){ok=true;break;} }
    console.log(c.id,'upload ok:',ok);
    if(!ok){ console.log(c.id,'SKIP save (upload not complete)'); continue; }
    await p.getByText('Facility',{exact:true}).first().click(); await p.waitForTimeout(1000);
    await p.getByRole('button',{name:'Submit'}).click({timeout:10000}); await p.waitForTimeout(5000);
    console.log(c.id,'notif', (await p.locator('.fi-no').allInnerTexts()).join('|'));
  }
  await b.close();
})();
