// /! Pas fonctionnel
document.addEventListener('DOMContentLoaded', () => {
  // Obtenez l'URL actuelle
  const currentPath = window.location.pathname;
  const url = `form[action="/${pathname}"]`
  let form = document.querySelector(url);

  switch (pathname) {
    case 'profile':
      form.style.display = 'none';
      break;
      
    case 'dashboard':
      form.style.display = 'none';
      break;
    default:
      break;
  }
  // Sélectionnez le formulaire avec l'action "/profile"
  const profileForm = document.querySelector('form[action="/profile"]');

  // Masquez le formulaire si l'URL correspond à une route spécifique
  if (currentPath === '/some_specific_route') {
      profileForm.style.display = 'none';
  }
});