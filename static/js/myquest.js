// Récupérer les sondages depuis l'API
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

        const container = document.getElementById('my_questions');
        container.innerHTML = ""; // Nettoyage du conteneur avant ajout

        if (data.status_code === 200 && Array.isArray(data.Sondage)) {
            const sondages = data.Sondage;

            if (sondages.length === 0) {
                container.textContent = "Aucun sondage disponible pour l'instant.";
                return;
            }

            sondages.forEach(question => {
                const sondageDiv = createSondageDiv(question);
                container.appendChild(sondageDiv);
            });
        } else {
            container.textContent = "Aucun sondage trouvé ou une erreur s'est produite.";
        }
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des sondages:", error);
        const container = document.getElementById('my_questions');
        container.innerHTML = `
            <div style="color: red; font-weight: bold;">
                Une erreur s'est produite lors du chargement des sondages. Veuillez réessayer plus tard.
            </div>
        `;
    });

// Fonction pour créer une div de sondage
function createSondageDiv(question) {
    const sondageDiv = document.createElement('div');
    sondageDiv.classList.add('sondage_item');
    sondageDiv.classList.add('form_container');

    const titleSection = createTitleSection(question);
    const choiceSection = createChoiceSection(question);
    const btnSection = createButtonSection(question);

    sondageDiv.appendChild(titleSection);
    sondageDiv.appendChild(choiceSection);
    sondageDiv.appendChild(btnSection);

    return sondageDiv;
}

// Fonction pour créer la section du titre
function createTitleSection(question) {
    const titleSection = document.createElement('div');
    titleSection.classList.add('title_quest');
    titleSection.classList.add('input_container');

    const headingTitle = document.createElement('h3');
    headingTitle.textContent = `Titre : ${question.title_question}`;
    // headingTitle.style.fontWeight = 'bold';

    const titleInput = document.createElement('input');
    titleInput.setAttribute('type', 'text');
    titleInput.value = question.title_question;
    titleInput.placeholder = 'Modifier le titre';

    titleInput.addEventListener('input', () => {
        question.title_question = titleInput.value; // Met à jour le titre en temps réel
    });

    const changeTitleButton = createButton('Changer le titre', () => {
        fetch('/update_title', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sondage_id: question._id,
                new_title: question.title_question
            })
        })
            .then(response => response.json())
            .then(data => {
                alert("Le titre a été mis à jour avec succès.");
            })
            .catch(error => {
                alert("Erreur lors de la mise à jour du titre:", error);
            });
    });
    changeTitleButton.classList.add('button')

    titleSection.appendChild(headingTitle);
    titleSection.appendChild(titleInput);
    titleSection.appendChild(changeTitleButton);

    return titleSection;
}

// Fonction pour créer la section des choix
function createChoiceSection(question) {
    const choiceSection = document.createElement('div');
    choiceSection.classList.add('choice_quest');

    question.choices.forEach((choice, index) => {
        const choiceWrapper = document.createElement('div')
        choiceWrapper.classList.add('input_container');
        choiceWrapper.classList.add('input_wide');
        const label = document.createElement('label');
        label.textContent = `Option ${index + 1}:`;

        const input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.value = choice;
        input.placeholder = 'Modifier ce choix';
        input.style.marginLeft = '10px';

        input.addEventListener('input', () => {
            question.choices[index] = input.value; // Mise à jour en temps réel
        });

        choiceWrapper.appendChild(label);
        choiceWrapper.appendChild(input);
        choiceWrapper.appendChild(document.createElement('br'))
        choiceSection.appendChild(choiceWrapper);
    });

    return choiceSection;
}

// Fonction pour créer la section des boutons d'action
function createButtonSection(question) {
    const btnSection = document.createElement('div');
    btnSection.classList.add('btn_action');

    // Bouton pour changer l'état de confidentialité
    const togglePrivacyButton = createButton(
        question.privacy === 'public' ? 'Passer en privé' : 'Passer en public',
        () => {
            const newPrivacy = question.privacy === 'public' ? 'private' : 'public';
            question.privacy = newPrivacy;
            togglePrivacyButton.textContent = newPrivacy === 'public' ? 'Passer en privé' : 'Passer en public';

            fetch('/Change_state_btn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sondage_id: question._id,
                    question_title: question.title_question,
                    choices: question.choices,
                    privacy: newPrivacy
                })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(`Confidentialité mise à jour : ${newPrivacy}`);
                })
                .catch(error => {
                    console.error("Erreur lors de l'envoi des données au serveur :", error);
                });
        }
    );

    // Bouton pour modifier les choix
    const changeChoicesButton = createButton('Changer les choix', '', () => {
        fetch('/update_choices', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sondage_id: question._id,
                new_choices: question.choices
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Les choix ont été mis à jour avec succès.");
            })
            .catch(error => {
                console.error("Erreur lors de la mise à jour des choix:", error);
            });
    });

    // Bouton pour supprimer un sondage
    const deleteButton = createButton('Supprimer ce sondage', '', () => {
        fetch('/Delete_btn', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question_title: question.title_question,
                choices: question.choices,
                privacy: question.privacy
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Sondage supprimé avec succès:", data);
            })
            .catch(error => {
                console.error("Erreur lors de la suppression du sondage:", error);
            });
    });

    // Bouton pour bloquer les votes
    const blockButton = createButton('Bloquer les votes', '', () => {
        fetch('/B_btn', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question_title: question.title_question,
                choices: question.choices,
                privacy: question.privacy,
                status_sondage: 'Block'
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Sondage bloqué avec succès:", data);
            })
            .catch(error => {
                console.error("Erreur lors du blocage des votes:", error);
            });
    });

    // Ajouter tous les boutons à la section
    btnSection.appendChild(togglePrivacyButton);
    btnSection.appendChild(changeChoicesButton);
    btnSection.appendChild(deleteButton);
    btnSection.appendChild(blockButton);

    return btnSection;
}

// Fonction générique pour créer un bouton
function createButton(text, marginTop, onClick) {
    const button = document.createElement('button');
    button.classList.add('button');
    button.textContent = text;
    button.style.marginTop = marginTop;
    button.setAttribute('type', 'button');
    button.addEventListener('click', onClick);
    return button;
}
