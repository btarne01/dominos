from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this to a random string


class DominoesGame:
    def __init__(self):
        self.rounds = ['12s', '11s', '10s', '9s', '8s', '7s', '6s', '5s', '4s', '3s', '2s', '1s', 'Blanks']

    def get_current_round_name(self, round_num):
        if round_num < len(self.rounds):
            return self.rounds[round_num]
        return "Game Complete"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        num_players = int(request.form['num_players'])
        players = []
        for i in range(num_players):
            player_name = request.form[f'player_{i}'].strip()
            if player_name:
                players.append(player_name)

        # Initialize game session
        session['players'] = players
        session['scores'] = {player: 0 for player in players}
        session['current_round'] = 0
        session['game_history'] = []

        return redirect(url_for('game'))

    return render_template('setup.html')


@app.route('/game')
def game():
    if 'players' not in session:
        return redirect(url_for('setup'))

    game = DominoesGame()
    current_round = session.get('current_round', 0)

    if current_round >= len(game.rounds):
        return redirect(url_for('final_results'))

    return render_template('game.html',
                           players=session['players'],
                           scores=session['scores'],
                           current_round=current_round,
                           round_name=game.get_current_round_name(current_round),
                           game_history=session.get('game_history', []))


@app.route('/submit_round', methods=['POST'])
def submit_round():
    if 'players' not in session:
        return redirect(url_for('setup'))

    winner = request.form['winner']
    players = session['players']
    current_round = session['current_round']

    # Record round results
    round_scores = {}
    for player in players:
        if player == winner:
            round_scores[player] = 0
        else:
            pips = int(request.form.get(f'pips_{player}', 0))
            round_scores[player] = pips
            session['scores'][player] += pips

    # Add to game history
    game = DominoesGame()
    round_info = {
        'round_num': current_round + 1,
        'round_name': game.get_current_round_name(current_round),
        'winner': winner,
        'scores': round_scores.copy()
    }

    if 'game_history' not in session:
        session['game_history'] = []
    session['game_history'].append(round_info)

    # Move to next round
    session['current_round'] = current_round + 1
    session.modified = True

    return redirect(url_for('game'))


@app.route('/final_results')
def final_results():
    if 'players' not in session:
        return redirect(url_for('setup'))

    # Sort players by score (lowest wins)
    players_scores = [(player, session['scores'][player]) for player in session['players']]
    players_scores.sort(key=lambda x: x[1])

    return render_template('final_results.html',
                           players_scores=players_scores,
                           game_history=session.get('game_history', []))


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)