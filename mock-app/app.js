
const qs=s=>document.querySelector(s);const qsa=s=>[...document.querySelectorAll(s)];
qsa('.nav button').forEach(b=>b.onclick=()=>{qsa('.nav button').forEach(x=>x.classList.remove('active'));b.classList.add('active')});
function stamp(msg){const t=qs('#terminal'); if(!t)return; const now=new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit',second:'2-digit'}); t.innerHTML += `\n<span style="color:#7890aa">[${now}]</span> ${msg}`; t.scrollTop=t.scrollHeight}

qs('#diag').onclick=()=>{stamp('Running HTTP/TCP checks...');setTimeout(()=>stamp('<span style="color:#85e7aa">OK</span> • latency and reachability within thresholds'),450)};
qs('#incident').onclick=()=>{qs('#api .dot').className='dot bad';qs('#apibadge').textContent='Critical';qs('#healthy').textContent='3 / 4';qs('#incidents').textContent='1';stamp('<span style="color:#ff8e8e">CRITICAL</span> • application-api check failed • evidence recorded');};
qs('#backup').onclick=()=>{stamp('Creating backup copy and calculating SHA-256...');setTimeout(()=>stamp('<span style="color:#85e7aa">VERIFIED</span> • source hash matches backup hash'),550)};
