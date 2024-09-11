document.addEventListener('DOMContentLoaded', () => {
    setupDragAndDrop();
});

function setupDragAndDrop() {
    // Make the icons draggable
    interact('.icon')
        .draggable({
            inertia: true,
            onmove: dragMoveListener,
            onend: (event) => { /* Optional: handle drag end event */ }
        });

    // Make the canvas a dropzone
    interact('#canvas').dropzone({
        accept: '.icon',
        overlap: 0.5,
        ondrop: dropOnCanvas
    });
}

function dragMoveListener(event) {
    const target = event.target;
    const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
    const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

    target.style.transform = `translate(${x}px, ${y}px)`;
    target.setAttribute('data-x', x);
    target.setAttribute('data-y', y);
}

function createComponentIcon(name, type, x, y) {
    const canvas = document.getElementById('canvas');
    const icon = document.createElement('div');
    icon.classList.add('component');
    icon.textContent = `${type}: ${name}`;
    icon.setAttribute('data-name', name);
    icon.setAttribute('data-type', type);
    icon.style.position = 'absolute';
    icon.style.left = `${x-200}px`;
    icon.style.top = `${y-200}px`;
    canvas.appendChild(icon);

    interact(icon)
        .draggable({
            inertia: true,
            onmove: dragMoveListener
        });

    // Ask the user to connect the newly added component
    promptForConnection(icon);
}

function promptForConnection(newIcon) {
    // Prompt the user for the target component name
    const targetName = prompt('Enter the name of the component you want to connect to:');

    if (targetName) {
        const sourceName = newIcon.getAttribute('data-name');

        // Send the connection request to the server
        fetch('/connect_components', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ source: sourceName, target: targetName })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'Connected') {
                    alert(`${data.source} connected to ${data.target}`);
                } else {
                    alert(`Error: ${data.message}`);
                }
            })
            .catch(error => console.error('Error:', error));
    }
}


function dropOnCanvas(event) {
    const type = event.relatedTarget.getAttribute('data-type');
    const name = prompt(`Enter name for the ${type}:`);

    if (name) {
        fetch('/add_component', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ type: type, name: name })
        })
            .then(response => response.json())
            .then(data => {
                alert(data.status);
                if (data.status.includes('added')) {
                    createComponentIcon(name, type, event.dragEvent.clientX, event.dragEvent.clientY);
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

function runSimulation() {
    fetch('/simulate', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status); // Show alert box
        if (data.status === "Simulation complete") {
            // Call reset after closing the alert
            resetSimulation();
            // Reload the page to reset everything visually
            window.location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}

function resetSimulation() {
    fetch('/reset', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
            // Clear the canvas and reset icons
            clearCanvas();
        })
        .catch(error => console.error('Error:', error));
}

function clearCanvas() {
    const canvas = document.getElementById('canvas');

    // Replace the canvas element with a new one to fully clear it
    const newCanvas = canvas.cloneNode(false); // Cloning without children resets it
    canvas.parentNode.replaceChild(newCanvas, canvas);

    // Reset other states if needed
    selectedComponent = null;
    console.log("Canvas and icons have been fully reset by replacing the canvas.");
}



// Call reset endpoint on page load to ensure a fresh start
document.addEventListener('DOMContentLoaded', () => {
    fetch('/reset', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data.status))
        .catch(error => console.error('Error:', error));
});