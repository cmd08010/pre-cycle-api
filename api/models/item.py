from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Item(models.Model):
    """Make scan class"""
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
    name = models.CharField(max_length=100, unique=True)
    recycleable = models.BooleanField()
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    barcode = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # This must return a string
        return f"The item named '{self.name}' is {self.description}. It is {self.recycleable} that it is recycleable."

    def as_dict(self):
        """Returns dictionary version of Item models"""
        return {
            'id': self.id,
            'name': self.name,
            'recycleable': self.recycleable,
            'description': self.description,
            'owner': self.owner,
            'barcode': self.barcode,
        }
