import requests
import json
from datetime import datetime, timezone

def all_games(date):
    request = 'http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date=' + date
    response = requests.get(request)
    games = response.json()

    games = games['dates'][0]['games']

    game_scores = []
    count = -1

    for x in games:

        zulu_game_time = x['gameDate']

        date = zulu_game_time.split('T')[0]
        time = zulu_game_time.split('T')[1].split('Z')[0]
        game_time = date + ' ' + time
        game_time = datetime.fromisoformat(game_time)
        game_time = game_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
        game_time = game_time.strftime('%I:%M %p')

        count = count + 1
        link = x['link']
        teams = x['teams']

        status = x['status']['abstractGameCode']

        away_team = teams['away']['team']['name']
        try:
            away_score = teams['away']['score']
        except:
            away_score = 0


        home_team = teams['home']['team']['name']
        try:
            home_score = teams['home']['score']
        except:
            home_score = 0

        if status == 'F':
            game_line = (away_team + ' ' +
                         str(away_score) +
                         ' - ' +
                         home_team + ' ' +
                         str(home_score) + ' ' +
                         'Final')
        if status == 'P':
            game_line = (away_team +
                         ' - ' +
                         home_team + ' ' +
                         '(' + game_time + ')')
        if status == 'L':
            game_line = (away_team + ' ' +
                         str(away_score) +
                         ' - ' +
                         home_team + ' ' +
                         str(home_score))

        game_info = {
            'status': status,
            'link': link,
            'away_team': away_team,
            'away_score': away_score,
            'home_team': home_team,
            'home_score': home_score,
            'game_line': game_line
        }

        game_scores.append(game_info)

    return game_scores


def live_game(link):
    game = requests.get('http://statsapi.mlb.com' + link)
    game_info = game.json()
    return game_info


def scoreboard(current_game):
    zulu_game_time = current_game['gameData']['datetime']['dateTime']

    date = zulu_game_time.split('T')[0]
    time = zulu_game_time.split('T')[1].split('Z')[0]
    game_time = date + ' ' + time
    game_time = datetime.fromisoformat(game_time)
    game_time = game_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
    game_time = game_time.strftime('%I:%M %p')

    status = current_game['gameData']['status']['detailedState']

    away_team = current_game['gameData']['teams']['away']['name']
    try:
        away_team_score = current_game['liveData']['linescore']['teams']['away']['runs']
    except:
        away_team_score = ' '
    away_wins = current_game['gameData']['teams']['away']['record']['leagueRecord']['wins']
    away_losses = current_game['gameData']['teams']['away']['record']['leagueRecord']['losses']
    away_record = str(away_wins) + '-' + str(away_losses)

    home_team = current_game['gameData']['teams']['home']['name']
    try:
        home_team_score = current_game['liveData']['linescore']['teams']['home']['runs']
    except:
        home_team_score = ' '
    home_wins = current_game['gameData']['teams']['home']['record']['leagueRecord']['wins']
    home_losses = current_game['gameData']['teams']['home']['record']['leagueRecord']['losses']
    home_record = str(home_wins) + '-' + str(home_losses)

    try:
        top_or_bottom = bool(current_game['liveData']['linescore']['isTopInning'])
        if top_or_bottom is True:
            t_o_b = 'Top'
        if top_or_bottom is False:
            t_o_b = 'Bottom'
    except:
        t_o_b = 'Top'
    try:
        inning = t_o_b + ' ' + str(current_game['liveData']['linescore']['currentInning'])
    except:
        inning = ' '
    try:
        outs = current_game['liveData']['linescore']['outs']
        balls = current_game['liveData']['linescore']['balls']
        strikes = current_game['liveData']['linescore']['strikes']

    except:
        outs = 0
        balls = 0
        strikes = 0

    current_game = {'away_team':
                        {'name':away_team,'score':away_team_score,'record':away_record},
                    'home_team':
                        {'name': home_team, 'score':home_team_score,'record':home_record},
                    'game_data':
                        {'inning':inning,
                         'outs': outs,
                         'balls': balls,
                         'strikes': strikes,
                         'start_time': game_time,
                         'game_status': status}
                    }

    return current_game


