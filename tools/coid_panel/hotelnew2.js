const { chromium } = require(process.env.PWPATH);
const cfg = JSON.parse(process.env.CFG); // [{name,city,country,address,rating}]
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2000} });
  const p = await ctx.newPage();
  for (const h of cfg) {
    await p.goto('https://elharamainwisata.co.id/secret-admin/hotels/create', {waitUntil:'domcontentloaded',timeout:60000}); await p.waitForTimeout(5000);
    const opts = await p.$$eval('select[id="form.rating"] option', os=>os.map(o=>o.value+'='+o.text.trim()));
    if (!process.env.SAVE) { console.log('rating opts', opts.join(' | ')); }
    await p.fill('input[id="form.name"]', h.name);
    await p.fill('input[id="form.city"]', h.city);
    await p.fill('input[id="form.country"]', h.country);
    await p.fill('textarea[id="form.address"]', h.address);
    const ins = p.locator('input.filepond--browser');
    await ins.nth(0).setInputFiles(h.logo); await p.waitForTimeout(3000);
    await ins.nth(1).setInputFiles(h.thumb);
    let okU=false; for (let i=0;i<20;i++){ await p.waitForTimeout(2000); const t=(await p.locator('.filepond--file-status').allInnerTexts()).filter(x=>/Upload complete/i.test(x)).length; if(t>=2){okU=true;break;} }
    console.log(h.name,'uploads ok:',okU);
    const sel = p.locator('select[id="form.rating"]');
    const val = opts.find(o=>new RegExp('(^|=)'+h.rating+'( |$)').test(o)) ? null : null;
    await sel.selectOption({ label: h.ratingLabel }).catch(async()=>{ await sel.selectOption(String(h.rating)); });
    console.log(h.name, 'rating now', await sel.inputValue());
    if (process.env.SAVE==='1' && okU) {
      await p.getByRole('button',{name:/^Create$/}).first().click(); await p.waitForTimeout(4000);
      console.log('notif', (await p.locator('.fi-no').allInnerTexts()).join('|'), p.url());
    }
  }
  await b.close();
})();
