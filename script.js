document.getElementById('textGenerationForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const prompt = document.getElementById('promptInput').value;
    const generatedTextDiv = document.getElementById('generatedText');

    // Clear previous generated text
    generatedTextDiv.innerHTML = "Generating...";

    try {
        // Send the prompt to your backend (e.g., a Flask server) to generate text
        const response = await fetch('http://localhost:5000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });

        if (response.ok) {
            const data = await response.json();
            generatedTextDiv.innerHTML = data.generated_text;
        } else {
            const errorData = await response.json();
            generatedTextDiv.innerHTML = `Error: ${errorData.error || "Error generating text."}`;
        }
    } catch (error) {
        generatedTextDiv.innerHTML = `Error: ${error.message || "An error occurred."}`;
    }
});
