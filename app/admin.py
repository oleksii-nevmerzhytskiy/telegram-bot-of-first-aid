from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import UserModel, UserStateModel, DecisionTreeModel
from mptt.admin import DraggableMPTTAdmin

class UserAdmin(admin.ModelAdmin):
  list_display = ("chat_id", "enabled", "updated_at",)
  list_filter = (('updated_at', DateFieldListFilter),)

admin.site.register(UserModel, UserAdmin)

class UserStateAdmin(admin.ModelAdmin):
  list_display = ("id", "module", "updated_at")
  list_filter = (('updated_at', DateFieldListFilter),)
admin.site.register(UserStateModel, UserStateAdmin)


class BotAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "indented_title"
    mptt_level_indent = 30


admin.site.register(DecisionTreeModel, BotAdmin)
