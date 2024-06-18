function sendURL(url, tabId) {
    console.log('Sending URL:', url);
    fetch('http://localhost:5000/capture_url/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        console.log('Response from API:', data);
        
        if (data.existencecheck === true) {
            console.log("I AM CALLED");
            chrome.windows.create({
                url: chrome.runtime.getURL("popup.html"),
                type: "popup",
                width: 400,
                height: 300
            });
        } else {
            if (data.message === 'valid') {
                console.log('URL is valid, sending message to content script.');
                chrome.tabs.sendMessage(tabId, { message: 'valid' });

                setTimeout(() => {
                    closeTab(tabId);
                }, 8000);
            } else {
                console.log('The response does not match the expected value.');
            }
        }
    })
    .catch(error => {
        console.error('Error sending URL:', error);
    });
}

function closeTab(tabId) {
    chrome.tabs.remove(tabId, function() {
        console.log(`Tab ${tabId} closed`);
    });
}

chrome.webNavigation.onCompleted.addListener(function(details) {
    chrome.tabs.get(details.tabId, function(tab) {
        sendURL(tab.url, details.tabId);
    });
}, {url: [{urlMatches: 'http://*/*'}, {urlMatches: 'https://*/*'}]});

chrome.webRequest.onErrorOccurred.addListener(function(details) {
    if (details.error === "net::ERR_CERT_AUTHORITY_INVALID") {
        chrome.tabs.get(details.tabId, function(tab) {
            sendURL(details.url, details.tabId);
        });
    }
}, {urls: ["<all_urls>"]});

chrome.webRequest.onErrorOccurred.addListener(function(details) {
    if (details.error === "net::ERR_CONNECTION_REFUSED") {
        chrome.tabs.get(details.tabId, function(tab) {
            sendURL(details.url, details.tabId);
        });
    }
}, {urls: ["<all_urls>"]});
