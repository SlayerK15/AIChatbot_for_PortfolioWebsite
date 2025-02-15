# 1. app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from anthropic import Anthropic
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS with allowed origins
ALLOWED_ORIGINS = [
    'http://localhost:5000',  # Local development
    os.getenv('FRONTEND_URL', ''),  # Production frontend URL
    os.getenv('ECS_SERVICE_URL', '')  # ECS service URL
]

CORS(app, resources={
    r"/chat": {
        "origins": [origin for origin in ALLOWED_ORIGINS if origin],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'), base_url="https://api.anthropic.com")

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
    8. For questions about the chatbot itself, explain that you're a Flask-based portfolio assistant created by Kanav using Python, Flask, and the Anthropic Claude API
    9. NEVER generate or make up repository links - only use the exact social links provided
    10. For questions about source code or repositories, direct users to Kanav's GitHub profile
    11. For deployment questions, mention that the frontend is hosted on Netlify and the chatbot backend runs on AWS ECS

    Tone guidelines:
    - Be professional but conversational
    - Focus on technical details and accomplishments
    - Avoid overly casual language
    - Stay factual and specific
    """

def handle_social_query(message):
    social_keywords = ['github', 'linkedin', 'social', 'profile', 'repository', 'repo', 'source code', 'source']
    if any(keyword in message.lower() for keyword in social_keywords):
        return True, "You can find Kanav on GitHub at https://github.com/SlayerK15 and LinkedIn at https://www.linkedin.com/in/gathekanav/."
    return False, None

def handle_chatbot_query(message):
    chatbot_keywords = ['who made you', 'what are you', 'how were you made', 'what technologies', 
                       'why were you made', 'your purpose', 'what is your purpose', 
                       'how do you work', 'tell me about yourself']
    if any(keyword in message.lower() for keyword in chatbot_keywords):
        return True, "I'm a portfolio assistant created by Kanav Gathe using Python, Flask, and the Anthropic Claude API. I was built to help visitors learn about Kanav's DevOps projects and experience, particularly his work with AWS cloud infrastructure and containerization."
    return False, None

def handle_deployment_query(message):
    deployment_keywords = ['deployed', 'hosting', 'where are you hosted', 'where do you run', 
                         'which service', 'infrastructure', 'container', 'ecs', 'aws']
    if any(keyword in message.lower() for keyword in deployment_keywords):
        return True, "The portfolio frontend is hosted on Netlify for optimal performance, while this chatbot runs as a containerized Flask application on AWS ECS. This demonstrates Kanav's expertise in both cloud platforms and containerization."
    return False, None

def handle_greeting(message):
    basic_greetings = ['hi', 'hello', 'hey', 'greetings']
    time_greetings = ['good morning', 'good afternoon', 'good evening']
    how_are_you = ['how are you', 'how r u', 'how you', 'how r you', 'how are u']
    
    message = message.lower().strip()
    
    if any(greeting in message for greeting in how_are_you):
        return True, "I'm doing great, thanks for asking! Would you like to connect with Kanav or need help exploring his projects?"
    
    if any(message == greeting for greeting in basic_greetings):
        return True, "Hello! Would you like to connect with Kanav or need help exploring his projects?"
    
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

def handle_skills_query(message):
    skills_keywords = ['skill', 'technology', 'tech stack', 'expertise', 'experience', 'know']
    if any(keyword in message.lower() for keyword in skills_keywords):
        return True, "Kanav specializes in AWS cloud services (EC2, ECS, S3), Docker, Kubernetes, and Terraform. He has extensive experience building CI/CD pipelines with Jenkins and managing Linux infrastructure."
    return False, None

def handle_certification_query(message):
    cert_keywords = ['certification', 'certificate', 'certified', 'courses', 'training', 'badge', 'achievement']
    if any(keyword in message.lower() for keyword in cert_keywords):
        return True, "Kanav is a Google Cloud Silver League member (4140 points) with certifications in Google Cloud Fundamentals and SRE Culture. He also holds certifications in Docker (KodeKloud), Git/GitHub (IBM), and Linux Basics (KodeKloud)."
    return False, None

def handle_location_query(message):
    location_keywords = ['where', 'location', 'city', 'based', 'live', 'stay', 'from']
    if any(keyword in message.lower() for keyword in location_keywords):
        return True, "Kanav is based in Amravati, Maharashtra, India, and works remotely as a DevOps Engineer, deploying solutions across multiple AWS regions globally. He has experience working with cloud infrastructure worldwide and is not limited to any specific region."
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

        # Check for location query
        is_location, location_response = handle_location_query(user_message)
        if is_location:
            return jsonify({'status': 'success', 'response': location_response})

        # Check for certification query
        is_certification, certification_response = handle_certification_query(user_message)
        if is_certification:
            return jsonify({'status': 'success', 'response': certification_response})

        # Check for social media/repository queries
        is_social_query, social_response = handle_social_query(user_message)
        if is_social_query:
            return jsonify({
                'status': 'success',
                'response': social_response
            })

        # Check for deployment queries
        is_deployment_query, deployment_response = handle_deployment_query(user_message)
        if is_deployment_query:
            return jsonify({
                'status': 'success',
                'response': deployment_response
            })

        # Check for chatbot-related queries
        is_chatbot_query, chatbot_response = handle_chatbot_query(user_message)
        if is_chatbot_query:
            return jsonify({
                'status': 'success',
                'response': chatbot_response
            })

        # Check for greetings
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

        # Check for skills queries
        is_skills, skills_response = handle_skills_query(user_message)
        if is_skills:
            return jsonify({
                'status': 'success',
                'response': skills_response
            })

        # Create focused context about portfolio for Claude API
        context = f"""{create_system_message()}

        Portfolio Information:
        - Role: DevOps Engineer
        - Location: Amravati, Maharashtra, India (Open to Global Remote Work)
        - Expertise: AWS cloud, CI/CD pipelines, infrastructure automation
        - Technical Skills: AWS (EC2, ECS, S3), Docker, Kubernetes, Terraform, Jenkins, Linux
        
        Certifications & Achievements:
        - Google Cloud Fundamentals: Core Infrastructure (Google Cloud)
        - Developing a Google SRE Culture (Google Cloud)        
        - Git/GitHub (IBM)
        - Linux Basics (KodeKloud)
        - Amazon Elastic Container Service (KodeKloud)
        - Docker Training Course for the Absolute Beginner (KodeKloud)
        - Shell Scripts for Beginners (KodeKloud)
        - 12 Factor App (KodeKloud)
        
        Social Links:
        - GitHub: https://github.com/SlayerK15
        - LinkedIn: https://www.linkedin.com/in/gathekanav/
        
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

        # Clean up response and check for fake links
        response = re.sub(r'\s+', ' ', response)
        response = response.strip()
        
        # If response contains github.com but not the correct profile, redirect to actual profile
        if 'github.com' in response.lower() and 'github.com/SlayerK15' not in response:
            response = "You can find Kanav's projects on his GitHub profile at https://github.com/SlayerK15"

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

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Service is running'
    })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_ENV') == 'development')