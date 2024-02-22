from django.db import models
from django.core.exceptions import ValidationError

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


class Club(models.Model):
    club_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=400)
    validity_status = models.BooleanField(default = False)
    #associated_coordinator = models.CharField(blank=True, null=True)
    club_created = models.DateTimeField()  
    club_updated = models.DateTimeField() 
     
    class Meta:
        managed = False
        db_table = 'club'

class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=20)
    description = models.CharField(max_length=400)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=30)
    event_created = models.DateTimeField()  
    event_updated = models.DateTimeField()  
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'events'

"""class ClubEvents(models.Model):
    club = models.ForeignKey(Club, models.DO_NOTHING, blank=True, null=True)
    event = models.ForeignKey('Events', models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()  
    updated = models.DateTimeField() 

    class Meta:
        managed = False
        db_table = 'club_events'"""


class ClubUser(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0) 
    is_coord = models.BooleanField(default = False)
    created = models.DateTimeField()  
    updated = models.DateTimeField() 
    is_approved = models.BooleanField(db_column='is_approved',null = False, default = False)
    class Meta:
        managed = False
        db_table = 'club_user'

class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE,  null=False)
    event = models.ForeignKey(Events, on_delete = models.CASCADE, null=False)
    is_approved = models.BooleanField( null=False)
    created = models.DateTimeField()  
    updated = models.DateTimeField() 

    class Meta:
        managed = False
        db_table = 'event_user'






