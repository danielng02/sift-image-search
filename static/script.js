function load() {
    const path1 = document.getElementById("path1").value;
    const path2 = document.getElementById("path2").value;

    const messageLabel = document.getElementById("message");
    messageLabel.innerText = "";

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
    const messageLabel = document.getElementById("loadMessage");
    messageLabel.innerText = message;
}

function checkQueryParameters(kNN, range) {
    let messageLabel = document.getElementById("kNNparameterMessage");

    if(document.getElementById("kEnabled").checked)
    {
        if(kNN === "" || isNaN(Number(kNN))) {
            messageLabel.innerText = "Invalid value in kNN query parameter";
            return false;
        }
        messageLabel.innerText = "";
        return true;
    }

    messageLabel.innerText = "";

    if(document.getElementById("rangeEnabled").checked)
    {
        messageLabel = document.getElementById("rangeParameterMessage");
        if(range === "" || isNaN(Number(range))) {
            messageLabel.innerText = "Invalid value in range query parameter";
            return false;
        }
        messageLabel.innerText = "";
        return true;
    }

    messageLabel.innerText = "";
    return true;
}

function visualise() {
    const kNN = document.getElementById("kNN").value;
    const range = document.getElementById("range").value;

    if(!checkQueryParameters(kNN, range)) {
        return;
    }

    const rangeEnabled = document.getElementById("rangeEnabled").checked;

    const url = new URL('/visualise', window.location.origin);
    url.searchParams.append('kNN', kNN);
    url.searchParams.append('range', range);
    url.searchParams.append('rangeEnabled', rangeEnabled);

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(() => {
        window.location.href = url;
    })
    .catch(error => console.error('Error:', error));
}
