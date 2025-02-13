from flask import Flask, request, jsonify
from flask_cors import CORS
from anthropic import Anthropic
import os
import re

app = Flask(__name__)
CORS(app)

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def create_system_message():
    return """You are a helpful assistant for Kanav Gathe's portfolio website. Your role is to provide specific, concise information about his work, experience, and contact methods.

    Key guidelines:
    1. NEVER give generic responses like "I'm ready to help" or "What would you like to know"
    2. ALWAYS give specific information from his portfolio
    3. Keep responses short and focused (2-3 sentences max)
    4. For greetings, respond naturally but quickly transition to portfolio information
    5. For vague questions, highlight his most impressive projects
    6. Use bullet points sparingly and only for listing multiple projects
    7. For contact questions, mention both the EmailJS form and direct contact methods

    Tone guidelines:
    - Be professional but conversational
    - Focus on technical details and accomplishments
    - Avoid overly casual language
    - Stay factual and specific
    """

def handle_greeting(message):
    # Expanded greetings patterns
    basic_greetings = ['hi', 'hello', 'hey', 'greetings']
    time_greetings = ['good morning', 'good afternoon', 'good evening']
    how_are_you = ['how are you', 'how r u', 'how you', 'how r you', 'how are u']
    
    message = message.lower().strip()
    
    # Handle "how are you" type messages
    if any(greeting in message for greeting in how_are_you):
        return True, "I'm doing great, thanks for asking! Would you like to connect with Kanav or need help exploring his projects?"
    
    # Handle basic greetings
    if any(message == greeting for greeting in basic_greetings):
        return True, "Hello! Would you like to connect with Kanav or need help exploring his projects?"
    
    # Handle time-based greetings
    if any(greeting in message for greeting in time_greetings):
        return True, f"{message.title()}! Would you like to connect with Kanav or need help exploring his projects?"
    
    return False, None

def handle_contact_query(message):
    contact_keywords = ['contact', 'email', 'reach', 'message', 'form', 'send', 'talk', 'connect']
    if any(keyword in message.lower() for keyword in contact_keywords):
        return True, "You can use the contact form above which sends messages directly via EmailJS, or email gathekanav@gmail.com. For quick responses, call +91 8999816954."
    return False, None

def handle_project_query(message):
    project_keywords = ['project', 'work', 'portfolio', 'build', 'made', 'created', 'developed']
    if any(keyword in message.lower() for keyword in project_keywords):
        return True, "Kanav has built six impressive projects including an AI-powered laptop recommendation system and a containerized compiler infrastructure on AWS ECS. Which project would you like to know more about?"
    return False, None

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'status': 'success',
                'response': "Would you like to connect with Kanav or need help exploring his projects?"
            })

        # Check for greetings first
        is_greeting, greeting_response = handle_greeting(user_message)
        if is_greeting:
            return jsonify({
                'status': 'success',
                'response': greeting_response
            })

        # Check for contact queries
        is_contact, contact_response = handle_contact_query(user_message)
        if is_contact:
            return jsonify({
                'status': 'success',
                'response': contact_response
            })

        # Check for project queries
        is_project, project_response = handle_project_query(user_message)
        if is_project:
            return jsonify({
                'status': 'success',
                'response': project_response
            })

        # Create focused context about portfolio
        context = f"""{create_system_message()}

        Portfolio Information:
        - Role: DevOps Engineer
        - Expertise: AWS cloud, CI/CD pipelines, infrastructure automation
        - Technical Skills: AWS (EC2, ECS, S3), Docker, Kubernetes, Terraform, Jenkins, Linux
        
        Contact Information:
        - Email: gathekanav@gmail.com
        - Phone: +91 8999816954
        - Contact Form: Uses EmailJS for direct message delivery
        
        Projects:
        1. Laptop Recommendation System
           - Web crawler and data parser
           - AI-powered React frontend
           - Deployed on AWS
        
        2. Online Compiler Infrastructure
           - Deployed on AWS ECS
           - Automated GitHub Actions pipeline
           - Secure VPC configuration
        
        3. Quotes Application (EC2)
           - 50,000+ quotes database
           - Docker containerized
           - MongoDB integration
        
        4. DevOps Tools Installation Suite
           - Automated setup scripts
           - Support for Docker, Jenkins, Kubernetes
           - Dependency management
        
        5. Task Manager
           - Flask and MongoDB
           - Grafana monitoring
           - Jenkins pipeline integration
        
        6. S3 Website Hosting
           - Static site deployment
           - GitHub Actions CI/CD
           - AWS S3 configuration

        User question: {user_message}

        Remember: 
        1. Answer in 2-3 sentences maximum
        2. Be specific about Kanav's work
        3. Focus on technical details
        4. Include contact info if asked"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=150,
            temperature=0.7,
            messages=[{
                "role": "user", 
                "content": context
            }]
        )
        
        response = message.content[0].text.strip()

        # Clean up response
        response = re.sub(r'\s+', ' ', response)  # Remove extra whitespace
        response = response.strip()

        # Fallback if response is too generic
        if any(phrase in response.lower() for phrase in [
            "ready to help",
            "what would you like to know",
            "how can i help",
            "what can i help",
            "feel free to ask"
        ]):
            return jsonify({
                'status': 'success',
                'response': "Would you like to connect with Kanav or need help exploring his projects?"
            })

        return jsonify({
            'status': 'success',
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': "I'm having trouble connecting right now. Please try again in a moment."
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True)