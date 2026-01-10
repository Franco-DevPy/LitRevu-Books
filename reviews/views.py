from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import TicketForm, ReviewForm, FollowForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (
    require_POST,
)
from django.contrib import messages

from .models import Ticket, Review, UserFollows
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import CharField, Value
from itertools import chain


@login_required
def feed_view(request):

    followed_ids = list(
        UserFollows.objects.filter(user=request.user, blocked=False).values_list(
            "followed_user_id", flat=True
        )
    )
    allowed_user_ids = followed_ids + [request.user.id]

    reviews = (
        Review.objects.filter(user_id__in=allowed_user_ids)
        .select_related("user", "ticket")
        .annotate(content_type=Value("REVIEW", CharField()))
    )

    tickets = (
        Ticket.objects.filter(user_id__in=allowed_user_ids)
        .select_related("user")
        .annotate(content_type=Value("TICKET", CharField()))
    )

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True,
    )

    user_reviewed_ticket_ids = set(
        Review.objects.filter(user=request.user).values_list("ticket_id", flat=True)
    )

    context = {
        "posts": posts,
        "user_reviewed_ticket_ids": user_reviewed_ticket_ids,
    }
    return render(request, "reviews/feed.html", context)


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            messages.success(request, "Compte créé. Vous êtes maintenant connecté.")
            login(request, user)
            return redirect("feed")
        else:

            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
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
            messages.success(request, "Ticket créé.")
            return redirect(reverse("feed"))
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = TicketForm()
    return render(request, "reviews/ticket_create.html", {"form": form})


@login_required
def abonnements(request):
    form = FollowForm()
    User = get_user_model()
    if request.method == "POST":
        action = request.POST.get("action")
        target_id = request.POST.get("target_id")

        if action == "follow":
            form = FollowForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"].strip()
                try:
                    target = User.objects.get(username__iexact=username)
                except User.DoesNotExist:
                    messages.error(request, "Utilisateur introuvable.")
                else:
                    if target == request.user:
                        messages.warning(
                            request, "Vous ne pouvez pas vous suivre vous-même."
                        )
                    else:
                        try:
                            rel, created = UserFollows.objects.get_or_create(
                                user=request.user,
                                followed_user=target,
                                defaults={"blocked": False},
                            )
                        except IntegrityError:
                            messages.error(request, "Relation déjà existante.")
                        else:
                            if not created and rel.blocked:
                                rel.blocked = False
                                rel.save()
                                messages.info(
                                    request, "Relation réactivée (déblocage)."
                                )
                            elif created:
                                messages.success(
                                    request,
                                    f"Vous suivez maintenant {target.username}.",
                                )
                            else:
                                messages.info(
                                    request, "Vous suivez déjà cet utilisateur."
                                )

        else:
            rel = None
            if target_id and target_id.isdigit():
                rel = UserFollows.objects.filter(
                    id=target_id, user=request.user
                ).first()

            if action in ("unfollow", "block", "unblock") and not rel:
                messages.error(request, "Relation introuvable.")
            else:
                if action == "unfollow":
                    rel.delete()
                    messages.success(request, "Vous ne suivez plus cet utilisateur.")
                elif action == "block":
                    rel.blocked = True
                    rel.save()
                    messages.success(
                        request,
                        "Utilisateur bloqué. Ses publications ne seront plus visibles.",
                    )
                elif action == "unblock":
                    rel.blocked = False
                    rel.save()
                    messages.success(request, "Utilisateur débloqué.")

        return redirect("abonnements")

    following_active = UserFollows.objects.filter(
        user=request.user, blocked=False
    ).select_related("followed_user")

    following_blocked = UserFollows.objects.filter(
        user=request.user, blocked=True
    ).select_related("followed_user")

    context = {
        "form": form,
        "following_active": following_active,
        "following_blocked": following_blocked,
    }
    return render(request, "reviews/abonnements.html", context)


def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return render(request, "reviews/logout.html")


@login_required
def mypost(request):
    """
    Mostrar los tickets y reviews del usuario conectado.
    """
    tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")

    reviews = (
        Review.objects.filter(user=request.user)
        .select_related("ticket")
        .order_by("-time_created")
    )

    reviewed_ticket_ids = set(reviews.values_list("ticket_id", flat=True))

    context = {
        "tickets": tickets,
        "reviews": reviews,
        "reviewed_ticket_ids": reviewed_ticket_ids,
    }
    return render(request, "reviews/mesposts.html", context)


@login_required
def modifierTicket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

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


@login_required
def review_edit_view(request, review_id):
    review = get_object_or_404(
        Review.objects.select_related("ticket", "user"), pk=review_id
    )
    if review.user != request.user:
        messages.error(request, "Vous ne pouvez pas modifier cette critique.")
        return redirect("feed")

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Critique mise à jour.")
            return redirect("feed")
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = ReviewForm(instance=review)

    context = {
        "form": form,
        "review": review,
        "ticket": review.ticket,
        "is_edit": True,
    }
    return render(request, "reviews/modification-critique.html", context)




@login_required
@require_POST
def ticket_delete_view(request, ticket_id):

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if ticket.user != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer ce ticket.")
        return redirect("mesposts")
    ticket.delete()
    messages.success(request, "Ticket supprimé.")
    return redirect("mesposts")


@login_required
@require_POST
def review_delete_view(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.user != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer cette critique.")
        return redirect("mesposts")
    review.delete()
    messages.success(request, "Critique supprimée.")
    return redirect("mesposts")


@login_required
def ticket_review_create_view(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES, prefix="ticket")
        review_form = ReviewForm(request.POST, prefix="review")
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            messages.success(request, "Ticket + critique créés.")
            return redirect("feed")
        else:
            messages.error(request, "Corrigez les erreurs des deux formulaires.")
    else:
        ticket_form = TicketForm(prefix="ticket")
        review_form = ReviewForm(prefix="review")

    return render(
        request,
        "reviews/ticket_review_create.html",
        {
            "ticket_form": ticket_form,
            "review_form": review_form,
        },
    )
