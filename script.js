function extractVideoId(url) {
    const match = url.match(/(?:v=|\/)([0-9A-Za-z_-]{11})/);
    return match ? match[1] : null;
}

document.getElementById('submitButton').addEventListener('click', async () => {
    const url = document.getElementById('url').value;
    const videoId = extractVideoId(url);

    try {
        const response = await fetch('http://localhost:5000/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: videoId }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Response:', data.summary);
            document.getElementById('summary').innerText = data.summary;
        } else {
            console.error('Error:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});
