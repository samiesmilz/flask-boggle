from unittest import TestCase
from app import app
from flask import session, json, jsonify
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True

    def test_homepage(self):
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)

            self.assertIn(
                '<button class="guess" id="submit-btn">Submit</button>', html)

            # Testing session data
            self.assertIn('board', session)
            self.assertIn('points', session)
            self.assertIn('no_of_plays', session)
            self.assertIn('score', session)
            self.assertIn('guessed_words', session)

    def test_check_guess_valid(self):
        with app.test_client() as client:
            # Assuming "cat" is a valid word on the board
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T"],
                                 ["C", "A", "T"],
                                 ["C", "A", "T"]]
                sess['guessed_words'] = []

            response = client.post('/check-guess', json={'guess': 'cat'})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['result'], 'Congrats - You got it right!')

            # Test session values after a valid guess
            self.assertEqual(session.get('points'), len('cat'))
            self.assertEqual(session.get('guessed_words'), ['cat'])

    def test_check_guess_invalid_word(self):
        with app.test_client() as client:
            # Assuming "xyz" is not a valid word
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T"],
                                 ["C", "A", "T"],
                                 ["C", "A", "T"]]
                sess['guessed_words'] = []

            response = client.post('/check-guess', json={'guess': 'xyz'})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['result'], 'Not a word!')

    def test_check_guess_already_guessed(self):
        with app.test_client() as client:
            # Assuming "dog" is already guessed
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T"],
                                 ["C", "A", "T"],
                                 ["C", "A", "T"]]
                sess['guessed_words'] = ['dog']

            response = client.post('/check-guess', json={'guess': 'dog'})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                data['result'], "You've already guessed this word!")
