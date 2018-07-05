from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, user_id):
        self.id = user_id

# class User():
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return '123-abc'
