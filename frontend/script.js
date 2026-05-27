const API_URL = "";

const youtubeUrlInput = document.getElementById("youtubeUrl");
const questionInput = document.getElementById("question");
const processBtn = document.getElementById("processBtn");
const askBtn = document.getElementById("askBtn");
const micBtn = document.getElementById("micBtn");
const speakAnswerBtn = document.getElementById("speakAnswerBtn");

const processStatus = document.getElementById("processStatus");
const answerBox = document.getElementById("answer");
const sourcesBox = document.getElementById("sources");

processBtn.addEventListener("click", async () => {
  const youtubeUrl = youtubeUrlInput.value.trim();

  if (!youtubeUrl) {
    processStatus.textContent = "Please paste a YouTube URL first.";
    return;
  }

  processStatus.textContent = "Processing video...";

  const response = await fetch(`${API_URL}/process-video`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      youtube_url: youtubeUrl
    })
  });

  const data = await response.json();

  processStatus.textContent = data.message;
});

askBtn.addEventListener("click", async () => {
  const question = questionInput.value.trim();

  if (!question) {
    answerBox.textContent = "Please ask a question first.";
    return;
  }

  answerBox.textContent = "Thinking...";
  sourcesBox.textContent = "";

  const response = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      question: question
    })
  });

  const data = await response.json();

  answerBox.textContent = data.response.answer;
  sourcesBox.innerHTML = "";

  data.response.sources.forEach((source) => {
    const link = document.createElement("a");

    link.href = source.url;
    link.target = "_blank";
    link.textContent = `${source.time} → ${source.url}`;
    link.className = "block hover:underline";

    sourcesBox.appendChild(link);
  });
});

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  micBtn.disabled = true;
  micBtn.textContent = "Not Supported";
} else {
  const recognition = new SpeechRecognition();

  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.continuous = false;

  micBtn.addEventListener("click", () => {
    micBtn.textContent = "Listening...";
    micBtn.classList.add("opacity-70");
    recognition.start();
  });

  recognition.addEventListener("result", (event) => {
    const spokenText = event.results[0][0].transcript;
    questionInput.value = spokenText;
  });

  recognition.addEventListener("end", () => {
    micBtn.textContent = "🎙️ Speak";
    micBtn.classList.remove("opacity-70");
  });

  recognition.addEventListener("error", () => {
    micBtn.textContent = "🎙️ Speak";
    micBtn.classList.remove("opacity-70");
    answerBox.textContent = "Microphone error. Please try again.";
  });
}

speakAnswerBtn.addEventListener("click", () => {
  const answerText = answerBox.textContent.trim();

  if (!answerText) return;

  const utterance = new SpeechSynthesisUtterance(answerText);

  utterance.lang = "en-US";
  utterance.rate = 1;
  utterance.pitch = 1;

  speechSynthesis.cancel();
  speechSynthesis.speak(utterance);
});