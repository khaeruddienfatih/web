const { chromium } = require(process.env.PWPATH);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2200} });
  const p = await ctx.newPage();
  for (const id of (process.env.IDS||"57,58,59,60,61,62").split(",").map(Number)) {
    await p.goto(`https://elharamainwisata.co.id/secret-admin/travel-packages/${id}/edit`, {waitUntil:'domcontentloaded',timeout:60000}); await p.waitForTimeout(5000);
    const f = await p.$$eval('input[id^="form."]', es=>Object.fromEntries(es.map(e=>[e.id.replace('form.',''),e.value])));
    const name=f.name, prices=Object.entries(f).filter(([k])=>/price$/.test(k)&&!/discount/.test(k)).map(([,v])=>v);
    const dq=Object.entries(f).filter(([k])=>/available_dates.*\.date$/.test(k)).map(([k,v])=>v.slice(5)+':'+f[k.replace('.date','.quota')]);
    const vis=await p.$$eval('button[role=switch]', bs=>bs.map(x=>x.getAttribute('aria-checked')));
    const rows=await p.$$eval('table tbody tr', trs=>trs.map(t=>t.innerText.replace(/\s+/g,' ').trim()));
    const pg=(await p.locator('text=/Showing .* results/').first().innerText().catch(()=>'')).replace(/\s+/g,' ');
    console.log(id,'|',name,'| visible',vis.join(','),'|',prices.join('/'),'|',dq.join(' '),'| hotel rows page1:',rows.length,pg);
  }
  await b.close();
})();
