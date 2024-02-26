from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    username = models.CharField(max_length=20, unique = True)
    password = models.CharField(max_length=20)
    phone_no = models.CharField('Phone Number',max_length=10, unique = True)
    email = models.CharField(max_length = 100, unique = True)
    is_admin = models.BooleanField(null=False, default = False)
    user_created = models.DateTimeField(auto_now_add=True)  
    user_updated = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(db_column='approved',null = False, default = False) 
    class Meta:
        managed = False
        db_table = 'user'

    def clean_username(self):
        if len(self.username) > 20:
            raise ValidationError("Username can only be 20 characters")
        
    def clean_password(self):
        if len(self.password) < 7 or not any(char.isdigit() for char in self.password) or not any(char.isupper() for char in self.password):
            raise ValidationError("Password must be at least 7 characters long and include a capital letter and a number")
    
    def clean_email(self):

        if '@' not in self.email or not self.email.endswith('.com'):
            raise ValidationError("Invalid email address")
        
    def clean_phone_no(self):
        if not self.phone_no.isdigit() or len(self.phone_no) != 9:
            raise ValidationError('Invalid phone number')

    def get_absolute_url(self):
        return(reverse('crm:index'))
    def __str__(self):
        return self.username

class Club(models.Model):
    club_id = models.AutoField(primary_key=True)

    name = models.CharField('Club Name',max_length=20, unique = True)
    description = models.TextField()
    club_created = models.DateTimeField(db_column='created',auto_now_add=True)  
    club_updated = models.DateTimeField(db_column='updated',auto_now_add=True) 

    def get_absolute_url(self):
        return(reverse('crm:club_detail',kwargs={'pk':self.club_id}))
    class Meta:
        managed = False
        db_table = 'club'
    def __str__(self) -> str:
        return self.name


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=20)
    description = models.TextField()
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=30)
    event_created = models.DateTimeField(auto_now_add=True)  
    event_updated = models.DateTimeField(auto_now_add=True)  
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'events'



class ClubUser(models.Model):
    id = models.AutoField(primary_key=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0) 
    is_coord = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now_add=True) 
    is_approved = models.BooleanField('Membership Status',db_column='is_approved',null = False, default = False)
    class Meta:
        managed = False
        db_table = 'club_user'
    @classmethod
    def create(cls, club_id,user_id):
        club = Club.objects.get(club_id = club_id)
        user = User.objects.get(id =user_id )
        return cls(club=club, user=user)
    
    def __str__(self) -> str:
        return f"User:{self.user}\nClub:{self.club}"
class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE,  null=False)
    event = models.ForeignKey(Events, on_delete = models.CASCADE, null=False)
    is_approved = models.BooleanField( null=False, default=False)
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now_add=True) 

    class Meta:
        managed = False
        db_table = 'event_user'
    @classmethod
    def create(cls, user,event):
        return cls(user=user,event=event)