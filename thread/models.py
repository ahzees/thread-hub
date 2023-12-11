from django.db import models
from authentication.models import CustomUser
import datetime

class Thread(models.Model):
    name = models.CharField("name of thread", max_length=555, null=False, blank=False, unique=True)
    members = models.ManyToManyField(CustomUser, related_name="threads")

class Messages(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="thread_messages", null=True)
    send_at = models.DateTimeField(auto_now_add=True, null=True)
    content = models.TextField("content of message", null=False, blank=False, default="Hello")
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE, null=True, related_name="messages")
    # Add other fields as needed
