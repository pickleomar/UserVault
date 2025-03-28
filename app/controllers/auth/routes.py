from flask import Blueprint, render_template, request, redirect ,url_for, flask_sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User 
from app.extensions import db

auth_bp = Blueprint('auth',__name__,url_prefix='/auth')


@auth_bp.route('/login',methods=['GET','POST'])

def login():
    if request.method== 'POST':
        email= request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not User or not check_password_hash(user.password_hash, password):
            flash('Invalid Credentials !')
            return redirect(url_for('auth.login'))
        return render_template(url_for('dashboard.html'))
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])

def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('email')
        password = request.form.get('username')

        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('auth.register'))

        new_user = User(
            username= username
            email= email
            password_hash= generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/regiter.html')

@auth_bp.route('/logout')
def logout():
    return redirect(url_for('home.index'))
