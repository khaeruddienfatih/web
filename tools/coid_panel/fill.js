const { chromium } = require(process.env.PWPATH);
const cfg = JSON.parse(process.env.CFG);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2200} });
  const p = await ctx.newPage();
  await p.goto(`https://elharamainwisata.co.id/secret-admin/travel-packages/${cfg.id}/edit`, {waitUntil:'networkidle'}); await p.waitForTimeout(2500);
  // step 1
  await p.fill('input[id="form.name"]', cfg.name);
  if (cfg.description) await p.fill('textarea[id="form.description"]', cfg.description);
  // step 2 prices
  await p.getByText('Package Type',{exact:true}).first().click(); await p.waitForTimeout(800);
  const typeInputs = await p.$$eval('input[id^="form.package_types."][id$=".name"]', es=>es.map(e=>[e.id,e.value]));
  for (const [id,val] of typeInputs) {
    const key = /Empat/.test(val)?'quad':/Tiga/.test(val)?'triple':'double';
    const pid = id.replace('.name','.price');
    await p.fill(`input[id="${pid}"]`, ''); await p.type(`input[id="${pid}"]`, String(cfg[key])); await p.waitForTimeout(400);
    const dpid = id.replace('.name','.discount_percent'); await p.fill(`input[id="${dpid}"]`, '1'); await p.waitForTimeout(700); await p.fill(`input[id="${dpid}"]`, '0'); await p.keyboard.press('Tab'); await p.waitForTimeout(900);
  }
  // step 3 dates: delete all then add
  await p.getByText('Available Date',{exact:true}).first().click(); await p.waitForTimeout(800);
  const delSel='button[title="Delete"][wire\\:click*="form.available_dates"]';
  for (let i=0;i<60;i++) {
    const n = await p.locator(delSel).count(); if (n<=1) break;
    await p.locator(delSel).first().click({timeout:10000}); await p.waitForFunction(([sel,n])=>document.querySelectorAll(sel).length<n,[delSel,n],{timeout:20000}).catch(()=>console.log('slow delete',n)); await p.waitForTimeout(300);
  }
  for (let k=1;k<cfg.dates.length;k++) {
    const before=(await p.$$('input[id^="form.available_dates."][id$=".date"]')).length;
    await p.getByRole('button',{name:'Add to package date'}).click();
    await p.waitForFunction(([sel,n])=>document.querySelectorAll(sel).length>n,['input[id^="form.available_dates."][id$=".date"]',before],{timeout:20000});
    await p.waitForTimeout(300);
  }
  const dates = await p.$$('input[id^="form.available_dates."][id$=".date"]');
  const quotas = await p.$$('input[id^="form.available_dates."][id$=".quota"]');
  for (let k=0;k<cfg.dates.length;k++) { await dates[k].fill(cfg.dates[k]); await quotas[k].fill(String((cfg.quotas&&cfg.quotas[cfg.dates[k]])??cfg.quota??45)); await p.waitForTimeout(200); }
  const vals = await p.$$eval('input[id^="form."],textarea[id^="form."]', es=>es.filter(e=>/name$|price$|discount_price$|\.date$|quota$/.test(e.id)).map(e=>e.id.replace('form.','')+'='+e.value));
  console.log(vals.join('\n'));
  if (process.env.SAVE==='1') {
    await p.getByText('Facility',{exact:true}).first().click(); await p.waitForTimeout(1000); await p.getByRole('button',{name:'Submit'}).click({timeout:10000}); await p.waitForTimeout(4000);
    console.log('SAVED', p.url(), (await p.locator('.fi-no').allInnerTexts()).join('|'));
  }
  await p.screenshot({path:'fill.png', fullPage:true});
  await b.close();
})();
