from flask import Flask, render_template, redirect, request, session, send_from_directory

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {
    'username': 'password'
}

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/task')
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/task')
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error = 'Username already exists. Please choose a different username.'
            return render_template('signup.html', error=error)
        else:
            if len(users) > 1:
                error = 'Only one user per browser is allowed. Please login instead.'
                return render_template('signup.html', error=error)
            users[username] = password
            session['username'] = username
            return redirect('/login')
    return render_template('signup.html')

@app.route('/task', methods=['GET', 'POST'])
def task():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        return redirect('/task')
    return render_template('task.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    session.clear()
    users.clear() 
    return 'Account deleted successfully', 200

if __name__ == '__main__':
    app.run(debug=True)
