# my_app/models.py
from django.db import models

class Message(models.Model):  # এই নামটা ঠিক Message হতে হবে (বড় M দিয়ে)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"