document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultArea = document.getElementById('resultArea');
    const confidenceBadge = document.getElementById('confidenceBadge');
    const classificationVal = document.getElementById('classificationVal');
    const explanationText = document.getElementById('explanationText');
    const traceList = document.getElementById('traceList');

    analyzeBtn.addEventListener('click', async () => {
        const text = userInput.value.trim();
        if (!text) return;

        // UI Loading State
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Analyzing...';
        resultArea.classList.add('hidden');

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Analysis failed');
            }

            const data = await response.json();
            displayResult(data);

        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze Text';
        }
    });

    function displayResult(data) {
        const result = data.result;
        const trace = data.trace;

        // Update Result Cards
        classificationVal.textContent = capitalize(result.classification);

        // Format confidence as percentage
        const confPercent = Math.round(result.confidence * 100);
        confidenceBadge.textContent = `${confPercent}% Confidence`;

        // Use text from result if available, otherwise default
        explanationText.textContent = result.text || "No explanation provided.";

        // Render Trace
        traceList.innerHTML = '';
        if (trace && trace.steps) {
            trace.steps.forEach(step => {
                const li = document.createElement('li');

                const nameSpan = document.createElement('span');
                nameSpan.className = 'trace-step-name';
                nameSpan.textContent = capitalize(step.step_name);

                const detailDiv = document.createElement('div');
                detailDiv.className = 'trace-detail';
                // Show input/output summary
                const summary = `Input: ${JSON.stringify(step.input)} \nOutput: ${JSON.stringify(step.output)}`;
                detailDiv.textContent = summary;

                li.appendChild(nameSpan);
                li.appendChild(detailDiv);
                traceList.appendChild(li);
            });
        }

        resultArea.classList.remove('hidden');
    }

    function capitalize(str) {
        if (!str) return '';
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
});
