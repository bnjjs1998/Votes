fetch('/get_questions')
  .then(response => response.json())
  .then(data => {
      console.log(data);  // Affiche la réponse complète pour inspecter sa structure

      // Vérifie si 'data.questions' est bien défini
      if (data && data.questions) {
          const container = document.getElementById('questions-container');
          container.innerHTML = ''; // Efface tout contenu précédent

          // Parcours des questions et affichage des titres
          data.questions.forEach(question => {
              console.log(question);  // Affiche chaque question pour vérifier sa structure
              const h1 = document.createElement('h1');
              h1.textContent = question.title_question;
              container.appendChild(h1);
          });
      } else {
          console.error('La réponse ne contient pas "questions".');
      }
  })
  .catch(error => console.error('Erreur de récupération des questions:', error));
