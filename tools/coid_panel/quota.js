const { chromium } = require(process.env.PWPATH);
const cfg = JSON.parse(process.env.CFG); // {id, quotas:{'2027-01-03':31}}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2200} });
  const p = await ctx.newPage();
  await p.goto(`https://elharamainwisata.co.id/secret-admin/travel-packages/${cfg.id}/edit`, {waitUntil:'networkidle'}); await p.waitForTimeout(2500);
  await p.getByText('Available Date',{exact:true}).first().click(); await p.waitForTimeout(800);
  const dates = await p.$$eval('input[id^="form.available_dates."][id$=".date"]', es=>es.map(e=>[e.id,e.value]));
  for (const [id,v] of dates) if (cfg.quotas[v]!==undefined) { const qid=id.replace('.date','.quota'); await p.fill(`input[id="${qid}"]`, String(cfg.quotas[v])); }
  await p.getByText('Facility',{exact:true}).first().click(); await p.waitForTimeout(800);
  await p.getByRole('button',{name:'Submit'}).click({timeout:10000}); await p.waitForTimeout(4000);
  console.log('notif', (await p.locator('.fi-no').allInnerTexts()).join('|'));
  await p.goto(`https://elharamainwisata.co.id/secret-admin/travel-packages/${cfg.id}/edit`, {waitUntil:'networkidle'}); await p.waitForTimeout(2500);
  console.log(await p.$$eval('input[id^="form.available_dates."]', es=>es.map(e=>e.value).join(' ')));
  const t = await p.locator('table').first().innerText();
  console.log('hotel rows', (t.match(/malam/g)||[]).length, t.includes('31 Jan 2027'));
  await b.close();
})();
