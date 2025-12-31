// SEND A MESSAGE TO SCRAPER.JS TO START PARSING AFTER BUTTON IS CLICKED
document.getElementById('startParse').addEventListener('click', () => {
  const statusEl = document.getElementById('status');
  statusEl.textContent = 'Initiating...';

  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {action: 'startParse'}, (response) => {
      if (response.error) {
        statusEl.textContent = response.error;
      } else if (response.status === 'loading') {
        statusEl.classList.add("loading"); // include spinner from css
        statusEl.textContent = 'Loading...';  // Spinner simulation (add CSS for actual spinner)
      }
    });
  });
});

// Listen for status updates from content script (scraper.js)
chrome.runtime.onMessage.addListener((request) => {
  if (request.action === 'updateStatus') {
    document.getElementById('status').textContent = request.text;
  }
});