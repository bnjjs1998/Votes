fetch('/get_sondage_current_id', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Données reçues:", data);

        const container = document.getElementById('my_quest');
        container.innerHTML = ""; // Nettoyage du conteneur avant ajout

        const sondages = data.Sondage;

        if (sondages.length === 0) {
            container.textContent = "Aucun sondage disponible pour l'instant.";
            return;
        }

        sondages.forEach((question) => {
            const sondageDiv = document.createElement('div');
            sondageDiv.classList.add('sondage_item');
            sondageDiv.style.marginBottom = '20px';
            // Section titre
            const titleSection = document.createElement('div');
            titleSection.classList.add('title_quest');
            titleSection.style.marginBottom = '15px';

            const titleHeading = document.createElement('h1');
            titleHeading.textContent = question.title_question;
            titleHeading.style.marginBottom = '10px';

            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.value = question.title_question;
            titleInput.style.marginRight = '10px';
            titleInput.style.width = '300px';

            const updateTitleButton = document.createElement('button');
            updateTitleButton.textContent = 'Mettre à jour le titre';
            updateTitleButton.style.marginLeft = '10px';

            updateTitleButton.addEventListener('click', () => {
                const newTitle = titleInput.value.trim();

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
                    .then(response => {
                        if (!response.ok) {
                            return response.json().then(data => {
                                throw new Error(data.error || `HTTP error! Status: ${response.status}`);
                            });
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.success) {
                            // Mise à jour de l'interface avec le nouveau titre
                            question.title_question = newTitle;
                            titleHeading.textContent = newTitle;
                            console.log("Titre mis à jour avec succès :", data.message);
                        } else {
                            console.log(data.error || "Erreur lors de la mise à jour du titre !");
                        }
                    })
                    .catch(error => {
                        console.error("Erreur :", error.message);
                    });


            });


            titleSection.appendChild(titleHeading);
            titleSection.appendChild(titleInput);
            titleSection.appendChild(updateTitleButton);
            sondageDiv.appendChild(titleSection);

            // Génération des choix
            const choicesContainer = document.createElement('div');
            choicesContainer.classList.add('choices_container');

            const choiceInputs = []; // Stocker les champs de saisie des choix

            if (question.choices && question.choices.length > 0) {
                question.choices.forEach((choice, index) => {
                    const choiceContainer = document.createElement('div');
                    choiceContainer.style.marginBottom = '15px';

                    const choiceLabel = document.createElement('label');
                    choiceLabel.textContent = `Modifier le choix ${index + 1}:`;
                    choiceLabel.style.display = 'block';
                    choiceLabel.style.fontWeight = 'bold';
                    choiceLabel.style.marginBottom = '5px';

                    const choiceInput = document.createElement('input');
                    choiceInput.type = 'text';
                    choiceInput.value = choice;
                    choiceInput.style.marginRight = '10px';
                    choiceInput.style.width = '300px';

                    choiceInputs.push({ input: choiceInput, oldValue: choice });

                    choiceContainer.appendChild(choiceLabel);
                    choiceContainer.appendChild(choiceInput);
                    choicesContainer.appendChild(choiceContainer);
                });
            } else {
                const noChoicesMessage = document.createElement('div');
                noChoicesMessage.textContent = "Aucun choix disponible pour cette question.";
                noChoicesMessage.style.color = 'gray';
                choicesContainer.appendChild(noChoicesMessage);
            }

            sondageDiv.appendChild(choicesContainer);

           // Bouton pour valider tous les choix
            const updateAllChoicesButton = document.createElement('button');
            updateAllChoicesButton.textContent = 'Mettre à jour tous les choix';
            updateAllChoicesButton.style.marginTop = '10px';

            updateAllChoicesButton.addEventListener('click', () => {
                const updatedChoices = [];
                const errors = [];
                const seenChoices = new Set(); // Pour détecter les doublons

                choiceInputs.forEach(({ input, oldValue }) => {
                    const newChoice = input.value;
                    if (newChoice === "") {
                        errors.push("Les choix ne peuvent pas être vides !");
                    } else if (seenChoices.has(newChoice)) {
                        errors.push(`Le choix "${newChoice}" est en double !`);
                    } else {
                        updatedChoices.push({ oldValue, newValue: newChoice });
                        seenChoices.add(newChoice);
                    }
                });

                // Affichage des erreurs si présentes
                if (errors.length > 0) {
                    console.error("Erreurs détectées :", errors);
                    alert(errors.join("\n")); // Affiche les erreurs à l'utilisateur
                    return; // Stoppe la soumission
                }

                // Log des choix mis à jour
                console.log("Mise à jour des choix :", updatedChoices);

                // Requête au backend
                fetch('/update_choices', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        Titre : question.title_question,
                        choices :updatedChoices
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log("Tous les choix mis à jour avec succès :", data);
                    })
                    .catch(error => {
                        console.error("Erreur lors de la mise à jour des choix :", error);
                        alert("Une erreur s'est produite lors de la mise à jour des choix.");
                    });
            });


            sondageDiv.appendChild(updateAllChoicesButton);

            // Bouton pour supprimer la question
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Supprimer la question';
            deleteButton.style.marginTop = '10px';
            deleteButton.addEventListener('click', () => {
                    fetch('/delete', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            Titre: question.title_question,
                        })
                    })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(`HTTP error! Status: ${response.status}`);
                            }
                            return response.json();
                        })
                        .then(data => {
                            console.log("Question supprimée avec succès :", data);
                        })
                        .catch(error => {
                            console.error("Erreur lors de la suppression de la question :", error);
                            alert("Une erreur s'est produite lors de la suppression de la question.");
                        });
            });

            sondageDiv.appendChild(deleteButton);

            // Bouton pour bloquer les votes
            const blockVotesButton = document.createElement('button');
            blockVotesButton.textContent = 'Bloquer les votes';
            blockVotesButton.style.marginLeft = '10px';

            blockVotesButton.addEventListener('click', () => {
                fetch('/block', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        Titre: question.title_question,
                        Choices: question.choices
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log("Votes bloqués avec succès :", data);
                    })
                    .catch(error => {
                        console.error("Erreur lors du blocage des votes :", error);
                        alert("Une erreur s'est produite lors du blocage des votes.");
                    });
            });

            sondageDiv.appendChild(blockVotesButton);

            // Bouton pour basculer entre public/privé
            const toggleVisibilityButton = document.createElement('button');
            toggleVisibilityButton.textContent = question.is_public ? 'Rendre Privé' : 'Rendre Public';
            toggleVisibilityButton.style.marginLeft = '10px';

            let state = question.is_public;

            toggleVisibilityButton.addEventListener('click', () => {
                toggleVisibilityButton.textContent = state ? 'Rendre Public' : 'Rendre Privé';
                state = state === 'Public' ? 'Privé' : 'Public';
                fetch('/Change_state_btn', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        Titre: question.title_question,
                        state : state
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log("Visibilité mise à jour avec succès :", data);
                    })
                    .catch(error => {
                        console.error("Erreur lors de la mise à jour de la visibilité :", error)
                    });
            });

            sondageDiv.appendChild(toggleVisibilityButton);
            container.appendChild(sondageDiv);
        });
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des sondages:", error);
    });
