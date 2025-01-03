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
        username_filter = request.args.get('username', default='', type=str) # get the username filter from the query string
        sort_by = request.args.get('sort_by', default='created_at', type=str) # get the sort_by parameter from the query string
        order = request.args.get('order', default='asc', type=str) # get the order parameter from the query string

        valid_sort_columns = ['username', 'data', 'created_at']
        if sort_by not in valid_sort_columns:
            sort_by = 'created_at'

        order =  'ASC' if order == 'asc' else 'DESC'

        conn = get_connection()
        cur = conn.cursor()
        

        if username_filter:
            cur.execute(f'''
                SELECT * FROM users WHERE username ILIKE %s ORDER BY {sort_by} {order};
            ''', (f'%{username_filter}%',))
        else:
            cur.execute(f'''SELECT * FROM users ORDER BY {sort_by} {order};''')
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
    
#Get the usernames
@app.route('/usernames', methods=['GET'])
def get_usernames():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT username FROM users;')
        result = cur.fetchall()
        conn.close()
        cur.close()
        
        usernames = [row[0] for row in result]
        return jsonify(usernames)
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    
#Delete the user
@app.route('/usernames/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM users WHERE username = %s;', (username,))
        conn.commit()
        conn.close()
        cur.close()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

#Update user data
@app.route('/usernames/<username>', methods=['PUT'])
def update_data(username):
    try:
        data = request.json
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('UPDATE users SET data = %s, created_at = NOW() WHERE username = %s;', (data['data'], username))
        conn.commit()
        conn.close()
        cur.close()
        return jsonify({'message': 'User data updated successfully'})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    