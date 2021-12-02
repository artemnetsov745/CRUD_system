from django.urls import reverse
from django.db import models
from django.contrib.auth.models import Group
import pathlib
import uuid

def person_image_path_handler(instance, filename):
    path = pathlib.Path(filename)
    return f'avatars/{uuid.uuid1()}{path.suffix}'

class Person(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=500)
    email = models.EmailField()
    photo = models.ImageField(upload_to=person_image_path_handler, null=True, blank=True)
    personnel_number = models.CharField(max_length=30)
    vk_username = models.CharField(max_length=100, null=True, blank=True, verbose_name='VK Username')
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100) # in hash?
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(to=Group)

    def display_phone_numbers(self):
        items = [item.phone_number for item in self.phonenumber_set.all()]
        return ', '.join(items)
    display_phone_numbers.short_description = 'Phone numbers'

    def display_passport_info(self):
        passport = self.passport
        return f'{passport.series} {passport.number}'
    display_passport_info.short_description = 'Passport'

    def display_groups(self):
        groups = map(lambda group: group.name, self.groups.all())
        return ', '.join(groups)
    display_groups.short_description = 'Groups'

    def get_absolute_url(self):
        return reverse('person_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['-date_create']

class Passport(models.Model):
    series = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
    owner = models.OneToOneField(to=Person, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.series} {self.number}'

class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    owner = models.ForeignKey(to=Person, on_delete=models.CASCADE)

    def __str__(self):
        if self.phone_number:
            return self.phone_number
        return ''
