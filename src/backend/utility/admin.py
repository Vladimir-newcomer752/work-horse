from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.translation import pgettext_lazy

from .models import Configuration, ConfigurationAdmin, User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=pgettext_lazy('User', 'Password'),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=pgettext_lazy('User',
                                                    'Password confirmation'),
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        link = reverse_lazy('admin:auth_user_password_change',
                            args=[self.instance.id])
        self.fields['password'].help_text = (
            f'<a href="{link}">Click here to '
            '<strong>change the user password</strong></a>.')

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name',
                  'login_redirect_page', 'first_last',
                  'is_active', 'is_superuser', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        if 'password' in self.initial:
            return self.initial["password"]
        else:
            return ''


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_superuser', 'is_staff')
    list_filter = ('is_active', 'is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('first_name',
                           'last_name',
                           'email',
                           'password')}),
        ('Details', {'fields': ('date_joined',
                                'last_login',
                                'login_redirect_page',
                                'first_last')}),
        ('Status', {'fields': ('is_active',
                               'is_superuser',
                               'is_staff')}),
        ('Permissions', {'fields': ('groups',
                                    'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name',
                       'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Models registration
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(User, CustomUserAdmin)
