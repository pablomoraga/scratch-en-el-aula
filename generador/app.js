// Marcar retos como hechos (se guarda solo en este navegador)
(function () {
  var KEY = 'scratch-en-el-aula-hechos';
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }
  var done = load();
  function slugOf(href) { var m = (href || '').match(/([^\/]+)\.html$/); return m ? m[1] : null; }
  function paint() {
    document.querySelectorAll('.side li a, .card').forEach(function (a) {
      var s = slugOf(a.getAttribute('href')); a.classList.toggle('done', !!(s && done[s]));
    });
  }
  var here = slugOf(location.pathname);
  var isReto = document.querySelector('.ficha');
  if (isReto && here) {
    var b = document.createElement('button'); b.className = 'done-btn';
    function label() { b.textContent = done[here] ? '✓ Reto hecho' : 'Marcar como hecho'; b.classList.toggle('on', !!done[here]); }
    b.onclick = function () { if (done[here]) delete done[here]; else done[here] = 1; save(done); label(); paint(); };
    label(); var pn = document.querySelector('.pn'); pn.parentNode.insertBefore(b, pn);
  }
  document.querySelectorAll('details.jugar').forEach(function (d) {
    d.addEventListener('toggle', function () {
      var f = d.querySelector('iframe');
      if (d.open && f && !f.getAttribute('src')) f.setAttribute('src', f.getAttribute('data-src'));
    });
  });
  paint();
  var on = document.querySelector('.side a.on'), side = document.querySelector('.side'); if (on && side) side.scrollTop = on.offsetTop - side.offsetTop - 120;
})();
