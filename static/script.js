document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const refactorBtn = document.getElementById('refactor-btn');
    const modelSelect = document.getElementById('model-select');
    const apiKeyInput = document.getElementById('api-key-input');
    const modelNameInput = document.getElementById('model-name-input');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const dropZonePrompt = dropZone.querySelector('.drop-zone__prompt');
    const historySidebar = document.getElementById('history-sidebar');
    const historyToggleBtn = document.getElementById('history-toggle-btn');
    const closeHistoryBtn = document.getElementById('close-history-btn');

    let selectedFile = null;

    // History Toggle Logic
    historyToggleBtn.addEventListener('click', () => {
        historySidebar.classList.add('open');
    });

    closeHistoryBtn.addEventListener('click', () => {
        historySidebar.classList.remove('open');
    });

    // Close sidebar when clicking outside
    document.addEventListener('click', (e) => {
        if (!historySidebar.contains(e.target) &&
            !historyToggleBtn.contains(e.target) &&
            historySidebar.classList.contains('open')) {
            historySidebar.classList.remove('open');
        }
    });

    // Load history on startup
    loadHistory();

    async function loadHistory() {
        try {
            const response = await fetch('/history');
            const history = await response.json();
            const historyList = document.getElementById('history-list');
            historyList.innerHTML = '';

            history.forEach(item => {
                const div = document.createElement('div');
                div.className = 'history-item';
                div.innerHTML = `
                    <div class="history-timestamp">${item.timestamp}</div>
                    <div class="history-filename">${item.filename}</div>
                    <div class="history-meta">${item.provider} / ${item.model_name || 'default'}</div>
                `;
                div.addEventListener('click', () => loadHistoryItem(item.id));
                historyList.appendChild(div);
            });
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    async function loadHistoryItem(id) {
        try {
            const response = await fetch(`/history/${id}`);
            const data = await response.json();

            document.getElementById('test-data-content').textContent = data.test_data;
            document.getElementById('test-page-content').textContent = data.test_page;
            document.getElementById('test-script-content').textContent = data.test_script;

            Prism.highlightAll();
            resultsDiv.classList.remove('hidden');
        } catch (error) {
            console.error('Error loading history item:', error);
        }
    }

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            updateThumbnail(dropZone, e.target.files[0]);
            selectedFile = e.target.files[0];
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    ['dragleave', 'dragend'].forEach(type => {
        dropZone.addEventListener(type, () => {
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');

        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            updateThumbnail(dropZone, e.dataTransfer.files[0]);
            selectedFile = e.dataTransfer.files[0];
        }
    });

    function updateThumbnail(dropZoneElement, file) {
        dropZonePrompt.textContent = file.name;
    }

    refactorBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            alert('Please select a file first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('model', modelSelect.value);
        formData.append('api_key', apiKeyInput.value);
        formData.append('model_name', modelNameInput.value);
        formData.append('system_prompt', document.getElementById('system-prompt-input').value);
        formData.append('language', document.getElementById('language-select').value);

        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');

        try {
            const response = await fetch('/refactor', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            document.getElementById('test-data-content').textContent = data.test_data;
            document.getElementById('test-page-content').textContent = data.test_page;
            document.getElementById('test-script-content').textContent = data.test_script;

            // Trigger Prism syntax highlighting
            Prism.highlightAll();

            resultsDiv.classList.remove('hidden');
            loadHistory(); // Refresh history
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the file.');
        } finally {
            loadingDiv.classList.add('hidden');
        }
    });
});

function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text).then(() => {
        // Optional: Show a tooltip or temporary change in icon to indicate success
        console.log('Copied to clipboard');
    }, (err) => {
        console.error('Could not copy text: ', err);
    });
}

function downloadContent(elementId, filename) {
    const text = document.getElementById(elementId).textContent;
    if (!text) return;

    const blob = new Blob([text], { type: 'text/javascript' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
