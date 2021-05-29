"""
  Description:    Model manager for django
"""

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned


class ModelManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            raise MultipleObjectsReturned

    def fetch_or_create(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return self.save()
        except MultipleObjectsReturned:
            raise MultipleObjectsReturned
