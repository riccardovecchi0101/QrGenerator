
// Waiting for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
     if (document.body.classList.contains('hub_page')) {
            console.log("DOM loaded");
            const submitButton = document.getElementById('submit-button');
            submitButton.addEventListener('click', function (event) {

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
                        'enctype': 'multipart/form-data',
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
    }

    else if (document.body.classList.contains('maker_page')) {
         const prevButton = document.getElementById('prevQr');

         prevButton.addEventListener('click', function(event){
            event.preventDefault();
            console.log("bottone cliccato");
            const preview = 'true'; // Imposta preview
            const fg_color = document.getElementById('fg_selector').value;
            const bg_color = document.getElementById('bg_selector').value;
            const fileInput = document.getElementById('imageUpload');
            const labelLogo = document.getElementById('inputTextLogo').value;
            const labelColor = document.getElementById('textColor').value;
            const file = fileInput.files[0];
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const formData = new FormData();

            formData.append('preview', true);
            formData.append('fg_color', fg_color);
            formData.append('bg_color', bg_color);
            formData.append('LabelLogo', labelLogo);
            formData.append('LabelColor', labelColor);

            if (file) {
                formData.append('image', file);
            }

            console.log("hello there");
            console.log(preview);


            fetch(qrMakerUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                }
            })
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                qrPreview.src = url;
                qrPreview.style.display = 'block'; //
             })
            .catch((error) => {
                console.error('Errore:', error);
            });
        });
    }

});


