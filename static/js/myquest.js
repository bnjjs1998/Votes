fetch('/get_sondage_current_id', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
})
    .then(response => {
        if (!response.ok) {
            console.log("Erreur lors de la récupération de l'ID du sondage actuel !");
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Données reçues:", data);
        const usernameButton = document.querySelector('form[action="/profile"] button');
        usernameButton.textContent = data.username;

        const container = document.getElementById('my_questions');
        container.innerHTML = ""; // Nettoyage du conteneur avant ajout

        const sondages = data.Sondage;

        if (sondages.length === 0) {
            container.textContent = "Aucun sondage disponible. Ajoutez-en un depuis votre dashboard !";
            return;
        }
        sondages.forEach((question, index) => {
            const sondageDiv = document.createElement('div');
            sondageDiv.classList.add('sondage_item', 'form_container');

            // Section titre
            const titleSection = document.createElement('div');
            titleSection.classList.add('title_quest', 'input_container');

            const titleHeading = document.createElement('h3');
            titleHeading.textContent = `${index + 1}. ${question.title_question}`;

            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.value = question.title_question;
            titleInput.style.width = '100%'

            const updateTitleButton = createButton('updateTitle', 'Mettre à jour le titre', question, { titleInput, titleHeading });
            titleSection.append(titleHeading, titleInput, updateTitleButton);
            sondageDiv.appendChild(titleSection);

            // Génération des choix
            const choicesContainer = document.createElement('div');
            choicesContainer.classList.add('choices_container');
            const choicesInput = [];

            if (question.choices && question.choices.length > 0) {
                question.choices.forEach((choice, i) => {
                    const choiceDiv = document.createElement('div');
                    choiceDiv.classList.add('input_container', 'input_wide');

                    const choiceLabel = document.createElement('label');
                    choiceLabel.textContent = `Choix ${i + 1}:`;

                    const choiceInput = document.createElement('input');
                    choiceInput.type = 'text';
                    choiceInput.value = choice;

                    choicesInput.push({ input: choiceInput, oldValue: choice });
                    choiceDiv.append(choiceLabel, choiceInput);
                    choicesContainer.appendChild(choiceDiv);
                });
            } else {
                const noChoicesMessage = document.createElement('div');
                noChoicesMessage.textContent = "Aucun choix disponible.";
                noChoicesMessage.style.color = 'gray';
                choicesContainer.appendChild(noChoicesMessage);
            }

            sondageDiv.appendChild(choicesContainer);
            
            // Boutons d'actions
            const updateChoicesButton = createButton('updateChoices', 'Mettre à jour les choix', question, { choicesInput });
            const deleteButton = createButton('deleteQuestion', 'Supprimer la question', question);
            const toggleVisibilityButton = createButton('toggleVisibility', question.is_public ? 'Rendre Privé' : 'Rendre Public', question);

            sondageDiv.append(updateChoicesButton ,deleteButton, toggleVisibilityButton);
            container.appendChild(sondageDiv);
        });
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des sondages:", error);
    });

    const createButton = (type, textContent, question, inputs) => {
        const btn = document.createElement('button');
        btn.classList.add('button');
        btn.textContent = textContent;
    
        switch (type) {
            case 'updateTitle':
                btn.addEventListener('click', () => {
                    const newTitle = inputs.titleInput.value.trim();
                    if (newTitle === "") {
                        alert("Le titre ne peut pas être vide !");
                        return;
                    }
                    fetch('/update_title', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            old_Titre: question.title_question,
                            new_Titre: newTitle
                        })
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                question.title_question = newTitle;
                                inputs.titleHeading.textContent = newTitle;
                                console.log("Titre mis à jour avec succès :", data.message);
                            } else {
                                console.error(data.error || "Erreur lors de la mise à jour du titre !");
                            }
                        })
                        .catch(error => console.error("Erreur :", error.message));
                });
                break;
    
            case 'updateChoices':
                btn.addEventListener('click', () => {
                    const updatedChoices = [];
                    const errors = [];
                    const seenChoices = new Set();
    
                    inputs.choicesInput.forEach(({ input, oldValue }) => {
                        const newChoice = input.value.trim();
                        if (newChoice === "") {
                            errors.push("Les choix ne peuvent pas être vides !");
                        } else if (seenChoices.has(newChoice)) {
                            errors.push(`Le choix "${newChoice}" est en double !`);
                        } else {
                            updatedChoices.push({ oldValue, newValue: newChoice });
                            seenChoices.add(newChoice);
                        }
                    });
    
                    if (errors.length > 0) {
                        alert(errors.join("\n"));
                        return;
                    }
    
                    fetch('/update_choices', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            Titre: question.title_question,
                            choices: updatedChoices
                        })
                    })
                        .then(response => response.json())
                        .then(data => console.log("Choix mis à jour :", data))
                        .catch(error => {
                            console.error("Erreur lors de la mise à jour des choix :", error);
                            alert("Une erreur s'est produite.");
                        });
                });
                break;
    
            case 'toggleVisibility':
                btn.addEventListener('click', () => {
                    console.log("Privacy state before:", question.is_public);
                    question.is_public = !question.is_public;
                    btn.textContent = question.is_public ? 'Rendre Privé' : 'Rendre Public';
    
                    fetch('/Change_state_btn', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            Titre: question.title_question,
                            state: question.is_public ? 'Public' : 'Privé'
                        })
                    })
                        .then(response => response.json())
                        .then(data => console.log("Visibilité mise à jour :", data))
                        .catch(error => console.error("Erreur :", error));
                });
                break;
    
            case 'deleteQuestion':
                btn.addEventListener('click', () => {
                    fetch('/delete', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ Titre: question.title_question })
                    })
                        .then(response => response.json())
                        .then(data => console.log("Question supprimée :", data))
                        .catch(error => console.error("Erreur :", error));
                });
                break;
    
            default:
                console.error("Type de bouton non reconnu :", type);
                alert("Type de bouton non reconnu !", type);
        }
    
        return btn;
    };
    