import boto3
import json

# Configure DynamoDB client
dynamodb = boto3.client('dynamodb')

# Your actual resume data
data = {
    "basics": {
        "name": "ADNAAN KHAN",
        "label": "Cloud and DevOps Engineer",
        "email": "adnaankhan0901@gmail.com",
        "phone": "+1(438)979-7998",
        "summary": "Experienced cloud and DevOps engineer with expertise in AWS, Azure, and GCP. Skilled in Python, Linux, Terraform, Ansible, Kubernetes, and CI/CD pipelines.",
        "location": {
            "city": "Toronto",
            "region": "ON",
            "countryCode": "CA"
        },
        "profiles": [
            {
                "network": "LinkedIn",
                "url": "https://www.linkedin.com/in/adnaankhan98/"  # Replace with actual LinkedIn URL
            },
            {
                "network": "GitHub",
                "url": "https://github.com/adukhan98"  # Replace with actual GitHub URL
            }
        ]
    },
    "education": [
        {
            "institution": "Concordia University",
            "area": "Electrical and Computer Engineering",
            "studyType": "Master of Engineering",
            "endDate": "2023-12"
        },
        {
            "institution": "Vellore Institute of Technology",
            "area": "Electronics and Communication Engineering",
            "studyType": "Bachelor of Technology",
            "endDate": "2020-04"
        }
    ],
    "certifications": [
        {"name": "AWS Certified Solutions Architect Associate"},
        {"name": "Oracle Cloud Infrastructure Foundations Associate"},
        {"name": "AI For Everyone"},
        {"name": "Microsoft Azure AI- 900: Azure AI Fundamental Associate"}
    ],
    "work": [
        {
            "company": "Concordia University",
            "position": "System Administrator/IT Analyst",
            "startDate": "2023-05",
            "endDate": "Present",
            "highlights": [
                "Managed Linux server environment with 95% uptime",
                "Automated tasks using Python and Bash, reducing manual intervention by 40%",
                "Developed knowledge base using version control systems"
            ]
        },
        {
            "company": "Oracle",
            "position": "Associate Cloud Engineer",
            "startDate": "2019-12",
            "endDate": "2021-12",
            "highlights": [
                "Deployed microservices using Kubernetes and Docker",
                "Implemented CI/CD pipelines with Jenkins",
                "Optimized performance monitoring achieving 95% system availability",
                "Utilized Ansible and Terraform for IaC",
                "Collaborated in Agile environment, reducing system downtime by 75%"
            ]
        },
        {
            "company": "Bajaj Auto Pvt Ltd",
            "position": "Product Development Engineering Intern",
            "startDate": "2019-05",
            "endDate": "2019-07",
            "highlights": [
                "Analyzed sensor data and implemented automated alerts",
                "Initiated integration of industrial IoT machines"
            ]
        }
    ],
    "projects": [
        {
            "name": "Cloud-Based Dynamic Resume using AWS Services and GitHub Actions",
            "description": "Created a cloud-based resume using AWS Lambda, DynamoDB, API Gateway, and S3 with automated deployment using GitHub Actions."
        },
        {
            "name": "Blog Generation using Llama2-13b-chat, AWS Bedrock and AWS Lambda",
            "description": "Developed an automated blog generation application using Llama 2-13b-chat and AWS services."
        },
        {
            "name": "Advanced Voice Chatbot Using Gradio, Whisper, Azure OpenAI, and Eleven Labs",
            "description": "Achieved over 90% voice-to-text accuracy using OpenAI's model and implemented Eleven Labs' voice synthesis."
        },
        {
            "name": "End to End CI/CD pipeline for a Java based App",
            "description": "Deployed and built a Java app using Kubernetes, Docker, and Jenkins for automated CI/CD pipelines."
        },
        {
            "name": "Generative AI-powered GitHub Issue Retrieval and Response",
            "description": "Created a RAG system using Zephyr-7b-beta LLM, LangChain, and FAISS vector database."
        }
    ],
    "skills": [
        {"name": "Programming Languages", "keywords": ["Python", "R", "SQL", "Bash"]},
        {"name": "Cloud Computing", "keywords": ["AWS", "Azure", "GCP"]},
        {"name": "DevOps & Automation", "keywords": ["Ansible", "Terraform", "Jenkins", "Kubernetes", "Docker", "GitHub Actions"]},
        {"name": "Development Tools", "keywords": ["Agile", "Scrum", "Jira", "Git", "VS Code"]},
        {"name": "Compliance", "keywords": ["GDPR", "HIPAA", "ISO 27001", "NIST", "CIS benchmarks"]}
    ],
    "activities": [
        "Content Creator with 5M+ impressions on Generative AI, AWS, and Cloud technologies",
        "Co-founder of DesignMyWeb, a startup focused on website creation for small and medium scale companies"
    ]
}

# Convert JSON data to DynamoDB format
dynamodb_data = {}

def convert_to_dynamodb(data, parent_key=None):
    for key, value in data.items():
        if isinstance(value, dict):
            # Nested object, recurse
            convert_to_dynamodb(value, key if parent_key is None else f"{parent_key}.{key}")
        elif isinstance(value, list):
            # List, convert to string set
            dynamodb_data[f"{parent_key}.{key}"] = {"SS": [json.dumps(item) if isinstance(item, dict) else str(item) for item in value]}
        else:
            # Single value, set data type
            dynamodb_data[f"{parent_key}.{key}" if parent_key else key] = {"S": str(value)}

convert_to_dynamodb(data)

# Add id to the item
dynamodb_data['id'] = {'S': '1'}

# Prepare item for DynamoDB
dynamodb_item = {k.replace('.', '_'): v for k, v in dynamodb_data.items()}

# Insert data into DynamoDB table
try:
    dynamodb.put_item(
        TableName='Resumes',
        Item=dynamodb_item
    )
    print("Data inserted successfully")
except Exception as e:
    print(f"Error inserting data: {str(e)}")