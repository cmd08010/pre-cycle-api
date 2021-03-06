from django.db import models
from django.contrib.auth import get_user_model
import json

from .material import Material

# Create your models here.
class Scan(models.Model):
    """Make scan class"""
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
    name = models.CharField(max_length=100)
    recycleable = models.BooleanField()
    description = models.CharField(max_length=1000)
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    barcode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_json(self):
        return {'data': self.data}

    def __str__(self):
        # This must return a string
        return f"The scan '{self.id}' named '{self.name}' is {self.description}. It is {self.recycleable} that it is recycleable."

    def as_dict(self):
        """Returns dictionary version of Scan models"""
        return {
            'id': self.id,
            'name': self.name,
            'recycleable': self.recycleable,
            'description': self.description,
            'material': self.material,
            'owner': self.owner,
            'barcode': self.barcode,
        }
