from app.extensions import db
from app.models.user import User
from app.extensions import bcrypt
class UserService:
    @staticmethod
    def _hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def _verify_password(user, password):
        return check_password_hash(user.password_hash, password)
    @staticmethod
    def update_username(user, new_username):
        if User.query.filter(User.username == new_username).first():
            return False
            
        user.username = new_username
        db.session.commit()
        return True

    @staticmethod
    def change_password(user, current_password, new_password):
        # Check for empty passwords
        if not current_password or not new_password:
            return False
            
        # Verify current password is correct
        if not user.password_hash or not bcrypt.check_password_hash(user.password_hash, current_password):
            return False
            
        try:
            # Generate new password hash
            user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Password change error: {str(e)}")
            return False

    @staticmethod
    def delete_account(user, password):
        if not check_password_hash(user.password_hash, password):
            return False
            
        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def get_recent_activity(user_id):
        activities = db.session.execute("SELECT * FROM activities WHERE user_id = :user_id", 
                                      {'user_id': user_id})
        
        processed = []
        for activity in activities:
            processed.append({
                'timestamp': datetime.strptime(activity['timestamp'], "%Y-%m-%d %H:%M:%S"),
                # other fields
            })
        return processed
