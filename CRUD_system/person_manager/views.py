from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from . import models
from . import forms

class PersonListView(generic.ListView):
    model = models.Person
    template_name = 'person_manager/people_list.html'
    context_object_name = 'people'

    paginate_by = 10

class PersonDetailView(generic.DetailView):
    model = models.Person
    template_name = 'person_manager/person_detail.html'
    context_object_name = 'person'

class PersonDeleteView(generic.DeleteView):
    model = models.Person
    success_url = reverse_lazy('all_people')

def create_person(request):
    person = models.Person()
    passport = models.Passport()
    passport.owner = person
    phone_numbers = person.phonenumber_set.all()

    if request.method == 'POST':
        person_form = forms.PersonModelForm(request.POST, request.FILES, instance=person)
        passport_form = forms.PassportModelForm(request.POST, instance=passport)
        formset = forms.PhoneNumberFormset(request.POST, queryset=phone_numbers)

        if all([person_form.is_valid(), passport_form.is_valid(), formset.is_valid()]):
            person_form.save()
            passport_form.save()

            for form in formset:
                phone_number = form.save(commit=False)
                data = form.cleaned_data
                if not data.get('to_delete') and phone_number.phone_number:
                    phone_number.owner = person
                    phone_number.save()

            return redirect(person.get_absolute_url())
    else:
        person_form = forms.PersonModelForm(instance=person)
        passport_form = forms.PassportModelForm(instance=passport)
        formset = forms.PhoneNumberFormset(queryset=phone_numbers)

    return render(request, 'person_manager/create_update_person.html', {'person_form': person_form,
                                                                 'passport_form': passport_form,
                                                                 'phone_number_formset': formset})

def update_person(request, pk):
    person = get_object_or_404(models.Person, pk=pk)
    passport = person.passport
    phone_numbers = person.phonenumber_set.all()

    if request.method == 'POST':
        person_form = forms.PersonModelForm(request.POST, request.FILES, instance=person)
        passport_form = forms.PassportModelForm(request.POST, instance=passport)
        formset = forms.PhoneNumberFormset(request.POST, queryset=phone_numbers)
        if all([person_form.is_valid(), passport_form.is_valid(), formset.is_valid()]):
            person_form.save()
            passport_form.save()

            for form in formset:
                phone_number = form.save(commit=False)
                data = form.cleaned_data
                if not data.get('to_delete') and phone_number.phone_number:
                    phone_number.owner = person
                    phone_number.save()
                elif phone_number.id:
                    phone_number.delete()
            
            return redirect(person.get_absolute_url())
    else:
        person_form = forms.PersonModelForm(instance=person)
        passport_form = forms.PassportModelForm(instance=passport)
        formset = forms.PhoneNumberFormset(queryset=phone_numbers)
    return render(request, 'person_manager/create_update_person.html', {'person_form': person_form,
                                                                 'passport_form': passport_form,
                                                                 'phone_number_formset': formset})
