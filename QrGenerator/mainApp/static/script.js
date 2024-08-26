
// waiting for the dom to be fully loaded
document.addEventListener('DOMContentLoaded', function () {

    const submitButton = document.getElementById('submit-button');
    submitButton.addEventListener('click', function (event) {
       // event.preventDefault();
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const data = {
            title: title,
            description: description
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
            alert("Progetto inserito correttamente")
            // Gestisci la risposta, ad esempio mostrando un messaggio di successo
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});