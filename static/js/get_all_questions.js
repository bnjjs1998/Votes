
const flashMessages = document.querySelectorAll('#flash-messages .alert');
// Applique l'effet d'apparition (fade-in) à chaque message
flashMessages.forEach((message, index) => {
  // Ajout de la classe fade-in pour l'apparition
  message.classList.add('fade-in');

  // Déclenche la disparition après un délai (ex. : 3 secondes)
  setTimeout(() => {
      message.classList.remove('fade-in'); // Retire l'effet d'apparition
      message.classList.add('fade-out'); // Ajoute l'effet de disparition

      // Supprime le message après la disparition complète
      setTimeout(() => {
          message.remove();
      }, 3000); // Durée de l'animation fade-out (1 seconde ici)
  }, 3000 + index * 200); // Décalage pour chaque message
});

fetch('/api_get_all_questions', {
    method: 'GET',
})
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur de récupération des questions');
        }
        return response.json();
    })
    .then(data => {
        console.log('Données reçues:', data);
        const { questions, user_role } = data;
        const questionsContainer = document.getElementById('questions-container');
        questionsContainer.innerHTML = '';

        questions.forEach(question => {
            const questionForm = document.createElement('form');
            questionForm.setAttribute('method', 'POST');
            questionForm.setAttribute('action', '/Post_vote');
            questionForm.classList.add('formVote', 'tooltip');

            // Titre de la question
            const title = document.createElement('h3');
            title.textContent = `• ${question.title_question}`;
            questionForm.appendChild(title);

            const expirationDate = document.createElement('p');
            expirationDate.textContent = `Date d'expiration : ${new Date(question.expiration_date).toLocaleString()}`;
            expirationDate.style.fontStyle = 'italic'; // Optionnel : ajoute du style
            expirationDate.style.marginTop = '10px'; // Ajout d'une marge supérieure
            expirationDate.style.marginBottom = '10px'; // Ajout d'une marge inférieure
            questionForm.appendChild(expirationDate);

            
            // Dictionnaire pour stocker les réponses
            const answers = {
                _id: question._id,
                title_question: question.title_question,
                choices: {}, // Dictionnaire pour les choix et leurs scores
            };

            // Parcours des choix dans la question
            question.choices.forEach((choice, index) => {
                const div = document.createElement('div');
                div.classList.add('input_container');
                div.classList.add('number_input');

                // Création des différents labels pour l'input
                const label = document.createElement('label');
                label.setAttribute('for', `choice${question._id}_${index}`);
                label.textContent = `${index + 1}. ${choice} :`;

                // Création de l'input en fonction de ce qu'il trouve dans le document mongo
                const input = document.createElement('input');
                input.setAttribute('id', `choice${question._id}_${index}`);
                input.setAttribute('type', 'number');
                input.setAttribute('name', `question${question._id}`);
                input.setAttribute('placeholder', 'Classer votre préférence');
                input.setAttribute('min', '1');
                input.setAttribute('max', '3');
                input.value = '0';
                
                // Mise à jour des réponses
                input.addEventListener('change', function () {
                  answers.choices[choice] = parseInt(input.value, 10); // Enregistre chaque choix avec son score
                });

                questionForm.appendChild(div);
                div.appendChild(label);
                div.appendChild(input);
              });
              
              const buttonPostVote = document.createElement('button');
              buttonPostVote.textContent = 'Vote';
              buttonPostVote.setAttribute('id', 'submit_button');
              buttonPostVote.setAttribute('type', 'submit');
              buttonPostVote.classList.add('button');
              const tooltip = document.createElement('span');
              tooltip.classList.add('tooltiptext');
              tooltip.textContent = 'Classez vos choix de 1 à 3, par ordre de préférence.';
              questionForm.appendChild(buttonPostVote);
              questionForm.appendChild(tooltip);
              
              questionsContainer.appendChild(questionForm);
              // Si l'utilisateur est admin, ajoutez un bouton de suppression
              if (user_role === 'admin') {
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Supprimer ce sondage';
                deleteButton.classList.add('button', 'danger');
                deleteButton.addEventListener('click', () => {
                    if (confirm('Voulez-vous vraiment supprimer ce sondage ?')) {
                        fetch('/delete_vote', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ question_id: question._id })
                        })
                            .then(response => response.json())
                            .then(result => {
                                if (result.success) {
                                    alert('Sondage supprimé avec succès.');
                                    questionDiv.remove();
                                } else {
                                    alert(result.error || 'Erreur lors de la suppression.');
                                }
                            })
                            .catch(error => {
                                console.error('Erreur lors de la suppression:', error);
                                alert('Une erreur est survenue.');
                            });
                    }
                });
                questionForm.appendChild(deleteButton);
            }

            // Gestion de la soumission du formulaire
            questionForm.addEventListener('submit', function (event) {
                event.preventDefault();

                console.log('Réponses collectées:', answers);
                fetch('/Vote', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(answers), // Envoi du dictionnaire de réponses
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Réponse du serveur:', answers, data);
                    })
                    .catch(error => {
                        console.error('Erreur lors de l\'envoi des données:', error);
                    });
            });
        });
    })
    .catch(error => {
        console.error('Erreur de récupération des questions:', error);
    });
