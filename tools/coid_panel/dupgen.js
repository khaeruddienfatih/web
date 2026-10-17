const { chromium } = require(process.env.PWPATH);
(async () => {
  const src = process.env.SRC;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:1500} });
  const p = await ctx.newPage();
  const ids = async () => { await p.goto('https://elharamainwisata.co.id/secret-admin/travel-packages', {waitUntil:'networkidle'}); await p.waitForTimeout(1500); const h=await p.content(); return [...new Set([...h.matchAll(/table\.records\.(\d+)/g)].map(x=>x[1]))]; };
  const before = await ids();
  await p.locator(`[wire\\:key$="table.records.${src}"]`).getByText('Duplikasi').click(); await p.waitForTimeout(1500);
  await p.getByRole('button',{name:'Ya, Duplikasi'}).click(); await p.waitForTimeout(5000);
  const after = await ids();
  console.log('NEWID', after.filter(x=>!before.includes(x)).join(','));
  await b.close();
})();
