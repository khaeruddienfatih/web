const { chromium } = require(process.env.PWPATH);
const cfg = JSON.parse(process.env.CFG); // {id, entries:[{date:'03 Jan 2027', hotel:'Al-aqeeq', in:'2027-01-03', out:'2027-01-06'}]}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:1800} });
  const p = await ctx.newPage();
  await p.goto(`https://elharamainwisata.co.id/secret-admin/travel-packages/${cfg.id}/edit`, {waitUntil:'networkidle'}); await p.waitForTimeout(2500);
  for (const e of cfg.entries) {
    await p.getByRole('button',{name:'Tambah Jadwal Hotel'}).click();
    await p.waitForTimeout(2500); const dlg = p.locator('[role=dialog]').last();
    const sel = dlg.locator('button.fi-select-input-btn');
    await sel.nth(0).click(); await p.waitForTimeout(500);
    await p.getByRole('option',{name:new RegExp('^'+e.date+' ')}).click(); await p.waitForTimeout(1000);
    await sel.nth(1).click(); await p.waitForTimeout(500);
    await p.getByRole('option',{name:new RegExp('^'+e.hotel)}).click(); await p.waitForTimeout(1200);
    const ci = dlg.locator('input[id$="check_in_date"]'), co = dlg.locator('input[id$="check_out_date"]');
    const pick = async (inp, iso) => {
      const [Y,M,D] = iso.split('-').map(Number);
      await inp.click(); await p.waitForTimeout(500);
      const panel = dlg.locator('.fi-fo-date-time-picker-panel:visible').first();
      await panel.locator('select').selectOption(String(M-1)); await p.waitForTimeout(300);
      const yr = panel.locator('input[type=number]'); await yr.fill(String(Y)); await p.waitForTimeout(900);
      await panel.getByText(String(D),{exact:true}).first().click(); await p.waitForTimeout(500);
    };
    await pick(ci, e.in); await pick(co, e.out);
    console.log('vals', await ci.inputValue(), await co.inputValue());
    if (process.env.SAVE==='1') {
      await dlg.getByRole('button',{name:'Create',exact:true}).click(); await p.waitForTimeout(3000);
      console.log('notif', (await p.locator('.fi-no').allInnerTexts()).join('|'));
    } else { await p.screenshot({path:'hotel1.png'}); break; }
  }
  const rows = await p.$$eval('table tbody tr', trs=>trs.map(t=>t.innerText.replace(/\s+/g,' ').trim()));
  console.log(rows.join('\n'));
  await b.close();
})();
