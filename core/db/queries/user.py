from sqlalchemy import true


def get_user(user_id, session):
    """ Get a user object by user id """

    from core.models import User
    user = session.query(User).filter(
            User.id == user_id,
            User.is_active == true(),
        ).first()

    return user
