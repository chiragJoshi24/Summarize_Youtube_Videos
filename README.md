# Summarize Youtube Videos

This Chrome extension allows users to get the summary of YouTube videos, either by pasting a link or using the URL of the currently open tab.
<p align="center">
  <img src="/assets/ui.png" />
</p>

## Setup Guide

### **1. Clone the Repository**


```
git clone https://github.com/chiragJoshi24/Summarize_Youtube_Videos
cd Summarize_Youtube_Videos
```

### **2. Setup the backend**

```
cd backend
pip install -r requirements.txt
```
### **3. Setup a Google Gemini API Key**

Go to your google console and get your api key and save it in a .env file as **GEMINI_API_KEY**

### **4. Start the backend**
Navigate to the `backend` folder within the project directory if your terminal is not already in that folder.
```
python backend.py
```

### **5. Set up the extension in browser**

Open the browser and go to 

```
chrome://extensions/
```
Turn on the developer mode and click on load unpacked.
Select the root folder of cloned repository.
Pin the extension on browser and use it.

The UI is intuitive and self-explanatory.

## Known Issues
The extension currently only supports YouTube video links.
Make sure the backend is running on localhost:5000 before using the extension.