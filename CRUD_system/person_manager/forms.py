from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import modelformset_factory
from . import models

class PassportModelForm(forms.ModelForm):
    def clean(self):
        series = self.cleaned_data.get('series')
        number = self.cleaned_data.get('number')

        if not(len(series) == 4 and len(number) == 6):
            raise ValidationError('Incorrect passport data! \'Series\' must contain four numbers, \'Number\' must contains six.')

        return super().clean()

    class Meta:
        model = models.Passport
        exclude = ['owner']

class PhoneNumberModelForm(forms.ModelForm):
    to_delete = forms.BooleanField(widget = forms.HiddenInput(attrs={'class': 'to-delete-flag'}), initial=False, required=False)

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        to_delete = self.cleaned_data.get('to_delete')
        if not to_delete and not (not phone_number or phone_number[0] == '8' and len(phone_number) == 11):
            raise ValidationError('Incorrect phone number! Phone number must contain eleven numbers and have \'8\' as the first one.')
        
        return super().clean()

    class Meta:
        model = models.PhoneNumber
        exclude = ['owner', 'id']

class PersonModelForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=['%d/%m/%Y', '%d.%m.%Y', '%d-%m-%Y'], help_text='(dd/mm/yyyy)')
    
    class Meta:
        model = models.Person
        fields = '__all__'

BasePhoneNumberFormset = modelformset_factory(models.PhoneNumber, form=PhoneNumberModelForm, extra=0)
class PhoneNumberFormset(BasePhoneNumberFormset):
    def clean(self):
        valid_forms_count = 0
        for form in self.forms:
            if form.cleaned_data.get('phone_number') and not form.cleaned_data.get('to_delete'):
                valid_forms_count += 1
        
        if valid_forms_count == 0:
            raise ValidationError('There must be at least one phone number!')
        
        return super().clean()
