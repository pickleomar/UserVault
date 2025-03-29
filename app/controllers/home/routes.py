from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.user_service import UserService
from flask import redirect, url_for
from .forms import ProfileForm, ChangePasswordForm

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@home_bp.route('/dashboard')
@login_required
def dashboard():
     form = ProfileForm()  
     form.username.data = current_user.username 
     return render_template('home/dashboard.html', form=form)

@home_bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    new_username = request.form.get('username')
    
    if UserService.update_username(current_user, new_username):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'message': 'Profile updated successfully',
                'update': {
                    'selector': '.card-title',
                    'content': new_username
                }
            })
        return redirect(url_for('home.dashboard'))
    
    return jsonify({'message': 'Update failed', 'category': 'danger'}), 400

@home_bp.route('/load-activity')
@login_required
def load_activity():
    activities = UserService.get_recent_activity(current_user.id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'update': {
                'selector': '#activityContent',
                'content': render_template('home/_activity_partial.html', 
                                          recent_activity=activities)
            }
        })
    
    return render_template('home/dashboard.html', 
                         recent_activity=activities)

@home_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    current = request.form.get('current_password')
    new = request.form.get('new_password')
    
    if UserService.change_password(current_user, current, new):
        return jsonify({
            'message': 'Password changed successfully',
            'redirect': url_for('auth.logout')
        })
    
    return jsonify({'message': 'Password change failed', 'category': 'danger'}), 400

@home_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    password = request.form.get('password')
    
    if UserService.delete_account(current_user, password):
        return jsonify({
            'message': 'Account deleted successfully',
            'redirect': url_for('home.dashboard')
        })
    
    return jsonify({'message': 'Account deletion failed', 'category': 'danger'}), 400

@home_bp.route('/stats')
@login_required
def load_stats():
    stats = UserService.get_user_stats(current_user.id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'update': {
                'selector': '#statsContent',
                'content': render_template('home/_stats_partial.html', 
                                          stats=stats)
            }
        })
    
    return render_template('home/dashboard.html', stats=stats)