console.log('Ici je peux modifier mon profil et le supprimer');

// URL de l'API pour récupérer les informations utilisateur
const url = '/Get_modifie_profile';

// Fonction pour récupérer et afficher les informations utilisateur
function fetchUserProfile() {
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include', // Inclure les cookies de session pour Flask-Login
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // Convertir la réponse en JSON
        })
        .then(data => {
            console.log('Données reçues:', data);
            // Afficher les informations utilisateur dans la page
            const userInfo = `
                <p><strong>Username:</strong> ${data.username}</p>
                <p><strong>Email:</strong> ${data.email}</p>
            `;
            document.getElementById('informations_user').innerHTML = userInfo;
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des informations utilisateur:', error);
        });
}

// Fonction pour mettre à jour l'email
function updateUserEmail() {
    const emailInput = document.getElementById('email_modifie').value;
    if (!emailInput) {
        alert('Veuillez saisir un nouvel email.');
        return;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include', // Inclure les cookies de session pour Flask-Login
        body: JSON.stringify({ email: emailInput }), // Envoyer le nouvel email
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // Convertir la réponse en JSON
        })
        .then(data => {
            console.log('Profil mis à jour:', data);
            alert('Votre email a été mis à jour avec succès.');
            // Mettre à jour l'affichage avec les nouvelles données
            fetchUserProfile();
        })
        .catch(error => {
            console.error('Erreur lors de la mise à jour de l\'email:', error);
        });
}

// Ajouter un écouteur d'événement au bouton de mise à jour
document.getElementById('update_email').addEventListener('click', (event) => {
    event.preventDefault(); // Empêche le comportement par défaut du formulaire
    updateUserEmail();
});

// Charger les informations utilisateur au chargement de la page
fetchUserProfile();
