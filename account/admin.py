from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin
from django import forms

from account.models import Employee

# Define a form that includes permissions
class GroupAdminForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('permissions', False)
    )

    class Meta:
        model = Group
        fields = '__all__'


class GroupAdmin(DefaultGroupAdmin):
    form = GroupAdminForm

# Unregister the default Group admin
admin.site.unregister(Group)

# Register the customized Group admin
admin.site.register(Group, GroupAdmin)
admin.site.register(Employee)