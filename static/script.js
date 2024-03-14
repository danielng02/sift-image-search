function load() {
    const path1 = document.getElementById("path1").value;
    const path2 = document.getElementById("path2").value;
    const kNN = document.getElementById("kNN").value;
    const range = document.getElementById("range").value;


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
    const range = document.getElementById("range").value;
    const k = document.getElementById("kNN").value;

    // Make AJAX request to Flask backend
    fetch('/visualise', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            range: range,
            k: k,
        })
    })
    .then(response => response.json())
    .then(data => displayResults(data.matches))
    .catch(error => console.error('Error:', error));
}

function displayResults(matches) {
    // Get the div where the results will be displayed
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; // Clear previous results

    // Create a table
    const table = document.createElement("table");

    // Create table header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");

    ["Score", "Image 1", "Image 2", "Same"].forEach(headerText => {
        const th = document.createElement("th");
        th.textContent = headerText;
        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    const tbody = document.createElement("tbody");

    matches.forEach(match => {
        const row = document.createElement("tr");

        [match.score, match.image1.name, match.image2.name, match.same].forEach(text => {
            const td = document.createElement("td");
            td.textContent = text;
            row.appendChild(td);
        });

        tbody.appendChild(row);
    });

    table.appendChild(tbody);

    // Append the table to the results div
    resultsDiv.appendChild(table);
}
