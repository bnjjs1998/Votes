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
        return response.json();
    })
    .then(data => {
        const container = document.getElementById('my_quest');
        container.innerHTML = ""; // Nettoyage du conteneur avant d'ajouter le contenu

        if (data.status_code === 200 && Array.isArray(data.Sondage)) {
            const sondages = data.Sondage;

            if (sondages.length === 0) {
                container.textContent = "Aucun sondage disponible pour l'instant.";
                return;
            }

            sondages.forEach(question => {
                // Créer une div pour chaque sondage
                const sondageDiv = document.createElement('div');
                sondageDiv.classList.add('sondage_item');

                // Créer la section pour le titre
                const titleSection = document.createElement('div');
                titleSection.classList.add('title_quest');

                // Créer un formulaire pour le titre
                const titleForm = document.createElement('form');
                titleForm.setAttribute('method', 'POST');
                titleForm.setAttribute('action', '#'); // Remplacer par l'URL d'action si nécessaire

                // Paragraphe pour le titre de la question
                const titleParagraph = document.createElement('p');
                titleParagraph.textContent = `Titre : ${question.title_question}`;
                titleParagraph.style.fontWeight = 'bold'; // Mise en valeur du titre
                titleParagraph.style.marginBottom = '5px';
                titleForm.appendChild(titleParagraph);

                // Input pour modifier le titre
                const titleInput = document.createElement('input');
                titleInput.setAttribute('type', 'text');
                titleInput.setAttribute('value', question.title_question);
                titleInput.setAttribute('placeholder', 'Modifier le titre');
                titleInput.classList.add('changeTitle');
                titleForm.appendChild(titleInput);

                // Bouton pour changer le titre
                const changeTitleButton = document.createElement('button');
                changeTitleButton.textContent = 'Changer le titre';
                changeTitleButton.setAttribute('type', 'button');
                changeTitleButton.style.marginBottom = '10px';
                changeTitleButton.addEventListener('click', function () {
                    question.title_question = titleInput.value; // Met à jour le titre
                    console.log(`Titre mis à jour pour l'ID ${question._id}: ${question.title_question}`);
                });
                titleForm.appendChild(changeTitleButton);

                // Ajouter le formulaire du titre dans la section du titre
                titleSection.appendChild(titleForm);

                // Ajouter la section du titre dans la div principale
                sondageDiv.appendChild(titleSection);

                // Créer la section pour les choix
                const choiceSection = document.createElement('div');
                choiceSection.classList.add('choice_quest');

                // Formulaire pour les choix
                const choiceForm = document.createElement('form');
                choiceForm.setAttribute('method', 'POST');
                choiceForm.setAttribute('action', '#'); // Remplacer par l'URL d'action si nécessaire

                // Array pour stocker les inputs des choix
                const choiceInputs = [];

                // Parcourir les choix
                question.choices.forEach((choice, index) => {
                    // Label pour chaque choix
                    const label = document.createElement('label');
                    label.setAttribute('for', `choice${question._id}_${index}`);
                    label.textContent = `Option ${index + 1}:`;

                    // Input pour modifier chaque choix
                    const input = document.createElement('input');
                    input.setAttribute('id', `choice${question._id}_${index}`);
                    input.setAttribute('type', 'text');
                    input.setAttribute('value', choice);
                    input.setAttribute('placeholder', 'Modifier ce choix');
                    input.style.marginLeft = '10px';

                    // Ajouter le label et l'input au formulaire des choix
                    choiceForm.appendChild(label);
                    choiceForm.appendChild(input);
                    choiceForm.appendChild(document.createElement('br'));

                    // Ajouter l'input à la liste pour un futur changement collectif
                    choiceInputs.push(input);
                });

                // Ajouter le formulaire des choix dans la section des choix
                choiceSection.appendChild(choiceForm);

                // Ajouter la section des choix dans la div principale
                sondageDiv.appendChild(choiceSection);

                // Créer la section des boutons (Changer les choix, Public/Privé, Delete, Block)
                const btnSection = document.createElement('div');
                btnSection.classList.add('btn_action');  // Classe ajoutée ici

                // Bouton "Changer les choix" - Ajouté en premier
                const changeChoicesButton = document.createElement('button');
                changeChoicesButton.textContent = 'Changer les choix';
                changeChoicesButton.setAttribute('type', 'button');
                changeChoicesButton.addEventListener('click', function () {
                    console.log('Mise à jour des choix pour le sondage ID:', question._id);
                    question.choices = choiceInputs.map(input => input.value); // Met à jour les choix avec les valeurs des inputs
                    console.log('Nouveaux choix:', question.choices);
                });
                btnSection.appendChild(changeChoicesButton);

                // Bouton Public/Privé
                const visibilityButton = document.createElement('button');
                visibilityButton.textContent = "Public";
                visibilityButton.setAttribute('type', 'button');
                visibilityButton.style.marginRight = '10px';
                visibilityButton.style.backgroundColor = 'green';
                visibilityButton.addEventListener('click', function () {
                    if (question.visibility === "Public") {
                        question.visibility = "Privé";
                        visibilityButton.textContent = "Privé";
                        visibilityButton.style.backgroundColor = "red";
                    } else {
                        question.visibility = "Public";
                        visibilityButton.textContent = "Public";
                        visibilityButton.style.backgroundColor = "green";
                    }
                    console.log(`Visibilité changée: ${question.visibility}`);
                });
                btnSection.appendChild(visibilityButton);

                // Bouton Delete
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.setAttribute('type', 'button');
                deleteButton.style.marginRight = '10px';
                deleteButton.addEventListener('click', function () {
                    console.log(`Vous avez supprimé le sondage avec l'ID: ${question._id}`);
                    sondageDiv.remove(); // Supprimer le sondage de l'interface
                });
                btnSection.appendChild(deleteButton);

                // Bouton Block
                const blockButton = document.createElement('button');
                blockButton.textContent = 'Block';
                blockButton.setAttribute('type', 'button');
                blockButton.style.marginRight = '10px';
                blockButton.addEventListener('click', function () {
                    console.log(`Vous avez bloqué le sondage avec l'ID: ${question._id}`);
                });
                btnSection.appendChild(blockButton);

                // Ajouter la section des boutons dans la div principale
                sondageDiv.appendChild(btnSection);

                // Ajouter la div principale au conteneur
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
