async function getSummary(url) {
    document.getElementById('fetching').style.display = 'block';
    try {
        const response = await fetch('http://localhost:5000/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ link: url }),
        });

        if(response.status !== 200) {
            document.getElementById('videoTitle').innerText = 'INVALID';
            document.getElementById('summary').innerText = `Error ${response.status}: ${response.statusText}. The backend was unable to fetch the data.`;
            return ;
        }
        const data = await response.json();
        console.log(data);
        document.getElementById('videoTitle').innerText = data.title.slice(0, -10);
        document.getElementById('summary').innerText = data.summary;
        
    } catch (error) {
        document.getElementById('videoTitle').innerText = 'INVALID';
        document.getElementById('summary').innerText = `An error occurred while fetching data: ${error.message}. Please check your network connection or backend service.`;
    } finally {
        document.getElementById('fetching').style.display = 'none';
        const contentDiv = document.querySelector('.content');
        contentDiv.classList.add('show');
        document.body.style.height = '550px';
    }
}

document.getElementById('submitButton').addEventListener('click', () => {
    const url = document.getElementById('url').value;
    if(!url.trim())
        return ;
    getSummary(url);    
});

document.getElementById('useCurrentTab').addEventListener('click', () => {
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
        const url = tabs[0].url;  
        getSummary(url);
    });
});