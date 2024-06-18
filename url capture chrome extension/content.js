console.log("Content script loaded");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("Message received in content script", request);
    if (request.message === 'valid') {
        showCustomAlert('The URL is malicious hence it will be blocked');
    }  if (request.message === 'exists') {
        showCustomAlert('The URL already exists. Click the button below to unblock it.');
        showUnblockButton();
    }
});

function showCustomAlert(message) {
    console.log("Showing custom alert with message:", message);
    const alertDiv = document.createElement('div');
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '50%';
    alertDiv.style.left = '50%';
    alertDiv.style.transform = 'translate(-50%, -50%)';
    alertDiv.style.padding = '20px';
    alertDiv.style.backgroundColor = 'red';
    alertDiv.style.color = 'white';
    alertDiv.style.zIndex = 10000;
    alertDiv.style.borderRadius = '5px';
    alertDiv.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
    alertDiv.innerText = message;
    alertDiv.style.fontSize = '24px';
    alertDiv.style.fontWeight = 'bold';
    alertDiv.style.textAlign = 'center';

    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showUnblockButton() {
    console.log("Showing unblock button");
    const buttonDiv = document.createElement('div');
    buttonDiv.style.position = 'fixed';
    buttonDiv.style.top = '60%';
    buttonDiv.style.left = '50%';
    buttonDiv.style.transform = 'translate(-50%, -50%)';
    buttonDiv.style.zIndex = 10000;
    
    const unblockButton = document.createElement('button');
    unblockButton.innerText = 'Unblock URL';
    unblockButton.style.padding = '10px 20px';
    unblockButton.style.fontSize = '18px';
    unblockButton.style.cursor = 'pointer';
    unblockButton.style.backgroundColor = 'blue';
    unblockButton.style.color = 'white';
    unblockButton.style.border = 'none';
    unblockButton.style.borderRadius = '5px';
    unblockButton.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
    
    unblockButton.onclick = function() {
        alert('URL unblocked!'); // Replace this with the actual logic to unblock the URL
        buttonDiv.remove();
    };

    buttonDiv.appendChild(unblockButton);
    document.body.appendChild(buttonDiv);
}
