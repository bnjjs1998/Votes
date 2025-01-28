fetch('/get_last_questions', {
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
        questionsContainer.innerHTML = '';

        data.forEach(question => {
            const questionForm = document.createElement('form');
            questionForm.setAttribute('method', 'POST');
            questionForm.setAttribute('action', '/Post_vote');
            questionForm.classList.add('formVote');

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
            buttonPostVote.setAttribute('type', 'submit');
            buttonPostVote.classList.add('button');
            questionForm.appendChild(buttonPostVote);

            questionsContainer.appendChild(questionForm);

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
            location.reload();
        } else {
            alert(`Erreur : ${result.error}`);
        }
    } catch (error) {
        alert("Une erreur est survenue. Veuillez réessayer.");
    }
});

function refreshQuestionsContainer() {
    fetch("/get_last_questions") // Mettez l'URL pour récupérer les questions à jour
        .then(response => response.text())
        .then(html => {
            console.log("Nouveau contenu des questions :", html);
            document.getElementById("questions-container").innerHTML = html;
        })
        .catch(error => console.error("Erreur lors de la mise à jour :", error));
}
