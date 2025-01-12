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
        //je parcours cheques questions 
        data.questions.forEach(question => {
            
            
           //Pour chaque question, je génère un formulaire
            const questionForm = document.createElement('form');
            questionForm.setAttribute('method', 'POST');
            questionForm.setAttribute('action', '/Post_vote');
            
            // le formulaire commence par un h2 qui prend comme contenant la clef title_question génèré dans ma database
            const title = document.createElement('h2');
            title.textContent = question.title_question;
            questionForm.appendChild(title);

            // Dans cette variable, je vais insérer l'ensemble des contenants de chaques réponses
            const answers = {};

            // Pareil ici, je parcours les choix possibles dans chaques questions de ma database
            question.choices.forEach((choice, index) => {

                // Je génère un label pour chaque input crée
                const label = document.createElement('label');
                label.textContent = `Choix ${choice} : `;
                label.setAttribute('for', `choice${question.id}_${index}`);

                // Je génère l'input
                const input = document.createElement('input');
                input.setAttribute('id', `choice${question.id}_${index}`);
                input.setAttribute('type', 'number');
                input.setAttribute('name', `question${question.id}`);
                input.setAttribute('placeholder', 'Classer votre préférence');
                input.setAttribute('min', '1');
                input.setAttribute('max', '3');
                // je set la value à 0
                input.value = '0';


                // Ici, c'est l'événement qui va permettre de renommer chaque clef du dictionnaire "answers" en A, B, C.
                input.addEventListener('change', function () {
                    answers[choice] = parseInt(input.value, 10);
                });

                questionForm.appendChild(label);
                questionForm.appendChild(input);


            });
            
            //Enfin, je génère le bouton vote pour transmettre les datas au serveur
            const buttonPostVote = document.createElement('button');
            buttonPostVote.textContent = 'Vote';
            buttonPostVote.setAttribute('type', 'submit');

            questionForm.appendChild(buttonPostVote);
            questionsContainer.appendChild(questionForm);


            // je crée l'évènement qui va agir sur la soumission des datas de votes au serveur
            questionForm.addEventListener('submit', function (event) {
                event.preventDefault();
                // je vérifie les datas que j'envoie.
                console.log('Réponses collectées:', answers);

                // Validation des réponses
                for (const [key, value_choice] of Object.entries(answers)) {
                    if (answers['A'] === answers['B'] || answers['A'] === answers['C'] || answers['B'] === answers['C']) {
                        alert('Les valeurs des choix ne doivent pas être identiques.');
                        return;
                    }
                }

                // Envoi des réponses au serveur
                fetch('/Post_vote', {
                    // je paramètre mon fetch
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(answers),  // Envoyer les données sous forme JSON

                })
                    .then(data => {
                        console.log('Réponse du serveur:', data);
                    })
                    .then()
                    .catch(error => {
                        console.error('Erreur lors de l\'envoi des données:', error);
                    });
            });


        });
    })
    .catch(error => {
        console.error('Erreur de récupération des questions:', error);
    });
