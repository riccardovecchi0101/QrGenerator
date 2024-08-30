// Waiting for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {

    const submitButton = document.getElementById('submit-button');
    submitButton.addEventListener('click', function (event) {
        //event.preventDefault();  // Previene il comportamento di submit predefinito

        const title = document.getElementById('title1').value;
        const description = document.getElementById('description').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const data = {
            'title': title,
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
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const data = {
            'title': title,
            'description': description,
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

});