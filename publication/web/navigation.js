const toggle=document.querySelector('.gb-menu-toggle');
const contents=document.getElementById('site-navigation');
if(toggle&&contents&&typeof HTMLDialogElement!=='undefined'&&typeof HTMLDialogElement.prototype.showModal==='function'){
  const dialog=document.createElement('dialog');
  dialog.id='site-navigation-dialog';dialog.className='gb-navigation-dialog';
  dialog.setAttribute('aria-labelledby','site-navigation-title');
  contents.before(dialog);dialog.append(contents);
  const close=contents.querySelector('.gb-menu-close');close.hidden=false;
  toggle.setAttribute('role','button');toggle.setAttribute('aria-haspopup','dialog');
  toggle.setAttribute('aria-controls',dialog.id);toggle.setAttribute('aria-expanded','false');
  let previousOverflow='',opened=false;
  function updateSection(){
    const links=[...contents.querySelectorAll('.gb-page-sections a')];let active=null;
    for(const link of links){link.removeAttribute('aria-current');const target=document.getElementById(link.hash.slice(1));if(target&&target.getBoundingClientRect().top<=150)active=link;}
    if(active)active.setAttribute('aria-current','location');
  }
  function open(){
    if(dialog.open)return;
    updateSection();previousOverflow=document.documentElement.style.overflow;
    dialog.showModal();opened=true;document.documentElement.style.overflow='hidden';
    toggle.setAttribute('aria-expanded','true');contents.scrollTop=0;close.focus({preventScroll:true});
  }
  function restore(){
    if(!opened||dialog.open)return;
    opened=false;document.documentElement.style.overflow=previousOverflow;
    toggle.setAttribute('aria-expanded','false');toggle.focus({preventScroll:true});
  }
  function shut(){if(dialog.open){dialog.close();restore();}}
  toggle.addEventListener('click',event=>{event.preventDefault();open();});
  toggle.addEventListener('keydown',event=>{if(event.key===' '){event.preventDefault();open();}});
  close.addEventListener('click',shut);
  dialog.addEventListener('cancel',event=>{event.preventDefault();shut();});
  dialog.addEventListener('close',restore);
  // Native modal dialog supplies Escape dismissal, focus containment and inert background.
  dialog.addEventListener('click',event=>{if(event.target===dialog){const r=contents.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)shut();}});
  contents.addEventListener('click',event=>{
    const link=event.target.closest('a');if(!link||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
    // Cloudflare canonicalizes .html URLs; the private host keeps the extension.
    const pagePath=path=>path.replace(/\/index(?:\.html)?$/,'/').replace(/\.html$/,'').replace(/\/$/,'');
    const url=new URL(link.href);if(url.origin===location.origin&&pagePath(url.pathname)===pagePath(location.pathname)){
      // Selecting the current page closes the menu without resetting a recorded view.
      if(!url.hash)event.preventDefault();
      shut();if(url.hash){const target=document.getElementById(decodeURIComponent(url.hash.slice(1)));requestAnimationFrame(()=>{if(target){target.setAttribute('tabindex','-1');target.focus({preventScroll:true});}});}
    }
  });
  window.addEventListener('pagehide',shut);
  // A fallback contents anchor remains useful when a reader enables JS after loading.
  if(location.hash==='#site-navigation')open();
}
