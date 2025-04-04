from flask import flash, jsonify, render_template, redirect, url_for
from flask import Blueprint, request
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required, logout_user
from flask_wtf.csrf import CSRFProtect
from app.models.user import User 
from app.extensions import db
from .forms import LoginForm, RegistrationForm
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()
csrf = CSRFProtect()


#API endpoint for Non-admins (Uncomment for admin + middleware to add later) 
@auth_bp.route('/api/users', methods=['GET'])
@login_required 
def api_list_users():
    # Check if current user is admin (assuming you have is_admin field)
    #if not current_user.is_admin:
     #   return jsonify({'error': 'Forbidden - Admin access required'}), 403
    
    # pagination parameters with defaults
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Paginated query
    users = User.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    # Format response
    users_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        #'is_admin': user.is_admin,
        'created_at': user.created_at.isoformat() if user.created_at else None
    } for user in users.items]
    
    return jsonify({
        'users': users_list,
        'total_users': users.total,
        'total_pages': users.pages,
        'current_page': users.page
    })


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if request.headers.get('X-Requested-With')== 'XMLHttpRequest':
            return jsonify({'redirect': url_for('home.dashboard')})
        return redirect(url_for('home.dashboard'))
    form = LoginForm()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                print('Login Successful - AJAX')
                return jsonify({
                    'message': 'Login successful',
                    'redirect': url_for('home.dashboard')
                })
            print('Login Unsuccessful - AJAX')
            return jsonify({'error': 'Invalid credentials'}), 401
        return jsonify({'error': 'Invalid form data'}), 400
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home.dashboard'))
        flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home. dashboard'))
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Database error occurred. Please try again.', 'danger')
            print(f"Database error: {str(e)}")
        except Exception as e:
            flash('An error occurred. Please try again.', 'danger')
            print(f"Unexpected error: {str(e)}")
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home.index'))