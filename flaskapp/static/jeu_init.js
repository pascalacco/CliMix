document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("passwordInput").style.display = "none";
    document.getElementById("submitButton").addEventListener("click", function(event) {
        var motDePasseScribe = document.getElementById("passwordInput").value;
        var scenario = document.getElementById("scenarioInput").value;
        var nom = document.getElementById("nomInput").value;
        var prenom = document.getElementById("prenomInput").value;
        var genre = document.getElementById("genreInput").value;
        var role = document.getElementById("roleInput").value;
        
        // Envoi des données au serveur via AJAX
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/set_group", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response[0] === "log_in_success") {
                    afficherMessage("Les informations sur le joueur ont été enregistrées.");
                    afficherMessage("Vous pouvez saisir les informations d'un autre joueur si vous le souhaitez.");
                } else {
                    afficherMessage("Une erreur s'est produite lors de l'enregistrement des informations.");
                }
            }
        };
        var data = JSON.stringify({
            group: nom,
            team: prenom,
            action: "new"
        });
        xhr.send(data);

        // Empêcher le formulaire d'être soumis normalement
        event.preventDefault();
    });

    function afficherMessage(message) {
        var messageDiv = document.createElement("div");
        messageDiv.textContent = message;
        document.getElementById("confirmationMessage").appendChild(messageDiv);
    }
});
