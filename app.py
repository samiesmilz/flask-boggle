from boggle import Boggle
from flask import Flask, session, redirect, render_template, flash, request, jsonify

boggle_game = Boggle()
app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "mk7638"


@app.route("/")
def homepage():
    """ Create and display the board on homepade """
    session['board'] = boggle_game.make_board()
    session["points"] = 0
    session["no_of_plays"] = session.get("no_of_plays", 0)
    session['score'] = session.get("score", 0)

    # Reset the list of guessed words for a new game
    session["guessed_words"] = []

    return render_template("/index.html")


@app.route("/check-guess", methods=["POST"])
def check_guess():
    """To verify if the word is valid and on the board."""
    guess = request.json.get("guess")
    board = session.get("board")
    guessed_words = session.get("guessed_words", [])

    # Check if the word has already been guessed
    if guess in guessed_words:
        return jsonify({"result": "You've already guessed this word!"})

    # Check if the word is a valid word in the dictionary
    if guess in boggle_game.words:
        # Check if the word is valid on the board
        result = boggle_game.check_valid_word(board, guess)
        if result == 'ok':
            session["points"] = session.get('points', 0) + len(guess)
            session["guessed_words"] = guessed_words + \
                [guess]  # Add the guessed word to the list
            points = session["points"]
            return jsonify({"result": "Congrats - You got it right!", "points": points})
        else:
            return jsonify({"result": "Your guess is not on the board!"})

    return jsonify({"result": "Not a word!"})


@app.route("/post-score", methods=["POST"])
def post_score():
    """ Storing and updating score values """
    highest_score = 0
    score = int(request.json.get("score"))
    session["no_of_plays"] = session.get("no_of_plays") + 1

    if score > session['score']:
        highest_score = score
        session['score'] = score

    else:
        highest_score = session["score"]

    no_of_plays = session.get("no_of_plays")
    return jsonify({"score": highest_score, "no_of_plays": no_of_plays})


@app.route("/get-hint")
def get_hint():
    """Provide a hint for the current board."""
    board = session.get("board")
    guessed_words = session.get("guessed_words", [])

    # Find the first unused word on the board
    unused_words = [
        word for word in boggle_game.words if word not in guessed_words]
    hint_word = next((word for word in unused_words if boggle_game.check_valid_word(
        board, word) == "ok"), None)

    if hint_word:
        # Find the coordinates of the entire word
        coordinates = []
        for y in range(len(board)):
            for x in range(len(board[y])):
                if boggle_game.find_from(board, hint_word, y, x, seen=set()):
                    for i in range(len(hint_word)):
                        coordinates.append((y + i, x + i))
        return jsonify({"hint": hint_word, "coordinates": coordinates})
    else:
        return jsonify({"hint": "No more hints available."})
