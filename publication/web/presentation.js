// Keep exact-result links useful when numeric evidence is collapsed by default.
function revealTarget(){
 let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
 if(!id)return;const target=document.getElementById(id);if(!target)return;
 let changed=false;for(let p=target.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS'&&!p.open){p.open=true;changed=true;}
 if(changed)requestAnimationFrame(()=>target.scrollIntoView({block:'start',behavior:'instant'}));
}
addEventListener('hashchange',revealTarget);revealTarget();
