// Waiting for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {

    const submitButton = document.getElementById('submit-button');
    submitButton.addEventListener('click', function (event) {
        //event.preventDefault();  // Previene il comportamento di submit predefinito

        const title = document.getElementById('title1').value;
        const description = document.getElementById('description').value;
        const link = document.getElementById('site_link').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const data = {
            'title': title,
            'link': link,
            'description': description
        };

        fetch(projectCreatorUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Progetto inserito', data);
            alert("Progetto inserito correttamente");
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });


    const editButton = document.getElementById('editbtn');
    project_id = this.getAttribute('data-id');
    editButton.addEventListener('click', function (event) {
        //event.preventDefault();  // Previene il comportamento di submit predefinito

        const title = document.getElementById('edit-title').value;
        const description = document.getElementById('edit-description').value;
        const link = document.getElementById('edit-link').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const data = {
            'title': title,
            'description': description,
            'link': link,
            'project_id': project_id
        };

        fetch(projectCreatorUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Progetto modificato', data);
            alert("Progetto modificato correttamente");
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    const qrMakerButton = document.getElementById('submitQR');
    qrMakerButton.addEventListener('click', function (event) {
        //event.preventDefault();  // Previene il comportamento di submit predefinito

        const fg_color = document.getElementById('fg-selector').value;
        const bg_color = document.getElementById('bg-selector').value;
        const fileInput = document.getElementById('imageUpload');
        const file = fileInput.files[0]; // Ottieni il primo file selezionato
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const formData = new FormData();
        if (file) {
            formData.append('image', file); // Aggiungi il file al FormData
        }
        formData.append('fg_color', fg_color); // Aggiungi il titolo
        formData.append('bg_color', bg_color); // Aggiungi la descrizione

        // Invia una richiesta POST con fetch
        fetch(qrMakerUrl, { // Sostituisci con l'URL del tuo endpoint
            method: 'POST',
            body: formData,
            headers: {
            'X-CSRFToken': csrfToken,
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Progetto modificato', data);
            alert("Progetto modificato correttamente");
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

});