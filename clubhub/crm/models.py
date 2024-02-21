from django.db import models
""" deprecated
class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)         
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone_no = models.CharField('Phone Number',max_length=10)
    email = models.CharField(max_length = 100)
    #TODO: change db_column to is_admin when merging with tables branch
    is_admin = models.BooleanField(default = False, db_column = 'admin')

    class Meta:
        managed = False
        db_table = 'user'"""
class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone_no = models.CharField('Phone Number',max_length=10)
    email = models.CharField(max_length = 100)
    is_admin = models.BooleanField(null=False, default = False)
    user_created = models.DateTimeField(auto_now_add=True)  
    user_updated = models.DateTimeField(auto_now_add=True) 
    class Meta:
        managed = False
        db_table = 'user'

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
    user = models.ForeignKey(User, models.DO_NOTHING,default=0) 
    is_coord = models.BooleanField(default = False)
    created = models.DateTimeField()  
    updated = models.DateTimeField() 

    class Meta:
        managed = False
        db_table = 'club_user'






