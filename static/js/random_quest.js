fetch('/get_questions', {
    method: 'GET', // méthode de requête
})
  .then(response => {
      if (!response.ok) {
          throw new Error('Erreur de récupération des questions');
      }
      return response.json(); // Convertir la réponse en JSON
  })
  .then(data => {
      console.log('Données reçues:', data); // Affiche toute la réponse reçue
      const questionsContainer = document.getElementById('questions-container');
      data.questions.forEach(question => {

          const questionform = document.createElement('form');
          questionform.setAttribute('method', 'POST');
          questionform.setAttribute('action', '');


          // Créer un titre pour chaque questions du document
          const title = document.createElement('h2');
          title.textContent = question.title_question;
          questionform.appendChild(title);


          // Créer les choix sous forme de radio boutons
          question.choices.forEach((choice, index) => {

              //je créer un label pour input de la solution de vote
              const label = document.createElement('label');
              label.textContent = `Choice ${choice}`;
              label.setAttribute('for', `choice${question._id}_${index}`);

              // je crée mon attribut
              const input = document.createElement('input');

              // Une fois crée je vais définir mon attribut
              input.setAttribute('id', `choice${question._id}_${index}`);
              input.setAttribute('type', 'number');
              input.setAttribute('name', `question${question._id}`);
              input.setAttribute('value', '1');
              input.setAttribute('placeholder', 'Classer votre préférence');
              input.setAttribute('min', '1');
              input.setAttribute('max', '3');

              questionform.appendChild(label);
              questionform.appendChild(input);
          });

          //création du bouton de soumission du formulaire
          const button_post_vote = document.createElement('button');
          button_post_vote.textContent = 'Vote';
          button_post_vote.setAttribute('type', 'submit');

          //joindre le bouton de soumissions
          questionform.appendChild(button_post_vote);
          // Ajouter le conteneur de la question au conteneur principal
          questionsContainer.appendChild(questionform);
          });
  })
  .catch(error => {
      console.error('Erreur:', error); // Affiche l'erreur en cas de problème
  });
