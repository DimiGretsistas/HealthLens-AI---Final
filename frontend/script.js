const API_URL = "";

let currentMode = "single";

const youtubeUrlInput = document.getElementById("youtubeUrl");
const questionInput = document.getElementById("question");
const processBtn = document.getElementById("processBtn");
const askBtn = document.getElementById("askBtn");
const micBtn = document.getElementById("micBtn");
const speakAnswerBtn = document.getElementById("speakAnswerBtn");

const singleVideoModeBtn = document.getElementById("singleVideoModeBtn");
const libraryModeBtn = document.getElementById("libraryModeBtn");
const videoInputArea = document.getElementById("videoInputArea");
const modeBadge = document.getElementById("modeBadge");

const processStatus = document.getElementById("processStatus");
const answerBox = document.getElementById("answer");
const sourcesBox = document.getElementById("sources");

singleVideoModeBtn.addEventListener("click", () => {
  currentMode = "single";

  videoInputArea.classList.remove("hidden");

  singleVideoModeBtn.className =
    "bg-[#1E3D32] text-white rounded-2xl py-4 font-bold transition shadow-lg";

  libraryModeBtn.className =
    "bg-white/80 dark:bg-black/20 border-2 border-[#c9d8d0] dark:border-white/10 rounded-2xl py-4 font-bold transition hover:border-[#5BC58C] text-[#123026] dark:text-white";

  processStatus.textContent = "Current mode: pasted video.";
  modeBadge.textContent = "Pasted video mode";
  answerBox.textContent = "No answer yet. Process a video and ask your first question.";
  sourcesBox.textContent = "No sources yet.";
});

libraryModeBtn.addEventListener("click", () => {
  currentMode = "library";

  videoInputArea.classList.add("hidden");

  libraryModeBtn.className =
    "bg-[#1E3D32] text-white rounded-2xl py-4 font-bold transition shadow-lg";

  singleVideoModeBtn.className =
    "bg-white/80 dark:bg-black/20 border-2 border-[#c9d8d0] dark:border-white/10 rounded-2xl py-4 font-bold transition hover:border-[#5BC58C] text-[#123026] dark:text-white";

  processStatus.textContent = "Current mode: preloaded video library.";
  modeBadge.textContent = "Video library mode";
  answerBox.textContent = "Ask a question from the preloaded health video library.";
  sourcesBox.textContent = "No sources yet.";
});

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

  const endpoint =
    currentMode === "library"
      ? "/ask-library"
      : "/ask";

  const response = await fetch(`${API_URL}${endpoint}`, {
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

  if (!data.response.sources || data.response.sources.length === 0) {
    sourcesBox.textContent = "No sources available.";
    return;
  }

  data.response.sources.forEach((source) => {
    const link = document.createElement("a");

    link.href = source.url;
    link.target = "_blank";

    if (source.title) {
      link.textContent = `${source.title} | ${source.time} → ${source.url}`;
    } else {
      link.textContent = `${source.time} → ${source.url}`;
    }

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