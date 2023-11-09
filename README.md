# Boggle Game

## Overview

Boggle is a word game where players attempt to find words in sequences

- of adjacent letters on a rectangular grid of lettered dice.
- This web application allows users to play the Boggle game online.

## Features

- Generate a random Boggle board.
- Validate user-inputted words against the generated board.
- Keep track of the user's score.
- Display the highest score achieved.

## Technologies Used

- Python
- Flask
- JavaScript
- jQuery
- Axios

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/samiesmilz/flask-boggle.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

   Visit [http://localhost:5000](http://localhost:5000) in your browser to play the game.

## How to Play

1. Access the game in your browser.
2. The Boggle board is displayed on the home page.
3. Find words by typing them into the input field.
4. Submit your word to check its validity.
5. The game will display the result and update your score.
6. The highest score achieved is shown on the page.

## File Structure

- `app.py`: Flask application containing routes and game logic.
- `boggle.py`: Utilities for the Boggle game, including board generation and word validation.
- `static/`: Static files including CSS and JavaScript.
- `templates/`: HTML templates for the web application.

## Dependencies

- Flask
- jQuery
- Axios

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to contribute or report issues.
Happy playing!
