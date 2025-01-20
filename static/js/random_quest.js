// Récupération des questions via l'API
fetch('/get_questions', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
})
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur lors de la récupération des questions');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        const questionsContainer = document.getElementById('questions-container');
        questionsContainer.innerHTML = ''; // Réinitialiser le conteneur

        // Créer des formulaires pour chaque question
        data.forEach(question => {
            const questionForm = createQuestionForm(question);
            questionsContainer.appendChild(questionForm);
        });
    })
    .catch(error => {
        console.error('Erreur lors de la récupération des questions:', error.message);
        const questionsContainer = document.getElementById('questions-container');
        questionsContainer.innerHTML = `
            <div style="color: red; font-weight: bold;">
                Une erreur est survenue lors du chargement des questions. Veuillez réessayer plus tard.
            </div>`;
    });

// Fonction pour créer un formulaire pour une question
function createQuestionForm(question) {
    const questionForm = document.createElement('form');
    questionForm.classList.add('question-form');
    questionForm.setAttribute('method', 'POST');
    questionForm.setAttribute('action', '/Vote');

    // Titre de la question
    const title = document.createElement('h2');
    title.textContent = question.title_question || 'Titre non disponible';
    questionForm.appendChild(title);

    // Ajout d'informations de confidentialité
    if (question.privacy) {
        const privacyInfo = document.createElement('p');
        privacyInfo.textContent = `Confidentialité : ${question.privacy}`;
        privacyInfo.classList.add('privacy-info');
        questionForm.appendChild(privacyInfo);
    }

    // Objet pour stocker les réponses de l'utilisateur
    const answers = {
        _id: question._id,
        question_title: question.title_question,
        choices: {}
    };

    // Prendre en compte les votes existants
    const userVote = question.user_vote || {};

    // Création des choix de la question
    if (question.choices_label && Array.isArray(question.choices_label)) {
        const choiceContainer = document.createElement('div');
        choiceContainer.classList.add('choice-container');

        question.choices_label.forEach((choiceLabel, index) => {
            const choiceWrapper = document.createElement('div');
            choiceWrapper.classList.add('choice-wrapper');

            // Label pour chaque choix
            const label = document.createElement('label');
            label.setAttribute('for', `choice_label_${question._id}_${index}`);
            label.textContent = choiceLabel;

            // Input pour chaque choix
            const input = document.createElement('input');
            input.setAttribute('id', `choice_label_${question._id}_${index}`);
            input.setAttribute('type', 'number');
            input.setAttribute('type', 'number');
            input.setAttribute('name', `choice_${choiceLabel}`);
            input.setAttribute('min', '1');
            input.setAttribute('max', question.choices_label.length.toString());
            input.value = userVote[choiceLabel] || '0'; // Pré-remplit avec le vote existant

            // Mise à jour des réponses en cas de changement
            input.addEventListener('input', () => {
                const parsedValue = parseInt(input.value, 10);
                if (!isNaN(parsedValue)) {
                    answers.choices[choiceLabel] = parsedValue;
                } else {
                    delete answers.choices[choiceLabel];
                }
            });

            choiceWrapper.appendChild(label);
            choiceWrapper.appendChild(input);
            choiceContainer.appendChild(choiceWrapper);
        });

        questionForm.appendChild(choiceContainer);
    }

    // Bouton de soumission
    const submitButton = document.createElement('button');
    submitButton.textContent = Object.keys(userVote).length > 0 ? 'Mettre à jour le vote' : 'Soumettre le vote';
    submitButton.classList.add('submit-button');
    submitButton.setAttribute('type', 'submit');
    questionForm.appendChild(submitButton);

    // Gestionnaire de soumission
    questionForm.addEventListener('submit', event => {
        event.preventDefault();

        if (!Object.keys(answers.choices).length) {
            alert('Veuillez classer au moins une option avant de soumettre votre vote.');
            return;
        }

        // Envoi du vote via Fetch API
        fetch('/Vote', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(answers)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erreur lors de la soumission du vote');
                }
                return response.json();
            })
            .then(data => {
                alert(data.message);
                console.log('Vote enregistré avec succès:', data);
            })
            .catch(error => {
                console.error('Erreur lors de la soumission du vote:', error.message);
            });
    });

    return questionForm;
}
