from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Material(models.Model):
    """Make material class"""
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
    name = models.CharField(max_length=100, unique=True)
    recycleable = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # This must return a string
        return f"{self.name}"

    def as_dict(self):
        """Returns dictionary version of Material models and stuff"""
        return {
            'id': self.id,
            'name': self.name,
            'recycleable': self.recycleable,
        }
