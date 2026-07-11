const API_URL = '/generate';

async function generatePlan() {
    const input = document.getElementById('problemInput');
    const btn = document.getElementById('generateBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');

    const problem = input.value.trim();
    
    if (!problem) {
        alert('Please enter a problem statement');
        return;
    }

    btn.disabled = true;
    btn.textContent = 'Generating...';
    loading.classList.remove('hidden');
    results.classList.add('hidden');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ problem_statement: problem })
        });

        if (!response.ok) {
            throw new Error('Failed to generate plan');
        }

        const data = await response.json();

        document.getElementById('projectPlan').textContent = data.project_plan;
        document.getElementById('requirements').textContent = data.requirements;
        document.getElementById('architecture').textContent = data.architecture;
        document.getElementById('development').textContent = data.development;
        document.getElementById('review').textContent = data.review;
        document.getElementById('documentation').textContent = data.documentation;

        results.classList.remove('hidden');

    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Generate Plan';
        loading.classList.add('hidden');
    }
}

function toggleCard(card) {
    card.classList.toggle('active');
}

function copySection(id) {
    const text = document.getElementById(id).textContent;
    navigator.clipboard.writeText(text).then(() => {
        const btn = event.target;
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = 'Copy', 2000);
    });
}
