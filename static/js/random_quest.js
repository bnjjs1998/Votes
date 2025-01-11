fetch('/get_questions', {
    method: 'GET', // méthode de requête
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}` // Ajoutez un token d'authentification si nécessaire
    }
})
  .then(response => {
      if (!response.ok) {
          throw new Error('Erreur de récupération des questions');
      }
      return response.json(); // Convertir la réponse en JSON
  })
  .then(data => {
      console.log('Données reçues:', data); // Affiche toute la réponse reçue
      if (data && data.questions) {
          console.log('Questions:', data.questions); // Affiche les questions si elles existent

          const questionsContainer = document.getElementById('questions-container');

          data.questions.forEach(question => {
              // Créer un conteneur pour la question
              const questionDiv = document.createElement('div');

              // Créer un titre pour la question
              const title = document.createElement('h2');
              title.textContent = question.title_question;
              questionDiv.appendChild(title);

              // Créer un créateur de la question
              const creator = document.createElement('p');
              creator.textContent = `Créé par: ${question['Créateur']}`;
              questionDiv.appendChild(creator);

              // Créer les choix sous forme de radio boutons
              question.choices.forEach((choice, index) => {
                  const label = document.createElement('label');
                  label.textContent = `Choice ${choice}`;
                  label.setAttribute('for', `choice${question._id}_${index}`);

                  const input = document.createElement('input');
                  input.setAttribute('id', `choice${question._id}_${index}`);
                  input.setAttribute('type', 'number');
                  input.setAttribute('name', `question${question._id}`); // Groupement des radios par question
                  input.setAttribute('value', choice);

                  questionDiv.appendChild(label);
                  questionDiv.appendChild(input);
              });

              // Ajouter le conteneur de la question au conteneur principal
              questionsContainer.appendChild(questionDiv);
          });
      } else {
          console.log('Aucune question trouvée dans la réponse');
      }
  })
  .catch(error => {
      console.error('Erreur:', error); // Affiche l'erreur en cas de problème
  });
