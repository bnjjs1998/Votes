// URL de l'API
const apiUrl = '/get_sondage_current_id';
// Fonction pour appeler l'API
function fetchSondage() {
  fetch(apiUrl, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include' // Inclut les cookies pour gérer les sessions
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Erreur HTTP : ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Données reçues :', data)
    })
    .catch(error => {
      console.error('Erreur lors de la récupération des sondages :', error);
    });
}
console.log(document.cookie);









// Appeler la fonction lorsque la page est chargée
document.addEventListener('DOMContentLoaded', fetchSondage);

