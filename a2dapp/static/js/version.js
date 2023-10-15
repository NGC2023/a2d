// Fetch the version number from /version endpoint
document.addEventListener('DOMContentLoaded', () => {
    fetch('/version')
        .then(response => response.json())
        .then(data => {
            const versionElement = document.getElementById('version-placeholder');
            versionElement.textContent = `v${data.version}`;
        })
        .catch(error => console.error('Error fetching version:', error));
});
