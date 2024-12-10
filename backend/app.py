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
        cur.execute('SELECT NOW();') # execute a query
        result = cur.fetchone() # fetch the result (fetch means: get the result)
        conn.close()    # close the connection
        return jsonify({'message': f'Database test successful. Current time: {result[0]}'})
    except Exception as e:
        return jsonify({'message': f'Database test failed. Error: {str(e)}'}), 500

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.json
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, data) VALUES (%s, %s);', (data['username'], data['data']))
        conn.commit() # commit the transaction (save the changes)
        conn.close()
        cur.close()
        
        print(data)
        return jsonify(data)
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    

@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_connection()
        cur = conn.cursor() # get a cursor from the connection (a cursor is like a pointer to the result)
        cur.execute('SELECT * FROM users;')
        result = cur.fetchall()
        conn.close()
        cur.close()
        return jsonify({'users': result})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    
#Now, show the data in the browser
@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users;')
        result = cur.fetchall()
        conn.close()
        cur.close()
        
        data = []
        for row in result:
            data.append({
                'id': row[0],
                'username': row[1],
                'data': row[2],
                'created_at': row[3]
            })
        return jsonify(data)
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    