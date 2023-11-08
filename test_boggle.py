from boggle import Boggle

# Initialize the Boggle game
boggle_game = Boggle()

# Create a sample Boggle board
sample_board = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'J'],
    ['K', 'L', 'M', 'N', 'O'],
    ['P', 'Q', 'R', 'S', 'T'],
    ['U', 'V', 'W', 'X', 'Y']
]

# Test the Boggle game logic
guess = "HELLO"  # Replace with the word you want to test
result = boggle_game.check_valid_word(sample_board, guess)

print(f"Result for '{guess}': {result}")
