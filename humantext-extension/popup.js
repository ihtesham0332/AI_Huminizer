document.addEventListener('DOMContentLoaded', () => {
  const humanizeBtn = document.getElementById('humanizeBtn');
  const copyBtn = document.getElementById('copyBtn');
  const inputText = document.getElementById('inputText');
  const outputText = document.getElementById('outputText');
  const strengthSelect = document.getElementById('strengthSelect');
  const loader = document.getElementById('loader');

  // Attempt to grab selected text from the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.scripting.executeScript(
      {
        target: { tabId: tabs[0].id },
        func: () => window.getSelection().toString()
      },
      (results) => {
        if (results && results[0] && results[0].result) {
          inputText.value = results[0].result;
        }
      }
    );
  });

  // Polling function for LangGraph Job
  const pollJobStatus = async (jobId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/jobs/${jobId}`);
      const data = await response.json();
      
      if (data.status === 'completed') {
        loader.classList.add('hidden');
        humanizeBtn.disabled = false;
        
        // Just take the first candidate for the extension UI to keep it simple
        const bestOutput = data.result.candidates ? data.result.candidates[0] : data.result.final_output;
        outputText.value = bestOutput;
      } else if (data.status === 'failed') {
        loader.classList.add('hidden');
        humanizeBtn.disabled = false;
        outputText.value = "Error: Humanization failed on backend.";
      } else {
        // Still processing
        setTimeout(() => pollJobStatus(jobId), 2000);
      }
    } catch (err) {
      console.error(err);
      loader.classList.add('hidden');
      humanizeBtn.disabled = false;
      outputText.value = "Error: Could not reach backend server.";
    }
  };

  humanizeBtn.addEventListener('click', async () => {
    const text = inputText.value.trim();
    if (!text) return;

    humanizeBtn.disabled = true;
    loader.classList.remove('hidden');
    outputText.value = '';

    try {
      const response = await fetch('http://localhost:8000/api/v1/humanize/advanced', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          strength: strengthSelect.value
        })
      });
      
      const data = await response.json();
      if (data.job_id) {
        pollJobStatus(data.job_id);
      } else {
        throw new Error("No Job ID returned");
      }
    } catch (err) {
      console.error(err);
      loader.classList.add('hidden');
      humanizeBtn.disabled = false;
      outputText.value = "Error: Backend server at localhost:8000 is not running.";
    }
  });

  copyBtn.addEventListener('click', () => {
    if (outputText.value) {
      navigator.clipboard.writeText(outputText.value);
      const originalText = copyBtn.innerText;
      copyBtn.innerText = "Copied!";
      setTimeout(() => {
        copyBtn.innerText = originalText;
      }, 2000);
    }
  });
});
