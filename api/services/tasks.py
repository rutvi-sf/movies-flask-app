from flask_mail import Message


from ..create_app import celery
from api.models import User

@celery.task
def send_confirmation_email(user_id):
    """
    Send confirmation email to users on signing up.
    """
    user = User.query.get(user_id)

    if user:
        msg = Message(
            subject="Welcome to YourApp! Confirm Your Email",
            recipients=[user.email_id],
            body=f"Hi {user.full_name},\n\nThank you for signing up!",
        )

        try:
            mail.send(msg)
        except Exception as exception:
            print(exception)