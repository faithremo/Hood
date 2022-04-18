from django import forms
from .models import Business, NeighbourHood, Post, Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.http  import HttpResponse
from django.shortcuts import render
from .forms import BusinessForm, NeighbourHoodForm, CreateUserForm, PostForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    hoods = NeighbourHood.objects.all()
    return render(request, 'index.html', {'hoods': hoods})

@login_required(login_url='loginpage')
def create_hood(request):
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.save()
            return redirect('index')
    else:
        form = NeighbourHoodForm()
    return render(request, 'newhood.html', {'form': form})

def registerPage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginpage') 
        name = form.cleaned_data.get("username")
        messages.success(request, 'Account was created for' , name)
    context = {'form':form, 'profile':profile}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request, 'Incorrect Username or Password')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('loginpage')

@login_required(login_url='loginpage')
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    user = request.user
    if request.method == 'POST':
        prof_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = ProfileForm(instance=request.user.profile)
    profiles = Profile.objects.filter(user=user)
    context = {
        'profiles': profiles,
        'prof_form': prof_form,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='loginpage')
def update_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST':
            prof_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if prof_form.is_valid():
                prof_form.save()
                return redirect('profile')
    else:
        prof_form = ProfileForm(instance=request.user.profile)
        context = {
            'prof_form': prof_form,
        }
    return render(request, 'updateprofile.html', context)

@login_required(login_url='loginpage')
def neighbourhood(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    posts = Post.objects.filter(hood=hood)
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            biz_form = form.save(commit=False)
            biz_form.user = request.user.profile
            biz_form.save()
            return redirect('neighbourhood', hood_id)
    else:
        form = BusinessForm()
    params = {
        'hood': hood,
        'business': business,
        'form': form,
        'posts': posts
    }
    return render(request, 'neighbourhood.html', params)

@login_required(login_url='loginpage')
def business(request,hood_id):
    hood = NeighbourHood.objects.get(id= hood_id)
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            biz_form = form.save(commit=False)
            biz_form.user = request.user.profile
            biz_form.save()
            return redirect('neighbourhood', hood_id)
    else:
        form = BusinessForm()
    return render(request, 'newbiz.html', {'form': form, 'hood': hood})

@login_required(login_url='loginpage')
def post(request,hood_id):
    hood = NeighbourHood.objects.get(id= hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.user = request.user.profile
            post_form.save()
            return redirect('neighbourhood', hood_id)
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form, 'hood': hood})

@login_required(login_url='loginpage')
def search_results(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_business = Business.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message, "businesses": searched_business, 'search': search_term})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

@login_required(login_url='loginpage')
def join_hood(request, hood_id):
    neighbourhood = get_object_or_404(NeighbourHood, id=hood_id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('neighbourhood', hood_id)

@login_required(login_url='loginpage')
def leave_hood(request, hood_id):
    hood = get_object_or_404(NeighbourHood, id=hood_id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('neighbourhood', hood_id)
