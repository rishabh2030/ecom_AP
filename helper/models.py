from django.db import models

class BaseModel(models.Model):

    """Mixin for adding creation and modification datetime."""
    id = models.AutoField(primary_key=True,editable=False)
    createdAt = models.DateTimeField(auto_now_add=True,help_text="time when instance is created")
    modifiedAt = models.DateTimeField(auto_now=True,help_text="time when instance is modified")

    class Meta:
        abstract = True