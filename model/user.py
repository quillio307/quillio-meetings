from setup import db

class User(db.Document):
    """ Definition for a User """
    email = db.EmailField(required=True, unique=True,
                          min_length=3, max_length=35)
    name = db.StringField(required=True, min_length=4, max_length=20)
    password = db.StringField(required=True, min_length=5, max_length=100)
    active = db.BooleanField(default=True)
    authenticated = db.BooleanField(required=False, default=False)
    groups = db.ListField(db.ReferenceField('Group'), default=[])
    meta = {'strict': False}

    def is_authenticated(self):
        """ Determines if a User is authenticated """
        return self['authenticated']

    def is_active(self):
        """ Determines if a User is currently active """
        return self['active']

    # NOTE: always returns false, anonymous users are not supported
    def is_anonymous(self):
        """ Determines if a User is anonymous; this will always return false
        becuase this functionality is not currently supported """
        return False

    def get_id(self):
        """ Fetches the unicode id for the Usera """
        return str(User.objects(email__exact=self['email'])[0].id)
