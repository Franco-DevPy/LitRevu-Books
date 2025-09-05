from django.shortcuts import render


def feed_view(request):
    return render(request, "reviews/feed.html")


def signup_view(request):

    return render(request, "reviews/signup.html")


def review_create_view(request):
    return render(request, "reviews/review_create.html")


def ticket_create_view(request):
    return render(request, "reviews/ticket_create.html")


def ticket_review_create_view(request):
    return render(request, "reviews/ticket_review_create.html")


def abonnements(request):
    return render(request, "reviews/abonnements.html")


def logout_view(request):
    return render(request, "reviews/logout.html")


def mypost(request):
    return render(request, "reviews/mesposts.html")


def modifierTicket(request):
    return render(request, "reviews/modification-ticket.html")


def modifierCritique(request):
    return render(request, "reviews/modification-critique.html")
