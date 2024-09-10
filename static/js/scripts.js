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
    icon.style.left = `${x}px`;
    icon.style.top = `${y}px`;
    canvas.appendChild(icon);

    interact(icon)
        .draggable({
            inertia: true,
            onmove: dragMoveListener
        });
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
    .then(data => alert(data.status))
    .catch(error => console.error('Error:', error));
}
