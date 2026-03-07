# Liver Care Chatbot

A FastAPI-based AI-powered chatbot application designed to provide liver care information and support. The application features a modern Arabic-language interface and integrates with OpenRouter's API for intelligent responses.

## Features

- **AI-Powered Chat**: Conversational AI using Google's Gemini model via OpenRouter
- **Session Management**: Create, manage, and persist chat sessions
- **Arabic Interface**: RTL-supported UI with Arabic text
- **Real-time Responses**: FastAPI backend with WebSocket support for real-time chat
- **Emergency Detection**: Built-in emergency response handling
- **Responsive Design**: Modern, accessible web interface

## Requirements

- Python 3.8+
- OpenRouter API key (for AI responses)

## Installation

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)
- OpenRouter API key (sign up at [openrouter.ai](https://openrouter.ai))

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Liver-Care-App-v2
   ```

2. **Verify Python version**:
   ```bash
   python --version
   ```
   Ensure it's Python 3.8 or higher.

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Configure environment variables**:
   - Copy the environment template:
     ```bash
     cp .env_example .env
     ```
   - Edit `.env` and add your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=your_actual_api_key_here
     ```
   - Optionally adjust other settings like `APP_HOST`, `APP_PORT`, etc.

7. **Verify installation** (optional):
   ```bash
   python -c "import fastapi, uvicorn, openai; print('All dependencies installed successfully')"
   ```

## Usage

1. **Start the server**:
   ```bash
   python main.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Open your browser** and navigate to `http://localhost:8000`

3. **Start chatting**: The interface will load the Arabic liver care chatbot

## API Endpoints

### Chat
- `POST /api/chat` - Send a message and receive AI response
  - Body: `{"message": "string", "session_id": "optional", "model": "optional"}`

### Sessions
- `POST /api/sessions` - Create a new session
- `GET /api/sessions` - List all active sessions
- `GET /api/sessions/{session_id}` - Get session details
- `DELETE /api/sessions/{session_id}` - Delete a session

## Configuration

The application uses Pydantic settings for configuration. Key settings include:

- `APP_TITLE`: Application title
- `APP_VERSION`: Version number
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `DEFAULT_MODEL`: Default AI model (google/gemini-2.5-flash-lite)
- `MAX_TOKENS`: Maximum response tokens
- `TEMPERATURE`: AI response creativity
- `MAX_HISTORY_TURNS`: Maximum conversation history length

## Project Structure

```
Liver-Care-App-v2/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── assets/
│   │   └── index.html      # Frontend interface
│   ├── config/
│   │   ├── settings.py     # Application settings
│   │   └── prompts.py      # AI prompts
│   ├── controllers/        # Business logic controllers
│   ├── helpers/            # Utility functions
│   ├── models/             # Data models
│   ├── routes/             # API route definitions
│   ├── schemas/            # Pydantic schemas
│   └── services/           # External service integrations
└── README.md
```

## Development

### Running in Development Mode
Use `--reload` flag with uvicorn for auto-restart on code changes:
```bash
uvicorn main:app --reload
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `OPENROUTER_API_KEY` is set in your `.env` file
2. **Port Already in Use**: Change the port in settings or kill the process using it
3. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
4. **Frontend Not Loading**: Check that `src/assets/index.html` exists and is accessible

### Logs
Check the console output for detailed error messages and debugging information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For support or questions, please open an issue in the repository.