def score_by_inning(current_game):

    away_team_abb = current_game['gameData']['teams']['away']['abbreviation']
    away_team_hits = current_game['liveData']['boxscore']['teams']['away']['teamStats']['batting']['hits']
    away_team_runs = current_game['liveData']['boxscore']['teams']['away']['teamStats']['batting']['runs']
    away_team_errors = current_game['liveData']['boxscore']['teams']['away']['teamStats']['fielding']['errors']

    home_team_abb = current_game['gameData']['teams']['home']['abbreviation']
    home_team_hits = current_game['liveData']['boxscore']['teams']['home']['teamStats']['batting']['hits']
    home_team_runs = current_game['liveData']['boxscore']['teams']['home']['teamStats']['batting']['runs']
    home_team_errors = current_game['liveData']['boxscore']['teams']['home']['teamStats']['fielding']['errors']

    current_game['liveData']['linescore']
    inning_data = current_game['liveData']['linescore']['innings']

    box_score = {
        'home_team':{
            'abb': home_team_abb,
            'hits': home_team_hits,
            'runs': home_team_runs,
            'errors': home_team_errors
        },
        'away_team': {
            'abb': away_team_abb,
            'hits': away_team_hits,
            'runs': away_team_runs,
            'errors': away_team_errors
        },
        'inning_data':inning_data,
        'game_status': ' '
    }

    return box_score


def pitcher_hitter_matchup(current_game):

    bater_name = current_game['liveData']['plays']['currentPlay']['matchup']['batter']['fullName']
    bater_id = current_game['liveData']['plays']['currentPlay']['matchup']['batter']['id']
    full_bater_id = 'ID' + str(bater_id)
    try:
        average = current_game['liveData']['boxscore']['teams']['away']['players'][full_bater_id]['seasonStats']['batting']['avg']
    except:
        average = current_game['liveData']['boxscore']['teams']['home']['players'][full_bater_id]['seasonStats']['batting']['avg']

    pitcher_name = current_game['liveData']['plays']['currentPlay']['matchup']['pitcher']['fullName']
    pitcher_id = current_game['liveData']['plays']['currentPlay']['matchup']['pitcher']['id']
    full_pitcher_id = 'ID' + str(pitcher_id)
    try:
        era = current_game['liveData']['boxscore']['teams']['home']['players'][full_pitcher_id]['seasonStats']['pitching']['era']

    except:
        era = current_game['liveData']['boxscore']['teams']['away']['players'][full_pitcher_id]['seasonStats']['pitching']['era']

    try:
        on_1st = current_game['liveData']['linescore']['offense']['first']
        first = True
    except:
        first = False

    try:
        on_2nd = current_game['liveData']['linescore']['offense']['second']
        second = True
    except:
        second = False

    try:
        on_3rd = current_game['liveData']['linescore']['offense']['third']
        third = True
    except:
        third = False

    matchup = {
        'bater': {
            'name': bater_name,
            'id': bater_id,
            'average': average
        },
        'pitcher': {
            'name': pitcher_name,
             'id' : pitcher_id,
             'era': era
        },
        'on_base': {
            'first': first,
            'second': second,
            'third': third
        }
    }

    return matchup


def bating_order(current_game,is_top):

    if is_top is True:
        side = 'away'
    if is_top is False:
        side = 'home'

    bating_order = current_game['liveData']['boxscore']['teams'][side]['battingOrder']

    all_batters = []
    for x in bating_order:
        full_bater_id = 'ID' + str(x)
        name = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['person']['fullName']
        atbats = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting'][
            'atBats']
        runs = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting']['runs']
        hits = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting']['hits']
        rbi = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting']['rbi']
        walks = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting'][
            'baseOnBalls']
        hbp = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting'][
            'hitByPitch']
        intwalk = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting'][
            'intentionalWalks']
        sacsbunt = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting'][
            'sacBunts']
        sacfly = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting'][
            'sacFlies']
        hrs = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['stats']['batting']['homeRuns']


        position = current_game['liveData']['boxscore']['teams'][side]['players'][full_bater_id]['position']['abbreviation']


        total_walks = walks + hbp + intwalk

        ops = atbats - total_walks - sacsbunt - sacfly
        avg = str(hits) + '-' + str(ops)

        stats = {'name': name,
                 'stats':{
                     'at_bats': atbats,
                     'hits': hits,
                     'walks': total_walks,
                     'rbi': rbi,
                     'avg': avg,
                     'hrs': hrs,
                     'runs': runs,
                     'position': position
                 }
                 }
        all_batters.append(stats)

    return all_batters

def color_return(home_team, away_team, sport):
    file = sport + '_colors.conf'

    with open(file) as f:
        rgbs = [line.strip() for line in f]

    for x in rgbs:
        if home_team in x:
            if '_1' in x:
                home_color_1 = x.split('= ')[1]
        if home_team in x:
            if '_2' in x:
                home_color_2 = x.split('= ')[1]

        if away_team in x:
            if '_1' in x:
                away_color_1 = x.split('= ')[1]
        if away_team in x:
            if '_2' in x:
                away_color_2 = x.split('= ')[1]

    rgb_return = {home_team:
                      {'color_1': home_color_1,
                       'color_2': home_color_2},
                  away_team: {
                      'color_1': away_color_1,
                      'color_2': away_color_2}
                  }

    return rgb_return
