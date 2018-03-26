from unevu.models import UserProfile, User

def create_user():
    # Create a user
    user = User.objects.create_user(username="testuser", password="test1234",
                                      first_name="Test", last_name="User", email="testuser@testuser.com")
    user.set_password(user.password)
    user.save()
    
    return user