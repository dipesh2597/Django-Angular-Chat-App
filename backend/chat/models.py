from django.db import models 
from django.contrib.auth.models import User
import hashlib, random, string
from datetime import date
from django.utils import timezone
from channels import Group

def randomStr(minLen, maxLen):
    strLen = random.choice(range(minLen,maxLen))
    return ''.join(random.choice(string.ascii_lowercase) for i in range(strLen))

User._meta.get_field('email')._unique = False

class ChatSession(models.Model):
    '''
    This is One to one chatting only no gourp chat so each session will have two users and start, end time for that particular session
    '''
    session_uuid = models.CharField(unique=True,max_length=50)
    first_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='first_user')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='second_user')
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True,blank=True)

    def generate_id(self):
        minLen = 15
        maxLen = 46
        valid_lengths = range(minLen, maxLen)
        idLen = random.choice(valid_lengths)
        seed = hashlib.md5(self.first_user.email.encode('utf-8')).hexdigest()
        seed += hashlib.md5(self.second_user.email.encode('utf-8')).hexdigest()
        seed += hashlib.md5(randomStr(minLen,maxLen).encode('utf-8')).hexdigest()
        last_part = hashlib.sha224(seed.encode('utf-8')).hexdigest()[:idLen]
        today = date.today()
        first_part = hashlib.md5(self.first_user.username.encode('utf-8')+str(today.year+today.month).encode('utf-8')).hexdigest()
        new_id = first_part[:5] + last_part
        self.session_uuid = new_id.upper()

    def save(self, *args, **kwargs):
        if not self.session_uuid:
           self.generate_id()
        super(ChatSession, self).save(*args, **kwargs)

    def __str__(self):
        return f'session for {self.first_user} and {self.second_user}'

    @property
    def websocket_group(self):
        ''' 
        Retunr chat room group name which will be subscribed by socket for message flow
        As session_uuid is unique will keep it as gorup name
        '''
        return Group(self.session_uuid)

class ChatMessage(models.Model):
    '''
    All message for each chat session will be store her mapped with session and from user
    '''
    session =  models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    message = models.TextField()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user')
    sent_at = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.from_user} sent at {self.sent_at}'