from flask import Flask, render_template, request, redirect
import zlib
import sys
import mysql.connector
import os

# Config for database
config = {
    'user': 'bob',      
    'password': '1204',  
    'host': 'host.docker.internal',          
    'database': 'url_short',     
    'raise_on_warnings': True
}
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS hash_urls (
        hash VARCHAR(10),
        url VARCHAR(100),
        PRIMARY KEY (hash, url)
    );
    """
    try:
        cursor.execute(create_table_query)
        print("Table created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def query_for_hash(connection, hash, url):
    cursor = connection.cursor()

    query = f"SELECT hash, url FROM hash_urls WHERE hash = '{hash}';"

    try:
        cursor.execute(query)
        results = cursor.fetchall()  # Fetch all rows
        print(results)
        if(results == []):
            query = f"INSERT INTO hash_urls (hash, url) VALUES ('{hash}', '{url}');"
            print(query)
            cursor.execute(query)
            connection.commit()
        else:
            print("huh")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "failed"
    return results

# Example usage

def query_for_url(connection, hash):
    cursor = connection.cursor()
    query = f"SELECT url, hash FROM hash_urls WHERE hash = '{hash}';"
    try:
        cursor.execute(query)
        results = cursor.fetchall()  # Fetch all rows
        print(results)
        print(type(results))
        print(results[0][0])
        return (results[0][0])
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "failed"
 

app = Flask(__name__)

if(len(sys.argv) < 2):
    print("You have no command line arguments")

def remove_http(url):
    if url.startswith('http://'):
        return url[len('http://'):]
    elif url.startswith('https://'):
        return url[len('https://'):]
    else:
        return url  


# Define a route for the root URL ("/")
@app.route('/', methods=['GET', 'POST'])
def urlshortner():
    if request.method == 'POST':
        user_input = request.form['user_input']
        user_input = remove_http(user_input)
        user_input = user_input.lower()
        url = user_input.encode('utf-8')
        hash = zlib.crc32(url)
        hash = f"{hash & 0xFFFFFFFF:08x}"
        hash = hash[4:]
        g = query_for_hash(connection, hash, user_input)


        return f'{cururl}/{hash}'
    return render_template('index.html')

@app.route('/<path:randomstuff>')
def catch_all(randomstuff):
    # Redirect to a specific page, e.g., 'home'
    g = query_for_url(connection, randomstuff)
    #print(g[0])
    ##return "hi"
    url = f'https://{g}'
    return redirect(url)


# Run the application
if __name__ == '__main__':
    try:
        connection = mysql.connector.connect(**config)
        print("Connected to the database!")
        create_table(connection)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    ##Command Line arugments
    #if(len(sys.argv) < 2):
    #    print("You have no command line arguments")
    port = int(os.getenv('FLASK_PORT', 5001))
    cururl = "localhost:" + str(port)
    app.run(debug=True, port=5001, host="0.0.0.0")