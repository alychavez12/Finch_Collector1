from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView

from .models import Finch, Toy
from .forms import FeedingForm


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def finches_index(request):
    finches = Finch.objects.all()
    return render(request, "finches/index.html", {"finches": finches})

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    feeding_form = FeedingForm()
    finch_toy_ids = finch.toys.all().values_list('id')
    toys_finch_doesnt_have = Toy.objects.exclude(id__in=finch_toy_ids) 

    return render(request, "finches/detail.html", {
        "finch": finch,
        "feeding_form": feeding_form,
        "toys": toys_finch_doesnt_have
        })

def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('finches_detail', finch_id=finch_id)

def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('finches_detail', finch_id=finch_id)

class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'
    template_name = 'finches/finches_form.html'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['description', 'age']    
    template_name = 'finches/finches_form.html'

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'
    template_name = 'finches/finches_confirm_delete.html'

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyList(ListView):
    model = Toy
    template_name = 'toys/toy_list.html'

class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/toy_detail.html'


class ToyUpdate(UpdateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'
    
class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
    template_name = 'toys/toy_confirm_delete.html'
