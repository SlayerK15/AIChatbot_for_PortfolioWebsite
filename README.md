# AI Chatbot for Portfolio Website

## Description
A minimalist yet powerful AI chatbot built with Flask and Anthropic's Claude model, designed to interact with visitors on your portfolio website. The chatbot provides information about your projects, skills, and experience through an intuitive chat interface.

## Project Structure
```
AIChatbot_for_PortfolioWebsite/
├── static/
│   ├── styles.css        # CSS styling for the chatbot
│   └── index.html        # Main chatbot interface
├── app.py               # Flask application and routes
├── requirements.txt     # Python dependencies
└── .env                # Environment variables
```

## Prerequisites
- Python 3.8 or higher
- Anthropic API key
- Flask

## Local Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/SlayerK15/AIChatbot_for_PortfolioWebsite.git
cd AIChatbot_for_PortfolioWebsite
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

## Features
- 🤖 **Claude AI Integration**: Powered by Anthropic's language model
- 💬 **Interactive Chat Interface**: Modern, responsive design
- 🎯 **Portfolio Information**: Customized responses about your work
- 📱 **Responsive Design**: Works on desktop and mobile
- ⚡ **Real-time Responses**: Quick and context-aware interactions

## Running Locally

1. Ensure your virtual environment is activated:
```bash
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Start the Flask application:
```bash
python app.py
```

3. Access the chatbot at `http://localhost:5000`

4. The chatbot will be ready to answer questions about your portfolio and experience

## Configuration

### Customizing Portfolio Information
Update the portfolio information in `app.py`:
```python
PORTFOLIO_INFO = {
    "name": "Your Name",
    "role": "Your Role",
    "projects": [
        # Add your projects here
    ],
    "skills": [
        # Add your skills here
    ]
}
```

### Styling
Customize the appearance by modifying `static/styles.css`:
- Update colors
- Modify chat bubble styles
- Adjust responsive breakpoints

## API Endpoint

### POST /chat
Handles chat interactions with the AI model.

Request format:
```json
{
    "message": "User's message"
}
```

Response format:
```json
{
    "status": "success",
    "response": "AI response message"
}
```

## Dependencies
Main requirements include:
- Flask
- anthropic
- python-dotenv
- Additional dependencies listed in `requirements.txt`

## Error Handling
The application handles:
- API connection issues
- Invalid requests
- Server errors
- Rate limiting

## Security
- API key stored in environment variables
- Basic input sanitization
- Error message sanitization

## Troubleshooting Common Issues

1. **API Key Issues**
   - Verify .env file exists and is in the correct location
   - Check API key format
   - Ensure key is valid and not expired

2. **Connection Errors**
   - Check internet connection
   - Verify API status
   - Check server logs
   - Ensure you're running the latest version of the required packages

3. **Response Issues**
   - Verify message format
   - Check request payload
   - Monitor server logs
   - Ensure your Python version is compatible

4. **Local Server Issues**
   - Check if port 5000 is available
   - Verify Flask is installed correctly
   - Ensure virtual environment is activated
   - Check console for error messages

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License.

## Author
Kanav Gathe
- GitHub: [SlayerK15](https://github.com/SlayerK15)

## Acknowledgments
- Anthropic for the Claude AI model
- Flask framework
- Modern chat UI inspiration