document.querySelectorAll('.team-shortcut-tabs').forEach(nav=>{
 const links=[...nav.querySelectorAll('a')];
 const update=()=>links.forEach(link=>{
  if(location.hash&&link.hash===location.hash)link.setAttribute('aria-current','location');
  else link.removeAttribute('aria-current');
 });
 addEventListener('hashchange',update);update();
});
