// Fonction principale pour récupérer les questions depuis l'API
fetch('/get_questions', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur ${response.status}: Impossible de récupérer les questions.`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Données brutes reçues depuis l\'API:', data);

        const questionsContainer = document.getElementById('questions-container');
        questionsContainer.innerHTML = ''; // Nettoyer le conteneur avant d'ajouter les questions

        // Vérifiez que les données sont un tableau
        if (Array.isArray(data)) {
            data.forEach((question, index) => {
                console.log(`Traitement de la question ${index + 1}:`, question);

                if (!question.title_question) {
                    console.warn(`Question ${index + 1} ignorée: titre manquant.`);
                    return;
                }

                // Création du formulaire pour la question
                const questionForm = createQuestionForm(question);
                questionsContainer.appendChild(questionForm);
            });
        } else {
            console.error('Les données reçues ne sont pas un tableau.');
            showError(questionsContainer, 'Les données reçues sont invalides. Veuillez réessayer plus tard.');
        }
    })
    .catch(error => {
        console.error('Erreur lors de la récupération des questions:', error.message);
        const questionsContainer = document.getElementById('questions-container');
        showError(questionsContainer, 'Une erreur s\'est produite lors du chargement des questions. Veuillez vérifier votre connexion ou réessayer plus tard.');
    });

// Fonction pour afficher un message d'erreur dans le DOM
function showError(container, message) {
    container.innerHTML = `
        <div style="color: red; font-weight: bold; margin: 20px;">
            ${message}
        </div>
    `;
}

// Fonction pour créer un formulaire pour une question
function createQuestionForm(question) {
    const questionForm = document.createElement('form');
    questionForm.classList.add('question-form');
    questionForm.setAttribute('method', 'POST');
    questionForm.setAttribute('action', '/Post_vote');

    // Ajout du titre de la question
    const title = document.createElement('h2');
    title.textContent = question.title_question;
    questionForm.appendChild(title);

    // Initialisation des réponses
    const answers = {
        _id: question._id,
        question_title: question.title_question,
        choices: {},
        has_voted: true,
        privacy: question.privacy || 'unknown'
    };

    // Création des choix de réponse
    if (Array.isArray(question.choices)) {
        const choiceContainer = document.createElement('div');
        choiceContainer.classList.add('choice-container');

        question.choices.forEach((choice, index) => {
            const choiceWrapper = document.createElement('div');
            choiceWrapper.classList.add('choice-wrapper');

            const label = document.createElement('label');
            label.setAttribute('for', `choice${index}`);
            label.textContent = `Option ${choice}:`;

            const input = document.createElement('input');
            input.setAttribute('id', `choice${index}`);
            input.setAttribute('type', 'number');
            input.setAttribute('name', `choice_${choice}`);
            input.setAttribute('min', '1');
            input.setAttribute('max', question.choices.length.toString());
            input.setAttribute('placeholder', 'Classer votre préférence');
            input.value = '0';

            // Mise à jour des réponses en fonction de l'entrée utilisateur
            input.addEventListener('change', () => {
                const parsedValue = parseInt(input.value, 10);
                if (!isNaN(parsedValue)) {
                    answers.choices[choice] = parsedValue;
                } else {
                    delete answers.choices[choice]; // Supprime les entrées invalides
                }
            });

            choiceWrapper.appendChild(label);
            choiceWrapper.appendChild(input);
            choiceContainer.appendChild(choiceWrapper);
        });

        questionForm.appendChild(choiceContainer);
    }
// Création du bouton pour soumettre le formulaire
const submitButton = document.createElement('button');
submitButton.textContent = 'Vote'; // Texte affiché sur le bouton
submitButton.classList.add('submit-button'); // Classe pour le style
submitButton.setAttribute('type', 'submit'); // Type de soumission
questionForm.appendChild(submitButton);

// Gestionnaire d'événements pour la soumission du formulaire
questionForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Empêche le rechargement de la page par défaut

    // Affiche les réponses collectées pour débogage
    console.log('Réponses collectées:', answers);

    // Vérification de base avant l'envoi
    if (!Object.keys(answers.choices).length) {
        alert('Veuillez classer au moins une option avant de soumettre votre vote.');
        return;
    }

    // Envoi des données via fetch
    fetch('/Vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }, // Spécifie que le contenu est du JSON
        body: JSON.stringify(answers) // Convertit les réponses en JSON
    })
        .then(response => {
            // Vérifie si la réponse est OK
            if (!response.ok) {
                throw new Error(`Erreur ${response.status}: Échec de l'envoi des données.`);
            }
            return response.json(); // Convertit la réponse en JSON
        })
        .then(data => {
            // Affiche la réponse du serveur pour confirmation
            console.log('Réponse du serveur:', data);
            alert(`Votre vote pour "${answers.question_title}" a été enregistré avec succès.`);
        })
        .catch(error => {
            // Gestion des erreurs
            console.error('Erreur lors de l\'envoi des données:', error.message);
            alert('Une erreur est survenue lors de l\'envoi de votre vote. Veuillez vérifier votre connexion ou réessayer.');
        });
});


    return questionForm;
}
