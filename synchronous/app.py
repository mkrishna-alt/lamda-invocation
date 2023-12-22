from flask import Flask, render_template, request, redirect, url_for
import boto3
import json

app = Flask(__name__)

# AWS credentials and Lambda function name
aws_access_key = ''
aws_secret_key = ''
region_name = 'us-east-1'
lambda_function_name = 'synchronous'

# Configure AWS credentials
lambda_client = boto3.client('lambda', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message_body = request.form['message']

    # Invoke Lambda function
    try:
        response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse',  # synchronous invocation
            Payload=json.dumps({'message': message_body})
        )
        print("Lambda function invoked. Response:", response)
    except Exception as e:
        print("Error invoking Lambda function:", e)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
