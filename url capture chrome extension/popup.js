document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM content loaded');
    const button = document.getElementById('unblockButton');
    console.log('Button:', button);
    
    button.addEventListener('click', () => {
        console.log('Button clicked');
        alert("button got clicked");
        fetch('http://localhost:5000/unblock_url/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status == 'success') {
                alert('URL unblocked successfully: ' + data.url);
                window.close()
            } else {
                alert('Failed to unblock URL: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while trying to unblock the URL.');
        });
    });
});
