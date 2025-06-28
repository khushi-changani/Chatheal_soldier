import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from scripts.user import registerUser, activate, loginUser, sendPasswordResetMail, fetchUser
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'\x02\x81I\r\x88~E\x17\xaf\xf7\xfd\x8d;\xd5M\xd8\x95Xj\xf2\xab\xc8\xd6\xe8'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        message, isLoggedIn, name = loginUser(email=email, password=password)
        if isLoggedIn:
            session['login'] = True
            session['user'] = {
                'name': name,
                'email': email
            }
            return redirect(url_for('index'))
        else:
            flash(message, "error")
            return redirect(url_for('login'))
    return render_template('signin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confPass = request.form.get('confPass')

        if password == confPass:
            message, isRegistered = registerUser(name=name, email=email, password=password)
            if isRegistered:
                return redirect(url_for('login'))
            else:
                return render_template('signup.html', error=message)
        else:
            return render_template('signup.html', error="Error! Passwords do not match")
    return render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if ('login' in session) & (session.get('login') == True):
        user = session.get('user')
        if user:
            name = user.get('name')
            email = user.get('email')
            message, isFetched, listDetails = fetchUser(email)
            if isFetched:
                dateJoined = listDetails[2]
                try:
                    adjusted_date = dateJoined.replace(day=1)
                    date = adjusted_date.strftime("%b %Y")
                    return render_template('profile.html', name=name, email=email, date=date)
                except ValueError as e:
                    flash(f"Invalid date format: {e}", "error")
                    return redirect(url_for('login'))
            else:
                flash(message, "error")
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    if ('login' in session) & (session.get('login') == True):
        return render_template('chat.html')
    return redirect(url_for('login'))

@app.route('/therapies')
def therapies():
    if ('login' in session) & (session.get('login') == True):
        return render_template('therapies.html')
    return redirect(url_for('login'))

@app.route('/tracker')
def tracker():
    if ('login' in session) & (session.get('login') == True):
        return render_template('mood_tracker.html')
    return redirect(url_for('login'))

@app.route('/forgotpass', methods=['GET', 'POST'])
def forgotPass():
    if ('login' in session) & (session.get('login') == True):
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            message, isEmailSend = sendPasswordResetMail(email=email)
            if isEmailSend:
                return redirect(url_for('login'))
            else:
                return render_template('forget_password.html', error=message)
        return render_template('forget_password.html')

@app.route('/activate/<token>')
def activateAccount(token):
    message, isActivated = activate(token=token)
    if isActivated:
        flash(message, "success")
        return redirect(url_for('login'))
    else:
        flash(message, "error")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    message = "Logged out successfully."
    flash(message, "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)