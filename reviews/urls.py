from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.feed_view, name="feed"),
    path("signup/", views.signup_view, name="signup"),
    path(
        "accueil/",
        auth_views.LoginView.as_view(template_name="reviews/accueil.html"),
        name="accueil",
    ),
    path("logout/", views.logout_view, name="logout"),
    path(
        "tickets/<int:ticket_id>/reviews/new/",
        views.review_create_view,
        name="review_create",
    ),
    path("tickets/new/", views.ticket_create_view, name="ticket_create"),
    path(
        "tickets/new-with-review/",
        views.ticket_review_create_view,
        name="ticket_review_create",
    ),
    path("abonnements/", views.abonnements, name="abonnements"),
    path("mesposts/", views.mypost, name="mesposts"),
    # Edition d'un ticket (une seule URL, évite duplication)
    path(
        "tickets/<int:ticket_id>/edit/",
        views.modifierTicket,
        name="modification-ticket",
    ),
    path("reviews/<int:review_id>/edit/", views.review_edit_view, name="review_edit"),
    # Alias pour compat retro (ancien nom francisé)
    path(
        "reviews/<int:review_id>/modifier/",
        views.review_edit_view,
        name="modification-critique",
    ),
    # Suppression sécurisée (POST uniquement)
    path(
        "tickets/<int:ticket_id>/delete/",
        views.ticket_delete_view,
        name="ticket_delete",
    ),
    path(
        "reviews/<int:review_id>/delete/",
        views.review_delete_view,
        name="review_delete",
    ),
]
