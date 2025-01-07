async function getSummary(url) {
    try {
        const response = await fetch('http://localhost:5000/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ link : url }),
        });
        if (response.ok) {
            const data = await response.json();
            document.getElementById('videoTitle').innerText = data.title;
            document.getElementById('summary').innerText = data.summary;
        } else {
            console.error('Error:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

document.getElementById('submitButton').addEventListener('click', () => {
    const url = document.getElementById('url').value;
    if(!url.trim())
        return ;
    getSummary(url);    
});

document.getElementById('useCurrentTab').addEventListener('click', () => {
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        const url = tabs[0].url;   
        getSummary(url);
    });
});