// Reproducible Chromium mobile simulation. This is not field Core Web Vitals.
import {chromium} from '@playwright/test';
import {writeFile} from 'node:fs/promises';
const browser=await chromium.launch();const results=[];
for(let run=1;run<=3;run++)for(const path of ['/','/resultats.html','/club.html','/stage-ete.html','/u11-mixte.html']){
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1});const page=await context.newPage();
 const cdp=await context.newCDPSession(page);await cdp.send('Network.enable');await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
 await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:150,downloadThroughput:1600000/8,uploadThroughput:750000/8,connectionType:'cellular4g'});await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
 await page.addInitScript(()=>{window.audit={lcp:0,cls:0,longTasks:[]};new PerformanceObserver(list=>{for(const e of list.getEntries())window.audit.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.audit.cls+=e.value}).observe({type:'layout-shift',buffered:true});new PerformanceObserver(list=>{for(const e of list.getEntries())window.audit.longTasks.push({start:e.startTime,duration:e.duration})}).observe({type:'longtask',buffered:true})});
 try{
  await page.goto((process.env.PHB_BASE_URL || 'https://ploufragan-handball.fr')+path,{waitUntil:'load',timeout:90000});await page.waitForTimeout(5000);
  const metrics=await page.evaluate(()=>({lcpMs:Math.round(window.audit.lcp),cls:Number(window.audit.cls.toFixed(4)),fcpMs:Math.round(performance.getEntriesByName('first-contentful-paint')[0]?.startTime||0),ttfbMs:Math.round(performance.getEntriesByType('navigation')[0].responseStart),observedEncodedBytes:performance.getEntriesByType('resource').reduce((s,r)=>s+r.encodedBodySize,0),longTasks:window.audit.longTasks,tbtApproxMs:Math.round(window.audit.longTasks.filter(t=>t.start>= (performance.getEntriesByName('first-contentful-paint')[0]?.startTime||0)).reduce((s,t)=>s+Math.max(0,t.duration-50),0))}));
  results.push({path,run,...metrics});console.log(run,path,metrics.lcpMs,metrics.cls,metrics.observedEncodedBytes);
 }catch(e){results.push({path,run,error:e.message});console.log('ERROR',path,e.message)}
 await context.close();await writeFile('reports/mobile-lab-audit.json',JSON.stringify({protocol:{viewport:'390x844',cpuSlowdown:4,latencyMs:150,downloadMbps:1.6,uploadMbps:.75,repeats:3,cache:'disabled',observation:'load + 5 seconds',fieldData:false},results},null,2));
}
await browser.close();
