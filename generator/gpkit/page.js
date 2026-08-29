
(function(){
  var IDS=__IDS__, KEY='__KEY__', MKEY='gp-explain-mode', TKEY='gradient_path_theme';

  /* ---- theme ---- */
  try{var st=localStorage.getItem(TKEY); if(st) document.documentElement.setAttribute('data-theme',st);}catch(e){}
  document.getElementById('theme').addEventListener('click',function(){
    var cur=document.documentElement.getAttribute('data-theme');
    if(!cur){cur = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark':'light';}
    var nxt = cur==='dark' ? 'light':'dark';
    document.documentElement.setAttribute('data-theme',nxt);
    try{localStorage.setItem(TKEY,nxt);}catch(e){}
  });

  /* ---- simple / technical -------------------------------------------
     This is a real mode, not a swapped paragraph. .tech-only is out of
     the flow in simple mode -- the math slab, the code block and the
     interview-grade drill answers all go with it. Every switch on the
     page stays in sync, and the switch in the sticky rail means you can
     change your mind at card 38 without scrolling back to the top. */
  var mode='simple';
  function setMode(m, keep){
    var anchor=null, before=0;
    if(keep){ anchor=keep; before=anchor.getBoundingClientRect().top; }
    mode = (m==='tech') ? 'tech' : 'simple';
    document.body.classList.toggle('mode-tech', mode==='tech');
    document.querySelectorAll('.modeswitch button').forEach(function(b){
      b.setAttribute('aria-pressed', b.dataset.mode===mode ? 'true':'false');
    });
    var d=document.getElementById('depth');
    if(d) d.textContent = mode==='tech'
      ? 'Showing the notation, the code and the interview-grade answers.'
      : 'Plain English only. The math and code are hidden until you switch.';
    try{localStorage.setItem(MKEY,mode);}catch(e){}
    /* switching modes changes the height of every card above you, so pin
       the card you were reading instead of letting the page jump */
    if(anchor){
      var after=anchor.getBoundingClientRect().top;
      window.scrollBy(0, after-before);
    }
  }
  document.querySelectorAll('.modeswitch button').forEach(function(b){
    b.addEventListener('click',function(){
      setMode(b.dataset.mode, b.closest('.card'));
    });
  });
  /* the per-card "show me the precise version" button */
  document.querySelectorAll('.tolevel').forEach(function(b){
    b.addEventListener('click',function(){
      var card=b.closest('.card');
      setMode(b.dataset.to||'tech', card);
      if(card) card.scrollIntoView({behavior:'smooth',block:'start'});
    });
  });
  var saved='simple'; try{saved=localStorage.getItem(MKEY)||'simple';}catch(e){}

  /* ---- status marks ---- */
  function load(){try{return JSON.parse(localStorage.getItem(KEY))||{};}catch(e){return {};}}
  function save(s){try{localStorage.setItem(KEY,JSON.stringify(s));}catch(e){}}
  var state=load();
  function paint(){
    IDS.forEach(function(id){
      var s=state[id]||'new';
      var dot=document.querySelector('[data-rail="'+id+'"] .dot');
      if(dot) dot.className='dot'+(s==='new'?'':' '+s);
      document.querySelectorAll('[data-for="'+id+'"] button').forEach(function(b){
        b.setAttribute('aria-pressed', b.dataset.s===s ? 'true':'false');
      });
    });
    var n=IDS.filter(function(id){return state[id]==='solid';}).length;
    document.getElementById('meter').innerHTML='<b>'+n+'</b> of '+IDS.length+' solid';
  }
  document.querySelectorAll('.statusbar button').forEach(function(b){
    b.addEventListener('click',function(){
      var id=b.parentElement.dataset.for;
      state[id]=(state[id]===b.dataset.s)?'new':b.dataset.s;
      save(state); paint();
    });
  });

  /* ---- copy prompt ---- */
  document.querySelectorAll('.copy').forEach(function(btn){
    var orig=btn.textContent;
    btn.addEventListener('click',function(){
      var pre=document.getElementById(btn.dataset.target); if(!pre) return;
      var t=pre.textContent, ok=false;
      try{
        var ta=document.createElement('textarea'); ta.value=t; ta.setAttribute('readonly','');
        ta.style.cssText='position:fixed;top:0;left:0;opacity:0';
        document.body.appendChild(ta); ta.select(); ta.setSelectionRange(0,t.length);
        ok=document.execCommand('copy'); document.body.removeChild(ta);
      }catch(e){}
      function win(){btn.textContent='Copied'; btn.classList.add('done');
        setTimeout(function(){btn.textContent=orig; btn.classList.remove('done');},1800);}
      function fallback(){var d=pre.closest('details'); if(d) d.open=true;
        var r=document.createRange(); r.selectNodeContents(pre);
        var sel=window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
        btn.textContent='Selected — press Ctrl/Cmd + C';
        setTimeout(function(){btn.textContent=orig;},4000);}
      if(ok){win(); return;}
      if(navigator.clipboard){navigator.clipboard.writeText(t).then(win).catch(fallback); return;}
      fallback();
    });
  });

  /* ---- pick tonight's topic ---- */
  document.getElementById('pick').addEventListener('click',function(){
    var fuzzy=IDS.filter(function(i){return state[i]==='fuzzy';});
    var fresh=IDS.filter(function(i){return !state[i]||state[i]==='new';});
    var pool=fuzzy.length?fuzzy:(fresh.length?fresh:IDS);
    var el=document.getElementById(pool[Math.floor(Math.random()*pool.length)]);
    if(el) el.scrollIntoView({behavior:'smooth',block:'start'});
  });

  /* ---- rail highlight ---- */
  var links={}; document.querySelectorAll('[data-rail]').forEach(function(a){links[a.dataset.rail]=a;});
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){var a=links[e.target.id]; if(a) a.classList.toggle('here', e.isIntersecting);});
    },{rootMargin:'-15% 0px -70% 0px'});
    IDS.forEach(function(id){var el=document.getElementById(id); if(el) io.observe(el);});
  }

  paint(); setMode(saved);
  window.__setMode=setMode; window.__mode=function(){return mode;};
})();
