from flask import Flask, redirect, url_for, render_template, request, session, send_file
import sqlite3, os, bcrypt

def scan_pdf(): 
    global pdf_folder
    global pdf_files
    pdf_folder = 'C:\\Users\\Administrator\\Desktop\\Produkttegninger'
    pdf_files = [file for file in os.listdir(pdf_folder) if file.endswith('.pdf')]
    global pdf_titles
    pdf_titles = {}
    for file_name in pdf_files:
        if file_name.endswith('.pdf'):
            file_path = os.path.join(pdf_folder, file_name)
            try:
                title = os.path.splitext(file_name)[0]
                pdf_titles[title] = file_path
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

    

def search_pdf(query):
    matching_files = []
    for title in pdf_titles:
        if query.lower() in title.lower():
            matching_files.append(title)
    return matching_files



def check_user(username, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT username, password FROM users WHERE username = ?', (username,))

    result = cur.fetchone()
    if result:
        stored_username, stored_hashed_password = result
        if bcrypt.checkpw(password.encode(), stored_hashed_password):
            return True
    return False

scan_pdf()
app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')

@app.route('/produktkatalog')
def produktkatalog():
    return render_template('produktkatalog.html')

@app.route('/omos')
def omos():
    return render_template('omos.html')


@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            session['username'] = username
            query = ""
            results = search_pdf(query)
            return render_template('search.html', results=results)
        else:
            error = 'Ugyldigt brugernavn eller adgangskode'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' in session:
        scan_pdf()
        if request.method == 'POST':
            query = request.form['query']
            results = search_pdf(query)
            return render_template('search.html', results=results)
        return render_template('search.html')
    else:
        error = 'Du skal logge ind!!'
        return render_template('login.html', error=error)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['fileToUpload']        
        upload_directory = 'C:\\Users\\Administrator\\Desktop\\Produkttegninger'
        file_path = os.path.join(upload_directory, file.filename)
        if file_path.endswith('.pdf'):
            file.save(file_path)
        else:
            error = 'Det skal være PDF'
            return render_template('search.html', error=error)
        success = 'Filen uploaded med Success'
        return render_template('search.html', success=success)
    return render_template('search.html')

@app.route('/download/<filename>')
def download(filename):
    if filename in pdf_titles:
        value = pdf_titles[filename]
    if os.path.isfile(value):
        return send_file(value, as_attachment=True)
    else:
        return "File not found."

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)




