from boggle import Boggle
from flask import Flask, session, redirect, render_template, flash, request, jsonify

boggle_game = Boggle()
app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "mk7638"


@app.route("/")
def homepage():
    # session['board'] = session.get('board', boggle_game.make_board())
    session['board'] = boggle_game.make_board()
    session["points"] = 0

    return render_template("/index.html")


@app.route("/check-guess", methods=["POST"])
def check_guess():
    guess = request.json.get("guess")
    board = session.get("board")

    # Check if the word is a valid word in the dictionary
    if guess in boggle_game.words:
        # Check if the word is valid on the board
        result = boggle_game.check_valid_word(board, guess)
        if result == 'ok':
            session["points"] = session.get('points', 0) + len(guess)
            points = session["points"]
            return jsonify({"result": "Congrats - You got it right!", "points": points})
        else:
            return jsonify({"result": "Your guess is not on the board!"})

    return jsonify({"result": "Not a word!"})
