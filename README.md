# 🚀 The Lonely Trader Desk

**AI-Powered Financial Analysis Platform for Smart Trading Decisions**

A comprehensive, production-grade application that combines the power of LLM-based financial analysis with a beautiful web interface and command-line tools.

## ✨ Features

- 🌐 **Web Interface**: Beautiful, responsive web application with real-time updates
- 🤖 **AI Analysis**: Advanced LLM-powered financial analysis with quality assurance
- 📊 **Multi-Symbol Support**: Analyze multiple stocks simultaneously
- 🔄 **Iterative Refinement**: Built-in critic system ensures high-quality reports
- 📈 **Real-Time Data**: Live financial data and market sentiment analysis
- 🛡️ **Quality Control**: Automated review process with approval/feedback cycle
- 💻 **CLI Support**: Command-line interface for quick analysis

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # Optional: for enhanced news data
```

### 3. Run the Application

**Web Interface** (Recommended):
```bash
python3 start_server.py
# Open: http://localhost:8077
```

**Command Line Analysis**:
```bash
python3 start_server.py AAPL
python3 start_server.py TSLA
```

**Run Tests**:
```bash
python3 start_server.py test
```

## 🌐 Web Interface

The web interface provides:
- **Multi-symbol input**: Enter multiple stock symbols (e.g., "AAPL, GOOGL, MSFT")
- **Real-time progress**: Live updates via WebSocket
- **Individual reports**: Detailed analysis for each symbol
- **Beautiful UI**: Modern, responsive design
- **Error handling**: Graceful error management and user feedback

### API Endpoints
- `GET /` - Web interface
- `POST /api/analyze` - Start multi-symbol analysis
- `GET /api/analysis/{id}` - Get analysis results
- `WebSocket /ws/{id}` - Real-time updates
- `GET /api/health` - Health check
- `GET /docs` - API documentation

## 🏗️ Architecture

### Backend (`trader_desk/`)
- **Core**: Configuration, types, and workflow management
- **Nodes**: AI analysis components (analyst, critic)
- **Utils**: Data fetching and utility functions

### Web Application (`web_app/`)
- **Backend**: FastAPI server with WebSocket support
- **Frontend**: Modern HTML/CSS/JavaScript interface

## 📊 Analysis Flow

1. **Data Collection**: Real-time financial data + market sentiment
2. **AI Analysis**: LLM-powered financial analysis with chain-of-thought reasoning
3. **Quality Review**: Built-in critic validates analysis completeness
4. **Iterative Refinement**: Up to 3 refinement cycles if needed
5. **Final Report**: Comprehensive analysis with quality assurance approval

## 🔧 Configuration

Environment variables:
```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
TAVILY_API_KEY=your_tavily_api_key
LLM_MODEL=gpt-4-turbo
LLM_TEMPERATURE=0.0
MAX_ITERATIONS=3
VERBOSE_LOGGING=true
SAVE_RESULTS=false
```

## 📁 Project Structure

```
├── start_server.py          # Main application entry point
├── requirements.txt         # Python dependencies
├── setup.py                # Package configuration
├── trader_desk/            # Core analysis engine
│   ├── core/               # Configuration and workflow
│   ├── nodes/              # AI analysis components
│   └── utils/              # Data fetching utilities
└── web_app/                # Web application
    ├── backend/            # FastAPI server
    └── frontend/           # HTML/CSS/JavaScript
```

## 🎯 Usage Examples

### Web Interface
1. Start server: `python3 start_server.py`
2. Open: http://localhost:8077
3. Enter symbols: `AAPL, GOOGL, MSFT, TSLA`
4. Click "Start Analysis"
5. Watch real-time progress and results

### Command Line
```bash
# Single stock analysis
python3 start_server.py AAPL

# Test the system
python3 start_server.py test

# Custom port for web interface
python3 start_server.py web --port 8080
```

## 🛡️ Production Deployment

For production use:
1. Set up proper environment variables
2. Use a production WSGI server (Gunicorn)
3. Configure reverse proxy (Nginx)
4. Set up monitoring and logging
5. Use a real database instead of in-memory storage

## 🤝 Contributing

This is a private trading analysis tool. For issues or enhancements, please modify the code directly or create local documentation.

---

**Built with**: FastAPI, LangChain, OpenAI GPT-4, WebSockets, Modern JavaScript
