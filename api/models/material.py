from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Material(models.Model):
    """Make material class"""
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
    name = models.CharField(max_length=100, unique=True)
    recycleable = models.BooleanField()

    def __str__(self):
        # This must return a string
        return f"The material named '{self.name}' It is {self.recycleable} that it is recycleable."

    def as_dict(self):
        """Returns dictionary version of Material models and stuff"""
        return {
            'id': self.id,
            'name': self.name,
            'recycleable': self.recycleable,
        }
