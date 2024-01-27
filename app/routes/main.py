from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, current_user
from app.extensions import db
from app.models.user import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/redirect_to_department_chat')
@login_required
def redirect_to_department_chat():
    # Assuming the 'department' attribute is stored in the user model
    user_department = current_user.department
    return redirect(url_for('main.department_chat', department=user_department))
                    
@main.route('/chat/<department>')
@login_required
def department_chat(department):
    # Ensure the user belongs to this department or is an admin
    if current_user.department != department and not current_user.is_admin:
        # Redirect to homepage or show an error message
        return redirect(url_for('main.index'))
    return render_template('chat_in_department.html', department=department)

@main.route('/register', methods=['POST'])
def register():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    department = request.form.get('department')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already exists.', 'danger')
        return redirect(url_for('main.index'))

    # Validate and create new user
    if password == confirm_password:
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(name=name, email=email, department=department, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user
        login_user(new_user)

        flash('Account created successfully!', 'success')
        return redirect(url_for('main.department_chat', department=new_user.department))
    else:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # Check if the user actually exists
        # Take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('main.login'))  # If the user doesn't exist or password is wrong, reload the page

        # If the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.index'))
    return render_template('index.html')