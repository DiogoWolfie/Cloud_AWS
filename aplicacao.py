from flask import Flask, render_template, request, jsonify, redirect
import boto3
import uuid
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('DynamoDBTable')

def is_palindrome(s):
    return s == s[::-1]

@app.route('/', methods=['GET', 'POST'])
def palindromo():
    try:
        if request.method == 'POST':
            name = request.form.get('name', '')
            if not name:
                return "Name not provided", 400

            reversed_name = name[::-1]
            palindrome_flag = is_palindrome(name)

            item_id = str(uuid.uuid4())
            table.put_item(Item={
                'id': item_id,
                'name': name,
                'reversed_name': reversed_name,
                'is_palindrome': palindrome_flag
            })

            return render_template('index.html', name=name, reversed_name=reversed_name, palindrome=palindrome_flag)
        else:
            return render_template('index.html')
    except Exception as e:
        return logging.error(f"Error processing request: {e}")


@app.route('/health')
def health():
    return "OK", 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
