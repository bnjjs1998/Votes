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

          // Fonction pour générer dynamiquement les questions avec leurs choix
          function Question(data) {
              this._id = data._id;
              this.title_question = data.title_question;
              this.choices = data.choices;
              this.creator = data['Créateur'];
          }

          Question.prototype.render = function(containerId) {
              const questionsContainer = document.getElementById(containerId);

              // Créer un titre pour la question
              const title = document.createElement('h2');
              title.textContent = this.title_question;
              questionsContainer.appendChild(title);

              // Créer un créateur de la question
              const creator = document.createElement('p');
              creator.textContent = `Créé par: ${this.creator}`;
              questionsContainer.appendChild(creator);

              // Parcourir les choix et créer un label et un input pour chaque choix
              this.choices.forEach((choice, index) => {
                  const label = document.createElement('label');
                  label.textContent = `Choice ${choice}`;
                  label.setAttribute('for', `choice${index}`);

                  const input = document.createElement('input');
                  input.setAttribute('id', `choice${index}`);
                  input.setAttribute('type', 'number');
                  input.setAttribute('name', `question${this._id}`);
                  input.setAttribute('value', choice);
                  questionsContainer.appendChild(label);
                  questionsContainer.appendChild(input);
              });
          };

          // Pour chaque question, créez une instance de Question et appelez la méthode render
          data.questions.forEach(questionData => {
              const question = new Question(questionData);
              question.render('questions-container'); // Render les questions dans le container
          });
      } else {
          console.log('Aucune question trouvée dans la réponse');
      }
  })
  .catch(error => {
      console.error('Erreur:', error); // Affiche l'erreur en cas de problème
  });
