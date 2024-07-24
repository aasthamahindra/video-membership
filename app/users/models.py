import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from app.config import get_settings
from . import validators
from . import security

settings = get_settings()

class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email}, user_id={self.user_id})"
    
    def set_password(self, password, commit=False):
        hash = security.hash_password(password=password)
        self.password = hash
        if commit:
            self.save()
        return True
    
    def verify_password(self, password):
        hash = self.password
        verified, _ = security.verify_hash(hash, password)
        return verified
    
    @staticmethod
    def create_user(email: str, password=None):
        query = User.objects.filter(email=email)
        if query.count() != 0:
            raise Exception("User already exists!")
        
        # validate email
        valid, msg, email = validators._validate_email(email=email)
        if not valid:
            raise Exception(f"Invalid email: {msg}")
        
        user = User(email=email)
        user.set_password(password)
        user.save()
        return user