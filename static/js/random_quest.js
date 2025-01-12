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

            const answers = {};

            question.choices.forEach((choice, index) => {


                const label = document.createElement('label');
                label.textContent = `Choix ${choice} : `;
                label.setAttribute('for', `choice${question.id}_${index}`);

                const input = document.createElement('input');
                input.setAttribute('id', `choice${question.id}_${index}`);
                input.setAttribute('type', 'number');
                input.setAttribute('name', `question${question.id}`);
                input.setAttribute('placeholder', 'Classer votre préférence');
                input.setAttribute('min', '1');
                input.setAttribute('max', '3');
                input.value = '0';

                input.addEventListener('change', function () {
                    answers[choice] = parseInt(input.value, 10);
                });

                questionForm.appendChild(label);
                questionForm.appendChild(input);


            });

            const buttonPostVote = document.createElement('button');
            buttonPostVote.textContent = 'Vote';
            buttonPostVote.setAttribute('type', 'submit');

            questionForm.addEventListener('submit', function (event) {
                event.preventDefault();

                console.log('Réponses collectées:', answers);
                const filteredChoices = {};

                // Validation des réponses
                for (const [key, value_choice] of Object.entries(answers)) {
                    if (answers['A'] === answers['B'] || answers['A'] === answers['C'] || answers['B'] === answers['C']) {
                        alert('Les valeurs des choix ne doivent pas être identiques.');
                        return;  // Empêcher l'envoi si la validation échoue
                    }
                }

                // Envoi des réponses au serveur
                fetch('/Post_vote', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(answers),  // Envoyer les données sous forme JSON
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Réponse du serveur:', data);
                        // Ajouter d'autres actions après le succès de l'envoi des données
                    })
                    .catch(error => {
                        console.error('Erreur lors de l\'envoi des données:', error);
                    });
            });

            questionForm.appendChild(buttonPostVote);
            questionsContainer.appendChild(questionForm);
        });
    })
    .catch(error => {
        console.error('Erreur de récupération des questions:', error);
    });
