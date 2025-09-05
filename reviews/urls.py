from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Accueil -> feed
    path("", views.feed_view, name="feed"),
    # Auth simples (templates statiques pour l'instant)
    path("signup/", views.signup_view, name="signup"),
    path(
        "accueil/",
        auth_views.LoginView.as_view(template_name="reviews/accueil.html"),
        name="accueil",
    ),
    path("logout/", views.logout_view, name="logout"),
    # Préviews des autres pages/templates
    # Création de review -> accessible uniquement via /new/review_create/
    path("new/review_create/", views.review_create_view, name="review_create"),
    path("tickets/new/", views.ticket_create_view, name="ticket_create"),
    path(
        "tickets/review/new/",
        views.ticket_review_create_view,
        name="ticket_review_create",
    ),
    path("abonnements/", views.abonnements, name="abonnements"),
    path("mesposts/", views.mypost, name="mesposts"),
    path("modification-ticket/", views.modifierTicket, name="modification-ticket"),
    path(
        "modification-critique/", views.modifierCritique, name="modification-critique"
    ),
]
