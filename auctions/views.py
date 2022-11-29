from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,auction_list


def index(request):
    active_auction_list = auction_list.objects.filter(isactive = True) 
    
    return render(request, "auctions/index.html",{
        "auction_list": active_auction_list,
        
    })


def close_auction(request,id):
    listing_data = auction_list.objects.get(pk=id)
    listing_data.isactive = False
    listing_data.save()
    return HttpResponseRedirect(reverse("index"))


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    else:
        #  Getting the data from the form
        title = request.POST["title"]
        description = request.POST["content"]
        image_url = request.POST["image_url"]

        currentuser = request.user
        #  Creating new list object and add data
        new_auction_list = auction_list(title= title, descrption= description, image= image_url,owner= currentuser)

        #  Save the object to our database
        new_auction_list.save()
        #  Redirect to home page
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
