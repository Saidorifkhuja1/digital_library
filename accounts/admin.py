

from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'last_name', 'family_name', 'email', 'id_card', 'education_level',
                  'work_place', 'education_place', 'home', 'avatar', 'deletion_date')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'last_name', 'family_name', 'email', 'id_card', 'education_level',
                  'work_place', 'education_place', 'home', 'avatar', 'deletion_date', 'is_active', 'is_admin')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'name', 'last_name', 'family_name', 'email', 'id_card', 'education_level',
                    'work_place', 'education_place', 'home', 'deletion_date', 'avatar', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        ('Personal info', {'fields': ('phone_number', 'password', 'name', 'last_name', 'family_name', 'email',
                                      'id_card', 'education_level', 'work_place', 'education_place', 'home', 'deletion_date', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'last_name', 'family_name', 'email', 'id_card', 'education_level',
                       'work_place', 'education_place', 'home', 'deletion_date', 'avatar', 'password1', 'password2', 'is_active', 'is_admin'),
        }),
    )
    search_fields = ('phone_number', 'email', 'name', 'last_name')
    ordering = ('phone_number',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)