from django.contrib.auth import get_user_model

class EmailAuthBackend:

    """
    User authentication using email or username.
    """

    def authenticate(self, request, username=None, password=None):
        User = get_user_model()

        # Check if the username is an email address
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# from django.contrib.auth.models import User


# class EmailAuthBackend:

#     """
#     User authentication using email-address.
#     """

#     def authenticate(self,request, username=None, password=None):

#         try: 
#             user = User.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#             return None
#         except(User.DoesNotExist, User.MultipleObjectsReturned):
#             return None
        
#     def get_user (self,user_id):

#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None


