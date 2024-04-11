function load() {
    const path1 = document.getElementById("path1").value;
    const path2 = document.getElementById("path2").value;

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
    const kNN = document.getElementById("kNN").value;
    const range = document.getElementById("range").value;
    const rangeEnabled = document.getElementById("rangeEnabled").checked;

    // Create the URL with parameters
    const url = new URL('/visualise', window.location.origin);
    url.searchParams.append('kNN', kNN);
    url.searchParams.append('range', range);
    url.searchParams.append('rangeEnabled', rangeEnabled);

    // Make AJAX request to Flask backend
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(() => {
        // Navigate to the /visualise page
        window.location.href = url;
    })
    .catch(error => console.error('Error:', error));
}
