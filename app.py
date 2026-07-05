from flask import Flask, render_template, request, redirect, send_from_directory, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
PASSWORD = '378'  # 💖 Changed password here!

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('dashboard.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    if not session.get('logged_in'):
        return redirect('/')
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
