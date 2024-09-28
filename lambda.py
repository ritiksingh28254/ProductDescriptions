import json
import os
import requests
import boto3
from uuid import uuid4
from dotenv import load_dotenv


# Set up the DynamoDB resource and connect to the table
load_dotenv()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProductDescriptions')

# Load the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def lambda_handler(event, context):
    # Get user inputs from the API request
    body = json.loads(event['body'])
    product_name = body['product_name']
    category = body['category']

    # Create a prompt for GPT-3.5 Turbo
    messages = [
        {"role": "user", "content": f"Write a product description for a {category} named {product_name}."}
    ]

    # Call OpenAI API to generate the product description
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
        'temperature': 0.7
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    gpt_response = response.json()

    # Log the full API response for debugging
    print("API Response:", gpt_response)

    # Check if the response contains the expected 'choices'
    if 'choices' in gpt_response and len(gpt_response['choices']) > 0:
        generated_description = gpt_response['choices'][0]['message']['content'].strip()
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to generate description',
                'details': gpt_response
            })
        }

    # Save the generated description to DynamoDB
    product_id = str(uuid4())  # Generate a unique ID for the product
    table.put_item(Item={
        'product_id': product_id,
        'product_name': product_name,
        'category': category,
        'description': generated_description
    })

    # Return the product description and the product_id as the response
      
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Adjust to your allowed origin if needed
            'Access-Control-Allow-Methods': 'POST',  # Specify allowed methods
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({
            'product_id': product_id,
            'product_name': product_name,
            'category': category,
            'description': generated_description
        })
    }