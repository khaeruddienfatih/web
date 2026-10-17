const { chromium } = require(process.env.PWPATH);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const ctx = await b.newContext({ ignoreHTTPSErrors:true });
  const p = await ctx.newPage();
  await p.goto('https://elharamainwisata.co.id/secret-admin/login', {waitUntil:'networkidle'});
  await p.fill('input[id="form.email"]', process.env.ELHARAMAINCOID_ADMIN_EMAIL);
  await p.fill('input[id="form.password"]', process.env.ELHARAMAINCOID_ADMIN_PASSWORD);
  await p.click('button[type=submit]');
  await p.waitForTimeout(6000);
  console.log('URL', p.url()); console.log((await p.innerText('body')).slice(0,600)); await p.screenshot({path:'login.png'});
  const links = await p.$$eval('nav a, aside a', as => as.map(a => a.textContent.trim().replace(/\s+/g,' ') + ' -> ' + a.href));
  console.log([...new Set(links)].join('\n'));
  await ctx.storageState({ path: 'state.json' });
  await b.close();
})();
