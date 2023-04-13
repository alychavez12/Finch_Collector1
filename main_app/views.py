from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Finch, Toy
from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")


@login_required
def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, "finches/index.html", {"finches": finches})

@login_required
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

@login_required
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('finches_detail', finch_id=finch_id)

@login_required
def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('finches_detail', finch_id=finch_id)

@login_required
def unassoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('finches_detail', finch_id=finch_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('finches_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ('name', 'breed', 'description', 'age')
    template_name = 'finches/finches_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['description', 'age']    
    template_name = 'finches/finches_form.html'

class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches/'
    template_name = 'finches/finches_confirm_delete.html'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/toy_list.html'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/toy_detail.html'


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'
    
class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'
    template_name = 'toys/toy_confirm_delete.html'
