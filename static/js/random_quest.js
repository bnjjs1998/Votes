fetch('/get_questions', {
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
        const questionsContainer = document.getElementById('questions-container');

        data.questions.forEach(question => {
            const questionForm = document.createElement('form');
            questionForm.setAttribute('method', 'POST');
            questionForm.setAttribute('action', '/Post_vote');

            const title = document.createElement('h2');
            title.textContent = question.title_question;
            questionForm.appendChild(title);

            // Dictionnaire pour stocker les réponses
            const answers = {
                _id: question._id,
                title_question: question.title_question,
                choices: {}  // Dictionnaire pour les choix et leurs scores
            };

            // Parcours des choix dans la question
            question.choices.forEach((choice, index) => {

                //Création des différents labels pour l'input
                const label = document.createElement('label');
                label.setAttribute('for', `choice${question._id}_${index}`);
                label.textContent = `Option ${choice} :`;


                //Création de l'input en fonction de ce quil trouve dans le document mongo
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
                    answers.choices[choice] = parseInt(input.value, 10);  // Enregistre chaque choix avec son score
                });

                questionForm.appendChild(label);
                questionForm.appendChild(input);
            });

            const buttonPostVote = document.createElement('button');
            buttonPostVote.textContent = 'Vote';
            buttonPostVote.setAttribute('type', 'submit');
            questionForm.appendChild(buttonPostVote);

            questionsContainer.appendChild(questionForm);

            // Gestion de la soumission du formulaire
            questionForm.addEventListener('submit', function (event) {
                event.preventDefault();

                console.log('Réponses collectées:', answers);
                fetch('/Post_vote', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(answers),  // Envoi du dictionnaire de réponses
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Réponse du serveur:', answers ,data);
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