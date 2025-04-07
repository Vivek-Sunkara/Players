from django.shortcuts import render, redirect
from django.http import HttpResponse
from scipy.optimize import linprog
import uuid

# ===================== AUTHENTICATION =====================

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = request.session.get('users', {})

        if username in users:
            return HttpResponse("Username already exists.")

        users[username] = password
        request.session['users'] = users
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = request.session.get('users', {})

        if username in users and users[username] == password:
            request.session['logged_in'] = True
            request.session['username'] = username
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials.")
    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')

# ===================== CREATOR FORM =====================

def creator_form(request):
    if not request.session.get('logged_in'):
        return redirect('login')

    if request.method == 'POST':
        session_id = 'session-' + str(uuid.uuid4())
        request.session['current_session_id'] = session_id
        request.session[session_id] = {
            'created_by': request.session['username'],
            'role_requirements': {
                'bowlers': int(request.POST.get('bowlers')),
                'batsmen': int(request.POST.get('batsmen')),
                'allrounders': int(request.POST.get('allrounders')),
            },
            'players': [],
            'final_team': []
        }
        return redirect('add_player', session_id=session_id)

    return render(request, 'creatorform.html')


# ===================== ADD PLAYER =====================

def add_player(request, session_id):
    if session_id not in request.session:
        return HttpResponse("Invalid session.")

    if request.method == 'POST':
        player = {
            'name': request.POST.get('name'),
            'age': int(request.POST.get('age')),
            'role': request.POST.get('role'),
            'strike_rate': float(request.POST.get('strike_rate')),
            'wickets': int(request.POST.get('wickets')),
            'matches': int(request.POST.get('matches')),
            'total_score': int(request.POST.get('total_score')),
            'high_score': int(request.POST.get('high_score'))
        }

        session_data = request.session[session_id]
        session_data['players'].append(player)
        request.session[session_id] = session_data

    players = request.session[session_id]['players']
    return render(request, 'addplayer.html', {'session_id': session_id, 'players': players})


# ===================== GENERATE TEAM =====================

def generate_team(request, session_id):
    if not request.session.get('logged_in'):
        return redirect('login')

    data = request.session.get(session_id, {})
    players = data.get('players', [])
    requirements = data.get('role_requirements', {})

    if not players or not requirements:
        return HttpResponse("Missing data.")

    def compute_skill(p):
        return (p['strike_rate'] * 0.2 + p['wickets'] * 0.3 +
                p['matches'] * 0.1 + p['total_score'] * 0.3 +
                p['high_score'] * 0.1)

    skills = [compute_skill(p) for p in players]
    n = len(players)
    c = [-s for s in skills]

    A_eq = [
        [1 if p['role'] == 'bowler' else 0 for p in players],
        [1 if p['role'] == 'batsman' else 0 for p in players],
        [1 if p['role'] == 'allrounder' else 0 for p in players],
    ]
    b_eq = [
        requirements.get('bowlers', 0),
        requirements.get('batsmen', 0),
        requirements.get('allrounders', 0),
    ]
    bounds = [(0, 1) for _ in range(n)]

    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    selected_players = []
    if res.success:
        for i, val in enumerate(res.x):
            if val > 0.99:
                selected_players.append(players[i])
    else:
        return HttpResponse("No valid team found. Please check inputs.")

    data['final_team'] = selected_players
    request.session[session_id] = data

    return render(request, 'team.html', {'team': selected_players})


# ===================== HOME PAGE =====================

def home_view(request):
    if not request.session.get('logged_in'):
        return redirect('login')

    username = request.session.get('username')
    all_session_keys = list(request.session.keys())

    previous_teams = []
    unique_players = []
    seen_players = set()

    for key in all_session_keys:
        if key.startswith('session-') and request.session[key].get('created_by') == username:
            session_data = request.session[key]
            players = session_data.get('players', [])
            unique_for_this_team = []

            for p in players:
                player_key = (p['name'], p['age'], p['role'])
                if player_key not in seen_players:
                    seen_players.add(player_key)
                    unique_players.append(p)
                unique_for_this_team.append(p)

            previous_teams.append({
                'session_id': key,
                'requirements': session_data.get('role_requirements'),
                'players': unique_for_this_team,
                'final_team': session_data.get('final_team', [])
            })

    return render(request, 'home.html', {
        'username': username,
        'previous_teams': previous_teams,
        'unique_players': unique_players
    })
def base_page(request):
    return render(request, 'base.html')
