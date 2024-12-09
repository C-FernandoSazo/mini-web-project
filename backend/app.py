from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app) # allow requests from any origin

DB_HOST = os.getenv('DB_HOST', 'database')
DB_NAME = os.getenv('POSTGRES_DB', 'mydatabase')
DB_USER = os.getenv('POSTGRES_USER', 'user')
DB_PASS = os.getenv('POSTGRES_PASSWORD', '123456')


def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn


@app.route('/')

def main_function():
    return '<p>Hello World</p>'

@app.route('/database-test')
def db_test():
    try:
        conn = get_connection() # get a connection to the database
        cur = conn.cursor() # get a cursor from the connection
        cur.execute('SELECT 1;') # execute a simple SQL statement
        result = cur.fetchone() # fetch the result (fetch means: get the result)
        conn.close()    # close the connection
        return f'Database test was successful: {result[0]}'
    except Exception as e:
        return f'Database test failed: {str(e)}'

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json.get('data', '')
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    return jsonify({'message': f'Data received: {data}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    