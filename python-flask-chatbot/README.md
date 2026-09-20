# Smart FAQ Chatbot - Hackathon Starter

Welcome to the Smart FAQ Chatbot Hackathon! Your team will build an AI-powered chatbot using Azure OpenAI and Python Flask.

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your Azure OpenAI credentials:
```bash
cp .env.example .env
```

3. Run the app:
```bash
python app.py
```

The app will be available at http://localhost:5000

## Project Structure
```
├── app.py                 # Flask application (your main backend)
├── knowledge_base.json    # Your FAQ knowledge base
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── static/
│   ├── css/
│   │   └── style.css     # Your chatbot styles
│   └── js/
│       └── chat.js       # Frontend chat logic
└── templates/
    └── index.html        # Chat UI template
```

## Team Tasks
- **Team Member 1**: Backend API & Azure OpenAI integration
- **Team Member 2**: Knowledge base & prompt engineering
- **Team Member 3**: Frontend UI & styling

Good luck! 🚀
