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


# Diary Routes
@home_bp.route('/diary')
@login_required
def diary_list():
    # List all diary entries for the current user
    entries = DiaryEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('diary/list.html', entries=entries)

@home_bp.route('/diary/create', methods=['GET', 'POST'])
@login_required
def create_entry():
    form = DiaryEntryForm()
    if form.validate_on_submit():
        entry = DiaryEntry(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        flash('Entry created!', 'success')
        return redirect(url_for('home.diary_list'))
    return render_template('diary/create.html', form=form)

@home_bp.route('/diary/<int:entry_id>')
@login_required
def view_entry(entry_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to view this entry.', 'danger')
        return redirect(url_for('home.diary_list'))
    return render_template('diary/view.html', entry=entry)

@home_bp.route('/diary/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('home.diary_list'))
    
    form = DiaryEntryForm(obj=entry)
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.content = form.content.data
        db.session.commit()
        flash('Entry updated!', 'success')
        return redirect(url_for('home.view_entry', entry_id=entry.id))
    return render_template('diary/edit.html', form=form, entry=entry)

@home_bp.route('/diary/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('home.diary_list'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted!', 'success')
    return redirect(url_for('home.diary_list'))