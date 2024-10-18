document.getElementById('pdf-upload').addEventListener('change', async (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = async (e) => {
      const pdfData = new Uint8Array(e.target.result);
      const pdf = await pdfjsLib.getDocument({ data: pdfData }).promise;
      let text = '';
      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        text += textContent.items.map(item => item.str).join(' ');
      }
      localStorage.setItem('pdfText', text);
      console.log(text);  // Add this line to print extracted text
      alert('PDF uploaded successfully!');
    };
    reader.readAsArrayBuffer(file);
  }
});

document.getElementById('ask').addEventListener('click', async () => {
  const question = document.getElementById('question').value;
  const pdfText = localStorage.getItem('pdfText');
  const url = document.getElementById('url').value;

  const response = await fetch('/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question, pdfText, url }),
  });

  const result = await response.json();
  const chat = document.getElementById('chat');
  chat.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
  chat.innerHTML += `<p><strong>Bot:</strong> ${result.answer}</p>`;
});

const startButton = document.getElementById('start-record');
const stopButton = document.getElementById('stop-record');

if ('webkitSpeechRecognition' in window) {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = 'ml-IN'; // Malayalam language code
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    startButton.disabled = true;
    stopButton.disabled = false;
  };

  recognition.onend = () => {
    startButton.disabled = false;
    stopButton.disabled = true;
  };

  recognition.onresult = (event) => {
    const result = event.results[0][0].transcript;
    document.getElementById('question').value = result;
  };

  startButton.addEventListener('click', () => {
    recognition.start();
  });

  stopButton.addEventListener('click', () => {
    recognition.stop();
  });
} else {
  startButton.disabled = true;
  stopButton.disabled = true;
  alert('Speech recognition not supported in this browser. Please use Google Chrome.');
}
