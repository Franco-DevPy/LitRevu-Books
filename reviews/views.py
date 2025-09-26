from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import TicketForm, ReviewForm, FollowForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Ticket, Review


@login_required
def feed_view(request):
    tickets = Ticket.objects.all().order_by("-time_created")
    reviews = Review.objects.all().order_by("-time_created")

    reviewed_ticket_ids = set(
        Review.objects.filter(user=request.user).values_list("ticket_id", flat=True)
    )

    return render(
        request,
        "reviews/feed.html",
        {
            "tickets": tickets,
            "reviews": reviews,
            "reviewed_ticket_ids": reviewed_ticket_ids,
        },
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


@login_required
def review_create_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        messages.info(request, "Vous avez déjà rédigé une critique pour ce ticket.")
        return redirect("feed")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, "Critique créée.")
            return redirect("feed")

        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/review_create.html",
        {"form": form, "ticket": ticket},
    )


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


@login_required
def mypost(request):
    """
    Mostrar los tickets y reviews del usuario conectado.
    """
    # 1) Obtener tickets del usuario, ordenados por fecha descendente
    tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")

    # 2) Obtener reviews del usuario. select_related('ticket') evita consultas adicionales
    reviews = (
        Review.objects.filter(user=request.user)
        .select_related("ticket")
        .order_by("-time_created")
    )

    context = {
        "tickets": tickets,
        "reviews": reviews,
        # 'page_tickets': page_tickets,
        # 'page_reviews': page_reviews,
    }
    return render(request, "reviews/mesposts.html", context)


@login_required
def modifierTicket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    # Sécurité: seul le propriétaire peut éditer
    if ticket.user != request.user:
        messages.error(request, "Vous ne pouvez pas modifier ce ticket.")
        return redirect("feed")

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket modifié.")
            return redirect("feed")
        else:
            messages.error(request, "Corrigez les erreurs.")
    else:
        form = TicketForm(instance=ticket)

    return render(
        request, "reviews/modification-ticket.html", {"form": form, "ticket": ticket}
    )


def modifierCritique(request):
    return render(request, "reviews/modification-critique.html")
