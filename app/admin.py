from django.contrib import admin
from .models import UserModel, UserStateModel, DecisionTreeModel
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

admin.site.register(UserModel)
admin.site.register(UserStateModel)


class BotAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "indented_title"
    mptt_level_indent = 30


admin.site.register(DecisionTreeModel, BotAdmin)
