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

        // Vérifiez si les données sont un tableau
        if (!Array.isArray(data)) {
            throw new Error('Les données reçues ne sont pas dans le format attendu.');
        }

        const questionsContainer = document.getElementById('questions-container');
        questionsContainer.innerHTML = ''; // Nettoyez le conteneur avant d'ajouter des questions

        data.forEach(question => {
            const questionForm = document.createElement('form');
            questionForm.setAttribute('method', 'POST');
            questionForm.setAttribute('action', '/Post_vote');

            const title = document.createElement('h3');
            title.textContent = question.title_question;
            questionForm.appendChild(title);

            const answers = {
                _id: question._id || null, // Assurez-vous que l'ID existe ou utilisez null
                title_question: question.title_question,
                choices: {},
            };

            (question.choices || []).forEach((choice, index) => {
                const div = document.createElement('div');
                div.classList.add('input_container');
                const label = document.createElement('label');
                label.setAttribute('for', `choice${index}`);
                label.textContent = `Option ${index + 1} : ${choice}`;

                    const input = document.createElement('input');
                    input.setAttribute('id', `choice${index}`);
                    input.setAttribute('type', 'number');
                    input.setAttribute('name', `question${index}`);
                    input.setAttribute('placeholder', 'Classer votre préférence');
                    input.setAttribute('min', '1');
                    input.setAttribute('max', '3');
                    input.value = '0';

                    // Mise à jour des réponses
                    input.addEventListener('change', () => {
                        answers.choices[choice] = parseInt(input.value, 10) || 0;
                    });

                    questionForm.appendChild(label);
                    questionForm.appendChild(input);
                    questionForm.appendChild(document.createElement('br'));
                });

                questionForm.appendChild(div);
                div.appendChild(label);
                div.appendChild(input);
            });

            const buttonPostVote = document.createElement('button');
            buttonPostVote.textContent = 'Vote';
            buttonPostVote.setAttribute('type', 'submit');
            buttonPostVote.classList.add('button');
            questionForm.appendChild(buttonPostVote);

            questionsContainer.appendChild(questionForm);

            // Gestion de la soumission
            questionForm.addEventListener('submit', function (event) {
                event.preventDefault();

                console.log('Réponses collectées:', answers);
                fetch('/Post_vote', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(answers),
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Erreur lors de l\'envoi des réponses.');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Réponse du serveur:', data);
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

document.getElementById("submit_button").addEventListener("click", async function (event) {
    event.preventDefault();    
    const formData = new FormData(document.getElementById("newFormVote")); 
    try {
        const response = await fetch("/Post_sondage", {
            method: "POST",
            body: formData,
        });
        const result = await response.json();
        if (response.ok) {
            alert(result.message); // Affiche l'alerte Windows avec le message du serveur
            // refreshQuestionsContainer(); // Actualise le  après que l'utilisateur ferme l'alerte
            location.reload();
        } else {
            alert(`Erreur : ${result.error}`);
        }
    } catch (error) {
        alert("Une erreur est survenue. Veuillez réessayer.");
    }
});

function refreshQuestionsContainer() {
    fetch("/get_questions") // Mettez l'URL pour récupérer les questions à jour
        .then(response => response.text())
        .then(html => {
            console.log("Nouveau contenu des questions :", html);
            document.getElementById("questions-container").innerHTML = html;
        })
        .catch(error => console.error("Erreur lors de la mise à jour :", error));
}
