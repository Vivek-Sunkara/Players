from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Player, Team, Creator
from .forms import TeamForm, PlayerForm, CreatorForm
from .utils import optimize_team


def player_form(request, unique_link):
    """
    Displays the player form for a specific team.
    The unique link is also displayed on the page.
    """
    team = get_object_or_404(Team, unique_link=unique_link)
    players = Player.objects.filter(team=team)

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team
            player.save()
            return redirect(reverse('player_form', kwargs={'unique_link': unique_link}))

    else:
        form = PlayerForm()

    return render(
        request,
        'player_form.html',
        {
            'form': form,
            'players': players,
            'creator': team.creator,
            'unique_link': request.build_absolute_uri(reverse('player_form', kwargs={'unique_link': unique_link})),
        }
    )


@login_required
def create_team_view(request):
    """
    Handles team creation and generates a unique link for inviting players.
    """
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user
            team.save()

            # Ensure creator is linked correctly
            creator, created = Creator.objects.get_or_create(user=request.user, defaults={'name': request.user.username})

            unique_link = request.build_absolute_uri(reverse('player_form', kwargs={'unique_link': team.unique_link}))

            return render(request, 'team_success.html', {'team': team, 'unique_link': unique_link})

    else:
        form = TeamForm()

    return render(request, 'create_team.html', {'form': form})


@login_required
def add_players(request, team_id):
    """
    Allows users to add players to a specific team.
    """
    team = get_object_or_404(Team, id=team_id, creator=request.user)

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team
            player.creator = request.user
            player.save()
            return redirect(reverse('add_players', kwargs={'team_id': team.id}))

    else:
        form = PlayerForm()

    players = Player.objects.filter(team=team)

    # Generate the unique link for the team
    unique_link = request.build_absolute_uri(reverse('player_form', kwargs={'unique_link': team.unique_link}))

    return render(
        request,
        'add_players.html',
        {
            'form': form,
            'players': players,
            'team': team,
            'unique_link': unique_link,  # Pass the unique link to the template context
        }
    )


def player_form_view(request, unique_link):
    """
    Displays the player form for a specific Creator.
    """
    creator = get_object_or_404(Creator, unique_link=unique_link)
    players = Player.objects.filter(creator=creator)

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.creator = creator
            player.save()
            return redirect(reverse('player_form_view', kwargs={'unique_link': unique_link}))

    else:
        form = PlayerForm()

    return render(request, 'player_form.html', {'form': form, 'creator': creator, 'players': players})


@login_required
def optimize_team_view(request, creator_id):
    """
    Optimizes team formation for a given creator.
    """
    creator = get_object_or_404(Creator, id=creator_id)
    optimized_team = optimize_team(creator)
    return render(request, 'team_display.html', {'team': optimized_team})


@login_required
def create_team(request):
    """
    Handles team creation and redirects users to add players.
    """
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user
            team.save()
            return redirect(reverse('add_players', kwargs={'team_id': team.id}))

    else:
        form = TeamForm()

    return render(request, 'create_team.html', {'form': form})


def home(request):
    """
    Renders the home page.
    """
    return render(request, 'home.html', {'name': 'Raju'})


@login_required
def profile_view(request):
    """
    Displays the profile page with all players belonging to the logged-in user's team.
    """
    players = Player.objects.filter(team__creator=request.user)
    return render(request, 'profile.html', {'players': players})


def player_detail_view(request, player_id):
    """
    Displays details of a specific player.
    """
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'player_detail.html', {'player': player})


def register(request):
    """
    Handles user registration and redirects to the profile page upon successful sign-up.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('profile'))

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})