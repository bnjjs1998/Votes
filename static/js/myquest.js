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
        // Loguer tous les titres des sondages



        if (sondages.length === 0) {
            container.textContent = "Aucun sondage disponible pour l'instant.";
            return;
        }

        sondages.forEach((question) => {
            const sondageDiv = document.createElement('div');
            sondageDiv.classList.add('sondage_item');
            sondageDiv.style.marginBottom = '20px';

            // Création de la section titre
            const titleSection = document.createElement('div');
            titleSection.classList.add('title_quest');
            titleSection.style.marginBottom = '15px';

            let old_title = question.title_question;

            // Titre principal en h1
            const titleHeading = document.createElement('h1');
            titleHeading.textContent = question.title_question;
            titleHeading.style.marginBottom = '10px';

            // Champ de saisie pour modifier le titre
            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.value = question.title_question;
            titleInput.placeholder = 'Modifier le titre';
            titleInput.style.marginRight = '10px';
            titleInput.style.width = '300px';

            // Bouton pour mettre à jour le titre
            const updateTitleButton = document.createElement('button');
            updateTitleButton.textContent = 'Mettre à jour le titre';
            updateTitleButton.setAttribute('type', 'button');

           updateTitleButton.addEventListener('click', () => {
                // Récupérer le nouveau titre
                const newTitle = titleInput.value.trim();

                // Vérification si le titre est vide
                if (newTitle === "") {
                    alert("Le titre ne peut pas être vide !");
                    return;
                }

                console.log("Liste des titres des sondages :");
                let isDuplicate = false;

                sondages.forEach((sondage) => {
                    console.log(`${sondage.title_question}`);

                    if(newTitle === sondage.title_question) {
                        console.log(newTitle,"'", 'ce titre existe deja',"'");
                        isDuplicate = true;
                    }
                });


                // je vérifie l'état de isDuplicate
               if (isDuplicate === true) {
                   return;
               }


                fetch('/update_title', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                old_Titre: old_title,
                                new_Titre: newTitle,
                            })
                        })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error(`HTTP error! Status: ${response.status}`);
                                }
                                return response.json();
                            })
                            .then(data => {

                            })
                            .catch(error => {
                                console.error("Erreur lors de la mise à jour du choix :", error);
                                alert("Une erreur s'est produite lors de la mise à jour des choix.");
                            });








            });

            // Ajout des éléments de la section titre
            titleSection.appendChild(titleHeading);
            titleSection.appendChild(titleInput);
            titleSection.appendChild(updateTitleButton);
            sondageDiv.appendChild(titleSection);

            // Génération des choix
            const choicesContainer = document.createElement('div');
            choicesContainer.classList.add('choices_container');

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

                    const updateChoiceButton = document.createElement('button');
                    updateChoiceButton.textContent = 'Mettre à jour';
                    updateChoiceButton.setAttribute('type', 'button');

                    updateChoiceButton.addEventListener('click', () => {
                        const newChoice = choiceInput.value.trim();
                        if (newChoice === "") {
                            alert("Le choix ne peut pas être vide !");
                            return;
                        }

                        fetch('/update_choices', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                Titre: question.title_question,
                                old_choice: choice,
                                new_choice: newChoice
                            })
                        })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error(`HTTP error! Status: ${response.status}`);
                                }
                                return response.json();
                            })
                            .then(data => {
                                console.log("Choix mis à jour avec succès :", data);
                                question.choices[index] = newChoice;
                            })
                            .catch(error => {
                                console.error("Erreur lors de la mise à jour du choix :", error);
                                alert("Une erreur s'est produite lors de la mise à jour des choix.");
                            });
                    });

                    choiceContainer.appendChild(choiceLabel);
                    choiceContainer.appendChild(choiceInput);
                    choiceContainer.appendChild(updateChoiceButton);
                    choicesContainer.appendChild(choiceContainer);
                });
            } else {
                const noChoicesMessage = document.createElement('div');
                noChoicesMessage.textContent = "Aucun choix disponible pour cette question.";
                noChoicesMessage.style.color = 'gray';
                choicesContainer.appendChild(noChoicesMessage);
            }

            // Ajouter les choix au sondage
            sondageDiv.appendChild(choicesContainer);

            // Bouton pour supprimer la question
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Supprimer la question';
            deleteButton.style.marginTop = '10px';
            deleteButton.addEventListener('click', () => {
                if (confirm("Êtes-vous sûr de vouloir supprimer cette question ?")) {
                    fetch('/delete_question', {
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
                            sondageDiv.remove(); // Supprimer la question du DOM
                        })
                        .catch(error => {
                            console.error("Erreur lors de la suppression de la question :", error);
                            alert("Une erreur s'est produite lors de la suppression de la question.");
                        });
                }
            });

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

            // Bouton pour basculer entre public/privé
            const toggleVisibilityButton = document.createElement('button');
            toggleVisibilityButton.textContent = question.is_public ? 'Rendre Privé' : 'Rendre Public';
            toggleVisibilityButton.style.marginLeft = '10px';

            let state = question.is_public

            toggleVisibilityButton.addEventListener('click', () => {
                 if (toggleVisibilityButton.textContent === 'Rendre Public') {
                     toggleVisibilityButton.textContent = 'Rendre Privé';
                 } else {
                     toggleVisibilityButton.textContent = 'Rendre Public';
                 }
                 state = !state

                 // Loguer "Privé" ou "Public" en fonction de l'état
                console.log(state ? 'Public' : 'Privé');
            });

            // Ajouter les boutons au sondage
            sondageDiv.appendChild(deleteButton);
            sondageDiv.appendChild(blockVotesButton);
            sondageDiv.appendChild(toggleVisibilityButton);

            // Ajouter le sondage complet au conteneur
            container.appendChild(sondageDiv);
        });
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des sondages:", error);
        const container = document.getElementById('my_quest');
        container.innerHTML = `
            <div style="color: red; font-weight: bold;">
                Une erreur s'est produite lors du chargement des sondages. Veuillez réessayer plus tard.
            </div>
        `;
    });
