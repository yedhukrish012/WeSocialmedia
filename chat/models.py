from django.db import models

from users.models import Account



class ChatRoom(models.Model):
    members = models.ManyToManyField(Account, related_name='chat_rooms')

    def __str__(self):
        return ', '.join([str(member) for member in self.members.all()])

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f'{self.sender}'

   
