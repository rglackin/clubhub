from django.db import models
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
        db_table = 'user'
        

