document.getElementById('scrapeForm').onsubmit = async function (e) {
    e.preventDefault();
    const repoUrl = document.getElementById('repoUrl').value;
    const docUrl = document.getElementById('docUrl').value;
    const fileSelection = document.querySelector('input[name="fileSelection"]:checked').value;
    let selectedFileTypes = [];
    if (fileSelection === 'select') {
        document.querySelectorAll('input[name="selectedFileTypes"]:checked').forEach(checkbox => {
            selectedFileTypes.push(checkbox.value);
        });
    }

    try {
        const result = await axios.post('/scrape', {
            repoUrl: repoUrl,
            docUrl: docUrl,
            selectedFileTypes: selectedFileTypes,
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        document.getElementById('response').value = result.data.response;
    } catch (error) {
        console.error(error);
    }
};

function copyText() {
    const outputArea = document.getElementById('response');
    outputArea.select();
    document.execCommand('copy');
}

document.getElementById('allFiles').onchange = function() {
    document.getElementById('fileTypesContainer').style.display = 'none';
};

document.getElementById('selectFiles').onchange = function() {
    document.getElementById('fileTypesContainer').style.display = 'block';
};

function addFileType() {
    const customFileType = document.getElementById('customFileType').value;
    if (customFileType) {
        const container = document.getElementById('fileTypesContainer');
        const div = document.createElement('div');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'selectedFileTypes';
        checkbox.value = customFileType;
        div.appendChild(checkbox);
        div.append(customFileType);
        container.appendChild(div);
        document.getElementById('customFileType').value = ''; // Clear the input after adding
    }
}
