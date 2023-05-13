from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.CharField(max_length=50)
    enabled = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'


class UserStateModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    module = models.IntegerField()
    category = models.CharField(max_length=50)
    step = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'users_state'



class DecisionTreeModel(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    instruction = models.CharField(max_length=300, default='')
    image = models.ImageField(upload_to='images/', default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


    class Meta:
        db_table = 'decision_tree'


