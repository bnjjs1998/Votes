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
    console.log('Données reçues:', data);  // Vérifiez les données
    if (data && Array.isArray(data.questions)) {  // Vérification explicite que questions est un tableau
        console.log('Questions:', data.questions);
        const questionsContainer = document.getElementById('questions-container');

        data.questions.forEach(question => {
            const questionForm = document.createElement('form');
            questionForm.setAttribute('method', 'POST');
            questionForm.setAttribute('action', '/Post_vote');

            const title = document.createElement('h2');
            title.textContent = question['Title Question'];  // Accédez à "Title Question"
            questionForm.appendChild(title);

            // Dictionnaire pour stocker les réponses
            const answers = {
                _id: question._id,
                title_question: question['Title Question'],  // Assurez-vous que le titre est correctement récupéré
                choices: {},
                has_voted: true
            };

            // Vérifiez si 'choices' existe avant de le parcourir
            if (Array.isArray(question.Choix)) {
                question.Choix.forEach((choice, index) => {
                    const label = document.createElement('label');
                    label.setAttribute('for', `choice${question._id}_${index}`);
                    label.textContent = `Option ${choice} :`;

                    const input = document.createElement('input');
                    input.setAttribute('id', `choice${question._id}_${index}`);
                    input.setAttribute('type', 'number');
                    input.setAttribute('name', `question${question._id}`);
                    input.setAttribute('placeholder', 'Classer votre préférence');
                    input.setAttribute('min', '1');
                    input.setAttribute('max', '3');
                    input.value = '0';

                    input.addEventListener('change', function () {
                        answers.choices[choice] = parseInt(input.value, 10);  // Enregistre chaque choix avec son score
                    });

                    questionForm.appendChild(label);
                    questionForm.appendChild(input);
                });
            }

            const buttonPostVote = document.createElement('button');
            buttonPostVote.textContent = 'Vote';
            buttonPostVote.setAttribute('type', 'submit');
            questionForm.appendChild(buttonPostVote);

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
                    console.log('Réponse du serveur:', data);
                })
                .catch(error => {
                    console.error('Erreur lors de l\'envoi des données:', error);
                });
            });

            questionsContainer.appendChild(questionForm);
        });
    } else {
        console.error('Les questions ne sont pas disponibles ou la clé "questions" est incorrecte');
    }
})
.catch(error => {
    console.error('Erreur de récupération des questions:', error);
});
