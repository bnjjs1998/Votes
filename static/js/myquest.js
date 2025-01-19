fetch('/get_sondage_current_id', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json(); // Assurez-vous que la réponse est bien en JSON
})
.then(data => {
    console.log("Données reçues:", data); // Affichez la réponse pour vérifier sa structure
    const container = document.getElementById('my_quest');
    container.innerHTML = ""; // Nettoyage du conteneur avant d'ajouter le contenu

    if (data.status_code === 200 && Array.isArray(data.Sondage)) {
        const sondages = data.Sondage;

        if (sondages.length === 0) {
            container.textContent = "Aucun sondage disponible pour l'instant.";
            return;
        }

        sondages.forEach(question => {
            const sondageDiv = document.createElement('div');
            sondageDiv.classList.add('sondage_item');
            const titleSection = document.createElement('div');
            titleSection.classList.add('title_quest');

            // Formulaire pour modifier le titre
            const titleForm = document.createElement('form');
            titleForm.setAttribute('method', 'POST');
            titleForm.setAttribute('action', '/update_title');  // Action pour la mise à jour du titre

            const titleDiv = document.createElement('div');
            titleDiv.classList.add('modifie_title');

            const titleParagraph = document.createElement('p');
            titleParagraph.textContent = `Titre : ${question.title_question}`;
            titleParagraph.style.fontWeight = 'bold';
            titleParagraph.style.marginBottom = '5px';
            titleForm.appendChild(titleParagraph);

            const titleInput = document.createElement('input');
            titleInput.setAttribute('type', 'text');
            titleInput.setAttribute('value', question.title_question);
            titleInput.setAttribute('placeholder', 'Modifier le titre');
            titleInput.classList.add('changeTitle');
            titleDiv.appendChild(titleInput);

            const changeTitleButton = document.createElement('button');
            changeTitleButton.textContent = 'Changer le titre';
            changeTitleButton.setAttribute('type', 'button');
            changeTitleButton.style.marginLeft = '10px';
            changeTitleButton.style.marginBottom = '10px';
            changeTitleButton.addEventListener('click', function () {
                question.title_question = titleInput.value; // Met à jour le titre
                console.log(`Titre mis à jour pour l'ID ${question._id}: ${question.title_question}`);

                // Mettre à jour le titre via un fetch
                fetch('/update_title', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        sondage_id: question._id,
                        new_title: titleInput.value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log("Le titre a été mis à jour avec succès.");
                    } else {
                        console.error("Échec de la mise à jour du titre.");
                    }
                })
                .catch(error => {
                    console.error("Erreur lors de la mise à jour du titre:", error);
                });
            });
            titleDiv.appendChild(changeTitleButton);
            titleForm.appendChild(titleDiv);
            titleSection.appendChild(titleForm);
            sondageDiv.appendChild(titleSection);

            // Partie choix
            const choiceSection = document.createElement('div');
            choiceSection.classList.add('choice_quest');

            const choiceForm = document.createElement('form');
            choiceForm.setAttribute('method', 'POST');
            choiceForm.setAttribute('action', '/update_choices'); // Action pour la mise à jour des choix

            const choiceInputs = [];

            question.choices.forEach((choice, index) => {
                const label = document.createElement('label');
                label.setAttribute('for', `choice${question._id}_${index}`);
                label.textContent = `Option ${index + 1}:`;

                const input = document.createElement('input');
                input.setAttribute('id', `choice${question._id}_${index}`);
                input.setAttribute('type', 'text');
                input.setAttribute('value', choice);
                input.setAttribute('placeholder', 'Modifier ce choix');
                input.style.marginLeft = '10px';

                choiceForm.appendChild(label);
                choiceForm.appendChild(input);
                choiceForm.appendChild(document.createElement('br'));

                choiceInputs.push(input);
            });

            choiceSection.appendChild(choiceForm);
            sondageDiv.appendChild(choiceSection);

            // Bouton de mise à jour des choix
            const btnSection = document.createElement('div');
            btnSection.classList.add('btn_action');

            const changeChoicesButton = document.createElement('button');
            changeChoicesButton.textContent = 'Changer les choix';
            changeChoicesButton.setAttribute('type', 'button');
            changeChoicesButton.addEventListener('click', function () {
                console.log('Mise à jour des choix pour le sondage ID:', question._id);

                // Met à jour les choix avec les valeurs des inputs
                question.choices = choiceInputs.map(input => input.value);
                console.log('Nouveaux choix:', question.choices);
                fetch('/update_choices', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        sondage_id: question._id,  // ID du sondage
                        new_choices: question.choices  // Liste des nouveaux choix
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.succes) {
                        console.log("Les choix ont été mis à jour avec succès.");
                        console.log("Nouveaux choix:", data.updated_choices);
                    } else {
                        console.error("Échec de la mise à jour des choix.");
                    }
                })
                .catch(error => {
                    console.error("Erreur lors de la mise à jour des choix:", error);
                });

            });

            btnSection.appendChild(changeChoicesButton);

            // Bouton de suppression
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Supprimer ce sondage';
            deleteButton.setAttribute('type', 'button');
            deleteButton.addEventListener('click', function () {
                fetch('/Delete_btn', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        sondage_id: question._id,
                        question_title: question.title_question,
                        choices: question.choices
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log("hello");
                })
                .catch(error => {
                    console.error("Erreur lors de la requête de suppression:", error);
                });
            });


            btnSection.appendChild(deleteButton);           // Bouton de suppression

            // Bouton pour blocker les votes et procédé au résultat
            const BlockButton = document.createElement('button');
            BlockButton.textContent = 'Block Vote';
            BlockButton.setAttribute('type', 'button');

            const answer = {
                "Status_Sondage":"Block"
            }

            BlockButton.addEventListener('click', function () {

                //en gros, je vais envoyer un jeu de donnée

                fetch('/Block_btn', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        sondage_id: question._id,
                        question_title: question.title_question,
                        choices: question.choices
                    })
                })
                .then(response => response.json())
                .then(data => {
                })
                .catch(error => {
                    console.error("Erreur lors de la requête de suppression:", error);
                });
            });
            btnSection.appendChild(BlockButton);

            // Bouton pour basculer entre Privé et Public
            const togglePrivacyButton = document.createElement('button');
            togglePrivacyButton.textContent = question.isPrivate ? 'Passer en public' : 'Passer en privé'; // Texte initial basé sur l'état
            togglePrivacyButton.setAttribute('type', 'button');


            // Écouteur d'événement pour basculer l'état
            togglePrivacyButton.addEventListener('click', function () {
                // Basculer l'état localement
                question.isPrivate = !question.isPrivate;

                // Mettre à jour le texte du bouton en fonction du nouvel état
                togglePrivacyButton.textContent = question.isPrivate ? 'Passer en public' : 'Passer en privé';

                // Envoyer la mise à jour de l'état au serveur
                fetch('/Change_state_btn', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        sondage_id: question._id,
                        question_title: question.title_question,
                        choices: question.choices
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log(`L'état du sondage a été mis à jour : ${question.isPrivate ? 'Privé' : 'Public'}`);
                    } else {
                        console.error('Échec de la mise à jour de l’état du sondage.');
                    }
                })
                .catch(error => {
                    console.error("Erreur lors de la mise à jour de l'état de confidentialité :", error);
                });
            });

            // Ajouter le bouton à la section des boutons
            btnSection.appendChild(togglePrivacyButton);



            sondageDiv.appendChild(btnSection);

            container.appendChild(sondageDiv);
        });
    } else {
        container.textContent = "Aucun sondage trouvé ou une erreur s'est produite.";
    }
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
