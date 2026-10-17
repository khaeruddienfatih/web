const { chromium } = require(process.env.PWPATH);
const cfg = JSON.parse(process.env.CFG);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ storageState:'state.json', viewport:{width:1500,height:2400} });
  const p = await ctx.newPage();
  await p.goto('https://elharamainwisata.co.id/secret-admin/itinerary-templates/create', {waitUntil:'domcontentloaded',timeout:60000}); await p.waitForTimeout(6000);
  await p.fill('input[id="form.title"]', cfg.name);
  await p.fill('textarea[id="form.description"]', cfg.desc);
  const titleSel='input[id^="form.itineraries."][id$=".title"]';
  while ((await p.$$(titleSel)).length < cfg.days.length) {
    const n=(await p.$$(titleSel)).length;
    await p.getByRole('button',{name:'Add to itineraries'}).click();
    await p.waitForFunction(([s,n])=>document.querySelectorAll(s).length>n,[titleSel,n],{timeout:20000}); await p.waitForTimeout(300);
  }
  const titles = await p.$$(titleSel), locs = await p.$$('input[id^="form.itineraries."][id$=".location"]'), eds = await p.$$('.tiptap.ProseMirror');
  console.log('items', titles.length, locs.length, eds.length);
  for (let i=0;i<cfg.days.length;i++){ const [t,l,d]=cfg.days[i]; await titles[i].fill(t); await locs[i].fill(l); await eds[i].click(); await p.keyboard.type(d,{delay:0}); }
  console.log('filled', cfg.days.length);
  if (process.env.SAVE==='1'){ await p.getByRole('button',{name:/^Create$/}).first().click(); await p.waitForTimeout(5000); console.log('notif',(await p.locator('.fi-no').allInnerTexts()).join('|'), p.url()); }
  await b.close();
})();
