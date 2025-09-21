from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import TicketForm, ReviewForm, FollowForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Ticket, Review


@login_required
@login_required
def feed_view(request):
    tickets = Ticket.objects.all().order_by("-time_created")
    reviews = Review.objects.all().order_by("-time_created")
    return render(
        request, "reviews/feed.html", {"tickets": tickets, "reviews": reviews}
    )


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            messages.success(request, "Account created. You are now logged in.")
            login(request, user)  # loguea inmediatamente
            return redirect("feed")
        else:

            messages.error(request, "Please fix the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "reviews/signup.html", {"form": form})


def review_create_view(request):
    return render(request, "reviews/review_create.html")


@login_required
def ticket_create_view(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(reverse("feed"))
        else:
            print("Errores formulario:", form.errors)
    else:
        form = TicketForm()
    return render(request, "reviews/ticket_create.html", {"form": form})


def ticket_review_create_view(request):
    return render(request, "reviews/ticket_review_create.html")


def abonnements(request):
    return render(request, "reviews/abonnements.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return render(request, "reviews/logout.html")


def mypost(request):
    return render(request, "reviews/mesposts.html")


def modifierTicket(request):
    return render(request, "reviews/modification-ticket.html")


def modifierCritique(request):
    return render(request, "reviews/modification-critique.html")
