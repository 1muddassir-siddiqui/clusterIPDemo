// Backend service URL - will be replaced by ClusterIP service name in K8s
const BACKEND_SERVICE = 'http://backend-service:8080';

async function countCharacters() {
    const nameInput = document.getElementById('nameInput');
    const resultDiv = document.getElementById('result');
    const name = nameInput.value.trim();

    if (!name) {
        resultDiv.innerHTML = '<p style="color: red;">Please enter a name first!</p>';
        return;
    }

    // Show loading state
    resultDiv.innerHTML = '<p>Calculating... (calling backend via ClusterIP)</p>';

    try {
        const response = await fetch(`${BACKEND_SERVICE}/count`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name })
        });

        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }

        const data = await response.json();
        
        // Display the result from backend
        resultDiv.innerHTML = `
            <p><strong>Hello ${data.name}!</strong></p>
            <p>Your name has <strong style="color: #007bff; font-size: 24px;">${data.length}</strong> characters.</p>
            <p><small>This calculation was done by the backend service via ClusterIP</small></p>
        `;

    } catch (error) {
        console.error('Error calling backend:', error);
        resultDiv.innerHTML = `
            <p style="color: red;">Error connecting to backend service: ${error.message}</p>
            <p><small>Make sure the backend pods are running and the ClusterIP service is configured correctly.</small></p>
        `;
    }
}

// Allow pressing Enter to submit
document.getElementById('nameInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        countCharacters();
    }
});
