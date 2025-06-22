
> **Customize any song your way — isolate stems, fine-tune effects, and create your own unique sound.**

Sound Box is a web application that lets users upload or paste a link to a song, split it into stems (vocals, drums, bass, etc.), tweak audio effects like reverb (float input) and other integer-based controls like pitch, gain, and speed, then download a clean, customized track. Whether you're a casual listener or an aspiring producer, Sound Editor gives you full control over how you experience your music.

---

## Features

- **Stem Separation** — Use advanced algorithms to isolate vocals, drums, piano, guitar, and more.
- **Custom Sound Effects** — Adjust reverb, pitch shift, gain, distortion, speed, and lowpass filters.
- **YouTube Link or MP3 Upload** — Upload local files or enter a YouTube link for processing.
- **Loading & Processing UI** — Beautiful feedback with animated loaders and transitions.
- **Downloadable Output** — Final audio file ready to play or download in seconds.

---

## Tech Stack

| Frontend     | Backend          |
| ------------ | ---------------- |
| Vue 3 + Vite | FastAPI (Python) |
| Tailwind CSS | Pedalboard       |
| VeeValidate  | LALAL.AI API     |
| Lucide Icons | Uvicorn Server   |

---

## Screenshots
![image](https://github.com/user-attachments/assets/1a51a6b6-dfb7-4c52-89ce-46c8b2b37484)
![image](https://github.com/user-attachments/assets/94d3ff44-1c88-4e53-965e-0b65eab61c98)
![image](https://github.com/user-attachments/assets/0e09f063-3af7-46ff-9b24-31b6e7f2f51b)
![image](https://github.com/user-attachments/assets/4d3f48bc-92a4-4cb3-bf50-31f6d90009e5)
![image](https://github.com/user-attachments/assets/1153ebfa-fc40-4131-a1a7-002ba5a49489)


## Inspiration

We love music, and we’ve always wanted a tool that made it easy to manipulate a song's individual parts — without needing a full DAW (Digital Audio Workstation). Inspired by lofi remixes and AI-powered stem separation tools, we decided to create a fun, beautiful, and accessible audio editor for everyone.

---

## How We Built It

1. **Frontend**: Built with Vue 3 and styled with Tailwind CSS for clean, modern visuals.
2. **Stem Splitting**: Used LALAL.AI’s API to handle professional-grade stem separation.
3. **Audio Effects**: Applied Pedalboard (by Spotify) to customize sound with pitch, reverb, gain, and more.
4. **Routing & State**: Vue Router manages page transitions and UX flow.
5. **Validation**: VeeValidate ensures correct input on sound effect forms.
6. **Audio Output**: Final audio is processed, served by FastAPI, and made downloadable via the frontend.

---

## Challenges We Faced

- Setting up cross-origin communication between frontend and backend on different systems (Mac vs. Windows).
- Managing real-time feedback while processing heavy audio tasks.
- Validating user inputs while keeping the UI intuitive.
- Making sure LALAL.AI API handled both uploads and YouTube inputs correctly.

---

## Accomplishments

- Fully working multi-step app with audio processing and final output.
- Designed a sleek UI from scratch with animated transitions and effects.
- Seamlessly integrated AI stem splitting and DSP effects into one flow.

---

## What We Learned

- How to connect a Vue frontend to a Python backend smoothly.
- Working with audio libraries and real-time media processing.
- Designing for both technical correctness and user experience.
- Handling async logic and loading states cleanly in the UI.

---

## What's Next

- Deploy the app so anyone can try it out!
- Possibly explore AI-powered suggestions for auto-effect presets
---

## Getting Started (Dev Setup)

```bash
# Clone the repo
git clone https://github.com/your-username/sound-editor.git
cd sound-editor

# Frontend setup
cd frontend
npm install
npm run dev

# Backend setup (Python 3.10+ recommended)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📄 License

MIT License © 2025 Sound Box
