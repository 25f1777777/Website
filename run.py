from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import TemplateNotFound
import secrets

# --------------------------------------------------
# App setup
# --------------------------------------------------
app = Flask(__name__)
app.config.update(
    SECRET_KEY=secrets.token_hex(32),
    SESSION_PERMANENT=False,
)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --------------------------------------------------
# Dummy User Model (single-user system)
# --------------------------------------------------
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Demo password (hash once at startup)
USER_PASSWORD_HASH = generate_password_hash("ChakradharTejaswini@2007@AbhiChinni#2025")

@login_manager.user_loader
def load_user(user_id):
    # Flask-Login will pass the stored user_id
    return User(user_id)

# --------------------------------------------------
# 🔒 GLOBAL LOCKDOWN — YES GATEKEEPER
# --------------------------------------------------
@app.before_request
def yes_gatekeeper():
    """
    Absolute gatekeeper:
    - NOTHING is accessible unless 'clicked_yes' is in session
    - Except:
        /              (home page)
        /click-yes     (Yes button action)
        /static/*      (CSS / JS / images)
    """

    allowed_paths = {
        url_for('home'),
        url_for('click_yes'),
    }

    # Allow static files
    if request.path.startswith('/static'):
        return

    # Allow home + yes button
    if request.path in allowed_paths:
        return

    # Block EVERYTHING else unless Yes was clicked
    if not session.get('clicked_yes'):
        return redirect(url_for('home'))

# --------------------------------------------------
# ROUTES — STAGE 1 (YES)
# --------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/click-yes')
def click_yes():
    # This is the physical "Yes" gate
    session['clicked_yes'] = True
    return redirect(url_for('accepted'))

@app.route('/accepted')
def accepted():
    # Accessible ONLY after clicking Yes
    return render_template('accepted.html')

# --------------------------------------------------
# ROUTES — STAGE 2 (LOGIN)
# --------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Already logged in → skip login page
    if current_user.is_authenticated:
        return redirect(url_for('section_show'))

    if request.method == 'POST':
        password = request.form.get('password')

        if check_password_hash(USER_PASSWORD_HASH, password):
            user = User(1)
            login_user(user)
            return redirect(url_for('section_show'))
        else:
            flash('Invalid password', 'error')

    return render_template('login.html')

# --------------------------------------------------
# ROUTES — STAGE 3 (PROTECTED CONTENT)
# --------------------------------------------------
@app.route('/sections')
@login_required
def section_show():
    return render_template('section_show.html')

@app.route('/section/<int:id>')
@login_required
def get_section(id):
    try:
        return render_template(f'section_{id}.html')
    except TemplateNotFound:
        return "Section not found", 404

# --------------------------------------------------
# LOGOUT — FULL RESET
# --------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # wipes login + Yes gate
    return redirect(url_for('home'))


@app.route('/chapter/<int:num>')
@login_required
def chapter_num(num):
    # Valid chapters
    if 1 <= num <= 7:
        return render_template(f'chapters/chapter_{num}.html')

    # Chapter 8 or any invalid number
    return render_template('chapters/chapter_inf.html')


@app.route('/chapter/<path:anything>')
@login_required
def chapter_anything(anything):
    # Handles strings, symbols, mixed paths, etc.
    return render_template('chapters/chapter_inf.html')




if __name__ == '__main__':
    app.run()
