from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from . import models

class RequiredInlineFormSet(BaseInlineFormSet):
    """
        Formset that doesn't allow empty fields.
    """
    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

class PhoneNumberInline(admin.TabularInline):
    list_display = ('phone_number',)
    model = models.PhoneNumber
    extra = 1
    formset = RequiredInlineFormSet

class PassportInline(admin.TabularInline):
    list_display = ('series', 'number')
    model = models.Passport
    formset = RequiredInlineFormSet

@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'date_of_birth', 'display_passport_info',
                    'address', 'email', 'display_phone_numbers','photo', 'personnel_number', 'vk_username',
                    'login', 'password', 'date_create', 'date_update')
    inlines = (PhoneNumberInline, PassportInline)
