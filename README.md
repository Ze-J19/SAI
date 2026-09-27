# SAI - Smart Academic Intelligence

SAI is an AI-powered educational chatbot designed for Cameroonian students at all levels especially those preparing for national exams (BEPC, Probatoire, Baccalauréat, GCE AL/OL). It combines conversational AI with an interactive quiz system to help students study more effectively.

---

## Features

- **AI Chat Assistant** — Ask questions about any subject in the Cameroonian curriculum and get instant answers
- **PDF Import** — Import your textbooks or past exam papers and let SAI generate quiz questions from them
- **Interactive MCQ Quiz** — Answer multiple choice questions (A/B/C/D) generated from your imported documents
- **Progress Report** — View a pie chart of your quiz results (correct vs incorrect answers)

---

## Tech Stack

- **Python 3** — Core language
- **Tkinter** — Graphical user interface
- **Cohere API** — AI language model (`command-r-08-2024`)
- **pypdf** — PDF text extraction
- **matplotlib** — Progress chart visualization
- **requests** — HTTP API calls

---

## Requirements

```
pip install requests
pip install pypdf
pip install matplotlib
```

> No Rust-dependent packages required — fully compatible with ARM 32-bit Android (Pydroid 3)

---

## Setup

1. Clone the repository
```bash
git clone https://github.com/Ze-J19/SAI.git
```

2. Get a free Cohere API key at [dashboard.cohere.com](https://dashboard.cohere.com)

3. Open `sai.py` and replace the API key:
```python
API_KEY = "your_cohere_api_key_here"
```

4. Run the app:
```bash
python sai.py
```

---

## How to Use

### Chat Mode
Type your question in the input field and press **Send** or **Enter**. SAI will respond as an educational assistant specialized in the Cameroonian curriculum.

### Quiz Mode
1. Click **Import PDF** and select a textbook or past exam paper
2. SAI will analyze the document and generate 5 multiple choice questions
3. Answer each question by clicking **A**, **B**, **C**, or **D**
4. At the end, your score is displayed
5. Click **Generate Report** to view your progress chart

---

## Project Status

This is **v1.0** — a functional MVP built and tested on Android (Pydroid 3, ARM 32-bit).

Planned for future versions:
- Push notifications for daily quizzes
- Multi-session progress tracking
- Migration to a native Android app.
- Support for multiple PDF sessions

---

## Author

Built by **Mandeng Emmanuel James** — DUT Génie Informatique student at IUT de Douala annexe d'Édea, Cameroon.

---

## License

MIT License
