document.addEventListener("DOMContentLoaded", function() {
  // Esperar 4 segundos antes de ocultar el preloader
  setTimeout(function() {
      document.getElementById('preloader').style.display = 'none';
  }, 10000); // 4000 milisegundos = 4 segundos
});