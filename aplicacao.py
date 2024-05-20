from flask import Flask, render_template, request, jsonify
import boto3
import uuid
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('MyDynamoDBTable')

def is_palindrome(s):
    return s == s[::-1]

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            name = request.form['name']
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

        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return render_template('error.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
