#!/usr/bin/env python3
"""Make the Simple/Technical switch real on the three pages built before the
two-layer contract existed (01, 03, 04).

Those pages already carry .say-simple / .say-tech, but the switch only swapped
the opening paragraph -- the math slab and the code block stayed on screen, so
"Explain simply" still handed you a wall of notation. This does not rewrite
their content (it is generator output and the generator's content files are
gone). It does three structural things:

  1. hides the math slab and the code block in simple mode, the two blocks that
     made the mode meaningless
  2. puts a mode switch in the sticky rail, so the choice is reachable from
     card 38 and not only from the top of a 2 MB page
  3. adds the line that tells a simple reader what is being withheld, with the
     button that reveals it

It runs as a second <script> after the page's own, and leans on window.__setMode
which the original page already exposes.
"""
import sys, os, re
import os as _os
ROOT = _os.path.dirname(_os.path.abspath(__file__))

CSS_MARK = '/* ============================================================ *'


def new_css():
    css = open(os.path.join(ROOT, 'gpkit', 'page.css')).read()
    i = css.index(CSS_MARK)
    return css[i:]


RETRO_JS = r"""
/* ---- retrofit: make Simple mode a real mode on this page ---------------
   Written by the module 05/06 build. The page's own script owns the state;
   this only adds what the two-layer contract needs and was not built in. */
(function(){
  var MKEY='gp-explain-mode';

  /* 1. the two blocks that made simple mode pointless */
  var hidden=0;
  document.querySelectorAll('.card > .blk').forEach(function(b){
    var kid=b.firstElementChild, has=false;
    for(var n=b.children.length-1;n>=0;n--){
      var c=b.children[n];
      if(c.classList && (c.classList.contains('slab')||c.classList.contains('codewrap'))) has=true;
    }
    if(has){ b.classList.add('tech-only'); hidden++; }
  });

  /* 2. a switch in the sticky rail */
  var rail=document.querySelector('.rail');
  if(rail){
    var d=document.createElement('div');
    d.className='rail-mode';
    d.innerHTML='<h2 class="lbl">Reading at</h2>'
      +'<div class="modeswitch" role="group" aria-label="Explanation depth">'
      +'<button type="button" data-mode="simple">Simple</button>'
      +'<button type="button" data-mode="tech">Technical</button></div>'
      +'<span class="depth" id="depth"></span>';
    rail.insertBefore(d, rail.firstChild);
  }

  /* 3. tell a simple reader what is being withheld, and hand them the control */
  document.querySelectorAll('.card').forEach(function(card){
    var hasMath = !!card.querySelector('.slab');
    var hasCode = !!card.querySelector('.codewrap');
    if(!hasMath && !hasCode) return;
    var bits=[];
    if(hasMath) bits.push('the formula');
    if(hasCode) bits.push('the code');
    var listed = bits.length>1 ? (bits.slice(0,-1).join(', ')+' and '+bits[bits.length-1]) : bits[0];
    listed = listed.charAt(0).toUpperCase()+listed.slice(1);
    var u=document.createElement('div');
    u.className='upshift simple-only';
    u.innerHTML='<p>You are reading the plain version. <b>'+listed+'</b>, and the precise '
      +'wording of this card, are one switch away.</p>'
      +'<button type="button" class="tolevel" data-to="tech">Show the precise version</button>';
    var practice=card.querySelector('.practice');
    if(practice) card.insertBefore(u, practice); else card.appendChild(u);
  });

  /* 4. wire the new controls through the page's own setMode, keeping the card
        you are reading pinned -- switching changes the height of everything
        above you, so without this the page jumps somewhere else entirely */
  function apply(m, keep){
    var before = keep ? keep.getBoundingClientRect().top : 0;
    if(window.__setMode) window.__setMode(m);
    document.querySelectorAll('.modeswitch button').forEach(function(b){
      b.setAttribute('aria-pressed', b.dataset.mode===m ? 'true':'false');
    });
    var dep=document.getElementById('depth');
    if(dep) dep.textContent = m==='tech'
      ? 'Showing the notation and the code.'
      : 'Plain English first. The math and code are hidden until you switch.';
    try{localStorage.setItem(MKEY,m);}catch(e){}
    if(keep) window.scrollBy(0, keep.getBoundingClientRect().top - before);
  }
  document.querySelectorAll('.modeswitch button').forEach(function(b){
    b.addEventListener('click', function(){ apply(b.dataset.mode, b.closest('.card')); });
  });
  document.querySelectorAll('.tolevel').forEach(function(b){
    b.addEventListener('click', function(){
      var card=b.closest('.card');
      apply(b.dataset.to||'tech', card);
      if(card) card.scrollIntoView({behavior:'smooth',block:'start'});
    });
  });

  var saved='simple'; try{saved=localStorage.getItem(MKEY)||'simple';}catch(e){}
  apply(saved, null);
})();
"""


def patch(path):
    s = open(path).read()
    if 'retrofit: make Simple mode a real mode' in s:
        print(f'{path}: already patched'); return
    # CSS goes at the end of the LAST style block (the page stylesheet)
    i = s.rindex('</style>')
    s = s[:i] + '\n' + new_css() + s[i:]
    # the retrofit script goes after the page's own
    j = s.rindex('</script>') + len('</script>')
    s = s[:j] + '<script>' + RETRO_JS + '</script>' + s[j:]
    open(path, 'w').write(s)
    print(f'{path}: patched  (+{len(new_css())/1000:.1f} KB css, +{len(RETRO_JS)/1000:.1f} KB js)')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        patch(p)
