from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Scan(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100)
  recycleable = models.BooleanField()
  description = models.CharField(max_length=100)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )
  barcode = models.CharField(max_length=100)

  def __str__(self):
    # This must return a string
    return f"The scan named '{self.name}' is {self.description}. It is {self.recycle} that it is ripe."

  def as_dict(self):
    """Returns dictionary version of Scan models"""
    return {
        'id': self.id,
        'name': self.name,
        'recycleable': self.recycleable,
        'description': self.description
    }
