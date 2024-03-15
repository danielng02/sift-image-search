function load() {
    const path1 = document.getElementById("path1").value;
    const path2 = document.getElementById("path2").value;
    const kNN = document.getElementById("kNN").value;
    const range = document.getElementById("range").value;

    const messageLabel = document.getElementById("message");
    messageLabel.innerText = "";

    // Make AJAX request to Flask backend
    fetch('/load', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            path1: path1,
            path2: path2,
            kNN: kNN,
            range: range
        })
    })
    .then(response => response.json())
    .then(data => loadResult(data.message))
    .catch(error => console.error('Error:', error));
}

function loadResult(message) {
    const messageLabel = document.getElementById("message");
    messageLabel.innerText = message;
}
function visualise() {

    // Make AJAX request to Flask backend
    fetch('/visualise', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(() => {
        // Navigate to the /visualise page
        window.location.href = '/visualise';
    })
    .catch(error => console.error('Error:', error));
}
