from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.uic import loadUi
import sys
from datetime import datetime, timezone
import time


import mlb_score as mlb

global home_style
global away_style


class mlb_home(QMainWindow):

    def __init__(self):
        super(mlb_home,self).__init__()
        self.setWindowTitle('Scoreboard')

        loadUi('GUIs/Baseball.ui',self)

        today = datetime.today().strftime('%m/%d/%Y')

        def game_picker():

            game_pick = self.pick_game.itemText(self.pick_game.currentIndex())
            for key in games:
                game_line_lookup = key['game_line']
                if game_pick == game_line_lookup:
                    global current_game_status
                    current_game_status = key['status']
                    game_id = key['link']
                    run(game_id)


        def run(game_id):

            #loop = True

            #while loop is True:

                #print(game_id)
                #QtCore.QCoreApplication.processEvents()
            current_game = mlb.live_game(game_id)
            scoreboard(current_game)
            time.sleep(30)
            print(game_id)



        def scoreboard(current_game):
            scoreboard_info = mlb.scoreboard(current_game)

            home_team = scoreboard_info['home_team']['name']
            home_score = scoreboard_info['home_team']['score']
            home_record = scoreboard_info['home_team']['record']
            self.home_team.setText(home_team + '\n' + home_record)
            self.home_score.setText(str(home_score))

            away_team = scoreboard_info['away_team']['name']
            away_score = scoreboard_info['away_team']['score']
            away_record = scoreboard_info['away_team']['record']
            self.away_team.setText(away_team + '\n' + away_record)
            self.away_score.setText(str(away_score))

            status = scoreboard_info['game_data']['game_status']
            start_time = scoreboard_info['game_data']['start_time']

            colors(home_team, away_team)

            if status == 'Final':
                inning = 'Final'
                inning_data(current_game)
                batter_matchup(current_game)
                batting_order(current_game)
                empty_2()
            if status == 'Warmup':
                inning = ('Warmup \n Start Time: ' + start_time)
                inning_data(current_game)
                batter_matchup(current_game)
                batting_order(current_game)
                empty_1()
                empty_2()

            if status == 'Pre-Game':
                inning = ('Pre-Game \n Start Time: ' + start_time)
                inning_data(current_game)
                batter_matchup(current_game)
                batting_order(current_game)
                empty_1()
                empty_2()

            if status == 'In Progress':
                empty_1()
                empty_2()
                inning = (scoreboard_info['game_data']['inning'])
                inning_data(current_game)
                batter_matchup(current_game)
                batting_order(current_game)
                board_line(scoreboard_info)

            if status == 'Delayed: Rain':
                empty_1()
                empty_2()
                inning = (scoreboard_info['game_data']['inning'] + '\n Rain Delay')
                inning_data(current_game)
                batter_matchup(current_game)
                batting_order(current_game)
                board_line(scoreboard_info)

            if status == 'Scheduled':
                empty_1()
                empty_2()
                inning = (status + '\n' + start_time)


            self.inning.setText(inning)
            self.home_team.setStyleSheet(home_style)
            self.home_score.setStyleSheet(home_style)
            self.away_team.setStyleSheet(away_style)
            self.away_score.setStyleSheet(away_style)


        def board_line(scoreboard_info):

            outs = scoreboard_info['game_data']['outs']
            strikes = scoreboard_info['game_data']['strikes']
            balls = scoreboard_info['game_data']['balls']
            if outs == 1:
                self.out_1.setStyleSheet('background-color: rgb(71, 61, 26)')
            if outs == 2:
                self.out_1.setStyleSheet('background-color: rgb(71, 61, 26)')
                self.out_2.setStyleSheet('background-color: rgb(71, 61, 26)')

            if balls == 1:
                self.ball_1.setStyleSheet('background-color: rgb(71, 61, 26)')
            if balls == 2:
                self.ball_1.setStyleSheet('background-color: rgb(71, 61, 26)')
                self.ball_2.setStyleSheet('background-color: rgb(71, 61, 26)')
            if balls == 3:
                self.ball_1.setStyleSheet('background-color: rgb(71, 61, 26)')
                self.ball_2.setStyleSheet('background-color: rgb(71, 61, 26)')
                self.ball_3.setStyleSheet('background-color: rgb(71, 61, 26)')

            if strikes == 1:
                self.strike_1.setStyleSheet('background-color: rgb(71, 61, 26)')
            if strikes == 2:
                self.strike_1.setStyleSheet('background-color: rgb(71, 61, 26)')
                self.strike_2.setStyleSheet('background-color: rgb(71, 61, 26)')


        def inning_data(current_game):

            inning_data = mlb.score_by_inning(current_game)

            home_team_abb = inning_data['home_team']['abb']
            home_team_hits = inning_data['home_team']['hits']
            home_team_runs = inning_data['home_team']['runs']
            home_team_errors = inning_data['home_team']['errors']

            self.home_board.setText(home_team_abb)
            self.home_runs.setText(str(home_team_runs))
            self.home_hits.setText(str(home_team_hits))
            self.home_errors.setText(str(home_team_errors))

            away_team_abb = inning_data['away_team']['abb']
            away_team_hits = inning_data['away_team']['hits']
            away_team_runs = inning_data['away_team']['runs']
            away_team_errors = inning_data['away_team']['errors']

            self.away_board.setText(away_team_abb)
            self.away_runs.setText(str(away_team_runs))
            self.away_hits.setText(str(away_team_hits))
            self.away_errors.setText(str(away_team_errors))

            for x in inning_data['inning_data']:
                try:
                    inning = x['num']
                    home_runs = x['home']['runs']
                    away_runs = x['away']['runs']

                    if inning == 1:
                        self.home_1.setText(str(home_runs))
                        self.away_1.setText(str(away_runs))

                    if inning == 2:
                        self.home_2.setText(str(home_runs))
                        self.away_2.setText(str(away_runs))

                    if inning == 3:
                        self.home_3.setText(str(home_runs))
                        self.away_3.setText(str(away_runs))

                    if inning == 4:
                        self.home_4.setText(str(home_runs))
                        self.away_4.setText(str(away_runs))

                    if inning == 5:
                        self.home_5.setText(str(home_runs))
                        self.away_5.setText(str(away_runs))

                    if inning == 6:
                        self.home_6.setText(str(home_runs))
                        self.away_6.setText(str(away_runs))

                    if inning == 7:
                        self.home_7.setText(str(home_runs))
                        self.away_7.setText(str(away_runs))

                    if inning == 8:
                        self.home_8.setText(str(home_runs))
                        self.away_8.setText(str(away_runs))

                    if inning == 9:
                        self.home_9.setText(str(home_runs))
                        self.away_9.setText(str(away_runs))

                except:
                    pass


        def batter_matchup(current_game):
            matchup = mlb.pitcher_hitter_matchup(current_game)

            batter_name = ('Hitter: ' +
                           matchup['bater']['name'] +
                           '\n' +
                           'AVG: ' + str(matchup['bater']['average']))

            self.batter_name.setText(str(batter_name))

            pitcher_name = ('Pitcher: ' +
                            matchup['pitcher']['name'] +
                            '\n' +
                            'ERA: ' + str(matchup['pitcher']['era']))

            self.pitcher_name.setText(str(pitcher_name))

            worked = False
            number = -1
            while worked is False:
                try:
                    action = current_game['liveData']['plays']['allPlays'][number]['result']['description']
                    self.last_action.setText(action)
                    worked = True
                except:
                    number = number - 1

            if matchup['on_base']['first'] is True:
                self.base_1.setStyleSheet('background-color: rgb(71, 61, 26)')
            if matchup['on_base']['second'] is True:
                self.base_2.setStyleSheet('background-color: rgb(71, 61, 26)')
            if matchup['on_base']['third'] is True:
                self.base_3.setStyleSheet('background-color: rgb(71, 61, 26)')


        def batting_order(current_game):

            top_or_bottom = bool(current_game['liveData']['linescore']['isTopInning'])

            order = mlb.bating_order(current_game,top_or_bottom)

            if top_or_bottom is True:
                style = away_style.replace('20pt','15pt')
                pitcher_style = home_style.replace('20pt','15pt')
            if top_or_bottom is False:
                style = home_style.replace('20pt','15pt')
                pitcher_style = away_style.replace('20pt','15pt')

            self.pitcher_name.setStyleSheet(pitcher_style)
            self.batter_name.setStyleSheet(style)
            self.inning.setStyleSheet(style)

            hhitter_1 = (order[0]['name'] +
                        '\n' +
                        order[0]['stats']['position']
                        )
            habs_1 = (order[0]['stats']['avg'])
            hruns_1 = (order[0]['stats']['runs'])
            hbb_1 = order[0]['stats']['walks']
            hhrs_1 = order[0]['stats']['hrs']

            self.hitter_1.setText(hhitter_1)
            self.abs_1.setText(habs_1)
            self.runs_1.setText(str(hruns_1))
            self.bb_1.setText(str(hbb_1))
            self.avg_1.setText(str(hhrs_1))

            self.hitter_1.setStyleSheet(style)
            self.abs_1.setStyleSheet(style)
            self.runs_1.setStyleSheet(style)
            self.bb_1.setStyleSheet(style)
            self.avg_1.setStyleSheet(style)

            hhitter_2 = (order[1]['name'] +
                        '\n' +
                        order[1]['stats']['position']
                         )
            habs_2 = (order[1]['stats']['avg'])
            hruns_2 = (order[1]['stats']['runs'])
            hbb_2 = order[1]['stats']['walks']
            hhrs_2 = order[1]['stats']['hrs']

            self.hitter_2.setText(hhitter_2)
            self.abs_2.setText(habs_2)
            self.runs_2.setText(str(hruns_2))
            self.bb_2.setText(str(hbb_2))
            self.avg_2.setText(str(hhrs_2))

            self.hitter_2.setStyleSheet(style)
            self.abs_2.setStyleSheet(style)
            self.runs_2.setStyleSheet(style)
            self.bb_2.setStyleSheet(style)
            self.avg_2.setStyleSheet(style)

            hhitter_3 = (order[2]['name'] +
                        '\n' +
                        order[2]['stats']['position']
                        )
            habs_3 = (order[2]['stats']['avg'])
            hruns_3 = (order[2]['stats']['runs'])
            hbb_3 = order[2]['stats']['walks']
            hhrs_3 = order[2]['stats']['hrs']

            self.hitter_3.setText(hhitter_3)
            self.abs_3.setText(habs_3)
            self.runs_3.setText(str(hruns_3))
            self.bb_3.setText(str(hbb_3))
            self.avg_3.setText(str(hhrs_3))

            self.hitter_3.setStyleSheet(style)
            self.abs_3.setStyleSheet(style)
            self.runs_3.setStyleSheet(style)
            self.bb_3.setStyleSheet(style)
            self.avg_3.setStyleSheet(style)

            hhitter_4 = (order[3]['name'] +
                        '\n' +
                        order[3]['stats']['position']
                        )
            habs_4 = (order[3]['stats']['avg'])
            hruns_4 = (order[3]['stats']['runs'])
            hbb_4 = order[3]['stats']['walks']
            hhrs_4 = order[3]['stats']['hrs']

            self.hitter_4.setText(hhitter_4)
            self.abs_4.setText(habs_4)
            self.runs_4.setText(str(hruns_4))
            self.bb_4.setText(str(hbb_4))
            self.avg_4.setText(str(hhrs_4))

            self.hitter_4.setStyleSheet(style)
            self.abs_4.setStyleSheet(style)
            self.runs_4.setStyleSheet(style)
            self.bb_4.setStyleSheet(style)
            self.avg_4.setStyleSheet(style)

            hhitter_5 = (order[4]['name'] +
                        '\n' +
                        order[4]['stats']['position']
                        )
            habs_5 = (order[4]['stats']['avg'])
            hruns_5 = (order[4]['stats']['runs'])
            hbb_5 = order[4]['stats']['walks']
            hhrs_5 = order[4]['stats']['hrs']

            self.hitter_5.setText(hhitter_5)
            self.abs_5.setText(habs_5)
            self.runs_5.setText(str(hruns_5))
            self.bb_5.setText(str(hbb_5))
            self.avg_5.setText(str(hhrs_5))

            self.hitter_5.setStyleSheet(style)
            self.abs_5.setStyleSheet(style)
            self.runs_5.setStyleSheet(style)
            self.bb_5.setStyleSheet(style)
            self.avg_5.setStyleSheet(style)

            hhitter_6 = (order[5]['name'] +
                        '\n' +
                        order[5]['stats']['position']
                        )
            habs_6 = (order[5]['stats']['avg'])
            hruns_6 = (order[5]['stats']['runs'])
            hbb_6 = order[5]['stats']['walks']
            hhrs_6 = order[5]['stats']['hrs']

            self.hitter_6.setText(hhitter_6)
            self.abs_6.setText(habs_6)
            self.runs_6.setText(str(hruns_6))
            self.bb_6.setText(str(hbb_6))
            self.avg_6.setText(str(hhrs_6))

            self.hitter_6.setStyleSheet(style)
            self.abs_6.setStyleSheet(style)
            self.runs_6.setStyleSheet(style)
            self.bb_6.setStyleSheet(style)
            self.avg_6.setStyleSheet(style)

            hhitter_7 = (order[6]['name'] +
                        '\n' +
                        order[6]['stats']['position']
                        )
            habs_7 = (order[6]['stats']['avg'])
            hruns_7 = (order[6]['stats']['runs'])
            hbb_7 = order[6]['stats']['walks']
            hhrs_7 = order[6]['stats']['hrs']

            self.hitter_7.setText(hhitter_7)
            self.abs_7.setText(habs_7)
            self.runs_7.setText(str(hruns_7))
            self.bb_7.setText(str(hbb_7))
            self.avg_7.setText(str(hhrs_7))

            self.hitter_7.setStyleSheet(style)
            self.abs_7.setStyleSheet(style)
            self.runs_7.setStyleSheet(style)
            self.bb_7.setStyleSheet(style)
            self.avg_7.setStyleSheet(style)

            hhitter_8 = (order[7]['name'] +
                        '\n' +
                        order[7]['stats']['position']
                        )
            habs_8 = (order[7]['stats']['avg'])
            hruns_8 = (order[7]['stats']['runs'])
            hbb_8 = order[7]['stats']['walks']
            hhrs_8 = order[7]['stats']['hrs']

            self.hitter_8.setText(hhitter_8)
            self.abs_8.setText(habs_8)
            self.runs_8.setText(str(hruns_8))
            self.bb_8.setText(str(hbb_8))
            self.avg_8.setText(str(hhrs_8))

            self.hitter_8.setStyleSheet(style)
            self.abs_8.setStyleSheet(style)
            self.runs_8.setStyleSheet(style)
            self.bb_8.setStyleSheet(style)
            self.avg_8.setStyleSheet(style)

            hhitter_9 = (order[8]['name'] +
                        '\n' +
                        order[8]['stats']['position']
                        )
            habs_9 = (order[8]['stats']['avg'])
            hruns_9 = (order[8]['stats']['runs'])
            hbb_9 = order[8]['stats']['walks']
            hhrs_9 = order[8]['stats']['hrs']

            self.hitter_9.setText(hhitter_9)
            self.abs_9.setText(habs_9)
            self.runs_9.setText(str(hruns_9))
            self.bb_9.setText(str(hbb_9))
            self.avg_9.setText(str(hhrs_9))

            self.hitter_9.setStyleSheet(style)
            self.abs_9.setStyleSheet(style)
            self.runs_9.setStyleSheet(style)
            self.bb_9.setStyleSheet(style)
            self.avg_9.setStyleSheet(style)


        def empty_1():
            style = str('font: 10pt "Team-Captain"; color: rgb(71, 61, 26); border-color: rgb(0, 0, 0); border-style:inset')
            text = ''

            self.last_action.setText(text)
            self.home_1.setText(text)
            self.away_1.setText(text)
            self.home_2.setText(text)
            self.away_2.setText(text)
            self.home_3.setText(text)
            self.away_3.setText(text)
            self.home_4.setText(text)
            self.away_4.setText(text)
            self.home_5.setText(text)
            self.away_5.setText(text)
            self.home_6.setText(text)
            self.away_6.setText(text)
            self.home_7.setText(text)
            self.away_7.setText(text)
            self.home_8.setText(text)
            self.away_8.setText(text)
            self.home_9.setText(text)
            self.away_9.setText(text)

            self.home_1.setStyleSheet(style)
            self.away_1.setStyleSheet(style)
            self.home_2.setStyleSheet(style)
            self.away_2.setStyleSheet(style)
            self.home_3.setStyleSheet(style)
            self.away_3.setStyleSheet(style)
            self.home_4.setStyleSheet(style)
            self.away_4.setStyleSheet(style)
            self.home_5.setStyleSheet(style)
            self.away_5.setStyleSheet(style)
            self.home_6.setStyleSheet(style)
            self.away_6.setStyleSheet(style)
            self.home_7.setStyleSheet(style)
            self.away_7.setStyleSheet(style)
            self.home_8.setStyleSheet(style)
            self.away_8.setStyleSheet(style)
            self.home_9.setStyleSheet(style)
            self.away_9.setStyleSheet(style)


            self.home_runs.setText(text)
            self.home_hits.setText(text)
            self.home_errors.setText(text)
            self.away_runs.setText(text)
            self.away_hits.setText(text)
            self.away_errors.setText(text)


        def empty_2():
            borders_style = str('border-color: rgb(71, 61, 26); border-width : 5px; border-style:inset;')

            self.out_1.setStyleSheet(borders_style)
            self.out_2.setStyleSheet(borders_style)

            self.ball_1.setStyleSheet(borders_style)
            self.ball_2.setStyleSheet(borders_style)
            self.ball_3.setStyleSheet(borders_style)

            self.strike_1.setStyleSheet(borders_style)
            self.strike_2.setStyleSheet(borders_style)

            self.base_1.setStyleSheet(borders_style)
            self.base_2.setStyleSheet(borders_style)
            self.base_3.setStyleSheet(borders_style)


        def colors(home_team, away_team):

            rgbs = mlb.color_return(home_team, away_team, 'mlb')

            home_rgb_1 = rgbs[home_team]['color_1']
            home_rgb_2 = rgbs[home_team]['color_2']
            away_rgb_1 = rgbs[away_team]['color_1']
            away_rgb_2 = rgbs[away_team]['color_2']

            global home_style
            global away_style
            home_style = ('background-color: ' + home_rgb_1 + '; color: ' + home_rgb_2 + ';font: 20pt "Team-Captain"; border-color: rgb(71, 61, 26); border-width : 5px; border-style:inset;')
            away_style = ('background-color: ' + away_rgb_1 + '; color: ' + away_rgb_2 + ';font: 20pt "Team-Captain"; border-color: rgb(71, 61, 26); border-width : 5px; border-style:inset;')


        def calendar_date():
            empty_1()
            empty_2()
            date = self.calendar.selectedDate()
            date = date.toString('MM/dd/yyyy')


            self.pick_game.clear()
            global all_game_lines, live_games, past_games, future_games, games

            games = mlb.all_games(date)
            all_game_lines = []
            live_games = []
            past_games = []
            future_games = []
            for key in games:
                game_line = key['game_line']
                if game_line not in all_game_lines:
                    if 'Yankee' in game_line:
                        all_game_lines.append(game_line)
                    elif 'Final' in game_line:
                        past_games.append(game_line)
                    elif ':' in game_line:
                        future_games.append(game_line)
                    else:
                        live_games.append(game_line)

            live_games.sort()
            past_games.sort()
            future_games.sort()
            all_game_lines.extend(live_games)
            all_game_lines.extend(future_games)
            all_game_lines.extend(past_games)

            self.pick_game.addItems(all_game_lines)


            game_picker()


        def today():

            today = datetime.today().strftime('%m/%d/%Y')
            empty_1()
            empty_2()

            self.pick_game.clear()
            global all_game_lines, live_games, past_games, future_games, games

            games = mlb.all_games(today)
            all_game_lines = []
            live_games = []
            past_games = []
            future_games = []
            for key in games:
                game_line = key['game_line']
                if game_line not in all_game_lines:
                    if 'Yankee' in game_line:
                        all_game_lines.append(game_line)
                    elif 'Final' in game_line:
                        past_games.append(game_line)
                    elif ':' in game_line:
                        future_games.append(game_line)
                    else:
                        live_games.append(game_line)

            live_games.sort()
            past_games.sort()
            future_games.sort()
            all_game_lines.extend(live_games)
            all_game_lines.extend(future_games)
            all_game_lines.extend(past_games)

            self.pick_game.addItems(all_game_lines)

            game_picker()


        self.pick_game.clear()
        self.go_to_game.clicked.connect(game_picker)
        self.go_to_date.clicked.connect(calendar_date)
        self.todays_game.clicked.connect(today)
        calendar_date()

if __name__ == "__main__":
    app=QApplication(sys.argv)
    mainwindow=mlb_home()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.show()
    app.exec_()