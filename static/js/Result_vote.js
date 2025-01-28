fetch('/get_result', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Erreur HTTP : ${response.status}`);
    }
    return response.json(); // Convertir la réponse en JSON
})
.then(data => {
    console.log("Données reçues :", data);

    // Accéder aux questions dans data[0].data
    const questions = data[0]?.data;

    if (!Array.isArray(questions)) {
        console.error("Aucune donnée valide trouvée.");
        return;
    }

    // Sélectionner ou créer le conteneur dans le DOM
    let resultContainer = document.getElementById('Result_container');
    if (!resultContainer) {
        resultContainer = document.createElement('div');
        resultContainer.id = 'Result_container';
        document.body.appendChild(resultContainer);
    }

    // Vider le conteneur avant de générer le contenu
    resultContainer.innerHTML = '';

    // Utiliser un fragment pour optimiser les manipulations DOM
    const fragment = document.createDocumentFragment();

    // Parcourir et afficher les questions dans le DOM
    questions.forEach((question, index) => {
        // Créer un conteneur pour chaque question
        const questionElement = document.createElement('div');
        questionElement.className = 'question';

        // Ajouter le titre de la question
        const title = document.createElement('h3');
        title.textContent = `Question ${index + 1} : ${question.title_question}`;
        questionElement.appendChild(title);

        // Ajouter les choix
        const choicesList = document.createElement('ul');
        if (question.choices_label && Array.isArray(question.choices_label)) {
            question.choices_label.forEach(choice => {
                const choiceItem = document.createElement('li');
                choiceItem.textContent = choice;
                choicesList.appendChild(choiceItem);
            });
        }
        questionElement.appendChild(choicesList);

        // Ajouter le statut et la confidentialité
        const status = document.createElement('p');
        status.textContent = `Statut : ${question.status}`;
        questionElement.appendChild(status);

        const privacy = document.createElement('p');
        privacy.textContent = `Confidentialité : ${question.privacy}`;
        questionElement.appendChild(privacy);

        // Ajouter les scores Condorcet s'ils existent
        if (question.Condorcet_Scores) {
            const scoresContainer = document.createElement('div');
            scoresContainer.className = 'condorcet-scores';

            const scoresTitle = document.createElement('h4');
            scoresTitle.textContent = 'Scores Condorcet :';
            scoresContainer.appendChild(scoresTitle);

            const scoresList = document.createElement('ul');
            Object.entries(question.Condorcet_Scores).forEach(([key, value]) => {
                const scoreItem = document.createElement('li');
                scoreItem.textContent = `${key} : ${value}`;
                scoresList.appendChild(scoreItem);
            });

            scoresContainer.appendChild(scoresList);
            questionElement.appendChild(scoresContainer);
        }

        // Ajouter la date d'expiration si elle existe
        if (question.expiration_date) {
            const expirationDate = new Date(question.expiration_date);
            const expiration = document.createElement('p');
            expiration.textContent = `Date d'expiration : ${expirationDate.toLocaleString()}`;
            questionElement.appendChild(expiration);
        }

        // Ajouter l'état si présent
        if (question.state) {
            const state = document.createElement('p');
            state.textContent = `État : ${question.state}`;
            questionElement.appendChild(state);
        }

        // Ajouter l'élément question dans le fragment
        fragment.appendChild(questionElement);
    });

    // Ajouter tout le fragment au conteneur principal
    resultContainer.appendChild(fragment);
})
.catch(error => {
    console.error("Erreur lors de la récupération des données :", error);

    // Afficher un message d'erreur dans le DOM
    let resultContainer = document.getElementById('Result_container');
    if (!resultContainer) {
        resultContainer = document.createElement('div');
        resultContainer.id = 'Result_container';
        document.body.appendChild(resultContainer);
    }
    resultContainer.innerHTML = `<p style="color: red;">Erreur : Impossible de récupérer les données.</p>`;
});
