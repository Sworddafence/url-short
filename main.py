from flask import Flask, render_template, request
import zlib
import sys
import mysql.connector

# Config for database
config = {
    'user': 'root',      
    'password': '',  
    'host': 'localhost',          
    'database': 'url_short',     
    'raise_on_warnings': True
}
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS hash_urls (
        hash VARCHAR(64),
        url VARCHAR(2048),
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

def query_for_hash(connection, hash):
    cursor = connection.cursor()
    query = f"SELECT url FROM hash_urls WHERE hash = {hash};"
    try:
        cursor.execute(query)
        results = cursor.fetchall()  # Fetch all rows
        print(results)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
    return results

# Example usage



app = Flask(__name__)

if(len(sys.argv) < 2):
    print("You have no command line arguments")
cururl = sys.argv[1]

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
        uers_input = user_input.encode('utf-8')
        hash = zlib.crc32(uers_input)
        hash = f"{hash & 0xFFFFFFFF:08x}"
        hash = hash[4:]
        t = 0

        #g = query_for_hash(connection, hash)


        return f'{cururl}/{hash}'
    return render_template('index.html')

# Run the application
if __name__ == '__main__':
    try:
        connection = mysql.connector.connect(**config)
        print("Connected to the database!")
        create_table(connection)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    #Command Line arugments
    if(len(sys.argv) < 2):
        print("You have no command line arguments")

    app.run(debug=True)