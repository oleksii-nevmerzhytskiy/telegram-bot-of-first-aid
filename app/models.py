from django.db import models



class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.CharField(max_length=50)
    enabled = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
