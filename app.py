import random
import streamlit as st
from prettytable import PrettyTable

# Static list of words for different lengths
words_list = [
    "go", "fig", "bat", "cat", "dog", "hat", "pen", "red", "tin", "van", "win", 
    "and", "the", "but", "for", "not", "are", "can", "you", "was", "all",
    "pear", "date", "grape", "melon", "lemon", "plum", "cherry", "berry", "ant", "ear", "fat"
]

# List to keep track of correctly guessed words
correct_words = []

def get_words_by_length(length):
    return [word for word in words_list if len(word) == length]

def display_correct_words():
    table = PrettyTable()
    table.field_names = ["Correctly Guessed Words"]
    
    for word in correct_words:
        table.add_row([word])
        
    return table

# Streamlit app
st.set_page_config(page_title="Word Guessing Game", layout="centered")

st.title("🎉 Word Guessing Game 🎉")
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f8;
    }
    .big-font {
        font-size:30px !important;
        color: #4CAF50;
    }
    .title {
        color: #1f78b4;
        font-size: 2em;
        text-align: center;
    }
    .attempt {
        font-weight: bold;
        color: #d9534f;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state variables
if "attempt" not in st.session_state:
    st.session_state.attempt = 0
if "word_to_guess" not in st.session_state:
    st.session_state.word_to_guess = None
if "first_letter" not in st.session_state:
    st.session_state.first_letter = ""
if "displayed_word" not in st.session_state:
    st.session_state.displayed_word = ""
if "previous_guesses" not in st.session_state:
    st.session_state.previous_guesses = set()

if "num_letters" not in st.session_state:
    st.session_state.num_letters = 3  # Default to 3-letter words

# Start new game
if st.button("Start Game"):
    num_letters = st.session_state.num_letters
    word_candidates = get_words_by_length(num_letters)
    
    if not word_candidates:
        st.error(f"No words found with {num_letters} letters.")
    else:
        st.session_state.word_to_guess = random.choice(word_candidates)
        st.session_state.first_letter = st.session_state.word_to_guess[0]
        st.session_state.attempt = 0
        st.session_state.displayed_word = st.session_state.first_letter + " _ " * (num_letters - 1)
        st.session_state.correct_guess = False
        st.session_state.previous_guesses.clear()

# Letter count selection
st.sidebar.subheader("Select Number of Letters")
num_letters = st.sidebar.selectbox("Choose the number of letters (2 to 8):", list(range(2, 9)), index=1)
st.session_state.num_letters = num_letters

# Display current game state
if st.session_state.word_to_guess:
    st.write(f"🔤 The word starts with **'{st.session_state.displayed_word.strip()}'** and has **{num_letters} letters**.")

    max_attempts = 2  # Set max attempts to 2 for all words

    if st.session_state.attempt < max_attempts:
        guess = st.text_input(f"Attempt {st.session_state.attempt + 1}: You have {max_attempts - st.session_state.attempt} attempts left. Guess the word:", "")

        if guess:
            if guess in st.session_state.previous_guesses:
                st.warning("🚫 You've already guessed that word! Try a different one.")
            else:
                st.session_state.previous_guesses.add(guess)
                
                if guess == st.session_state.word_to_guess:
                    st.success("🎉 Congratulations! You guessed the word!")
                    correct_words.append(st.session_state.word_to_guess)
                    st.session_state.correct_guess = True
                elif guess.startswith(st.session_state.first_letter):
                    st.warning("🔑 You got the first letter right! Keep trying...")
                else:
                    st.error("❌ Incorrect guess, try again.")
                
                # Increment attempts
                st.session_state.attempt += 1

                # If max attempts reached, reveal the correct word
                if st.session_state.attempt == max_attempts:
                    st.error(f"😢 Sorry, the correct word was: **{st.session_state.word_to_guess}**")
                    
                    # Change to a new word with a different starting letter
                    word_candidates = get_words_by_length(num_letters)
                    new_word_candidates = [word for word in word_candidates if word[0] != st.session_state.first_letter]
                    
                    if new_word_candidates:
                        st.session_state.word_to_guess = random.choice(new_word_candidates)
                        st.session_state.first_letter = st.session_state.word_to_guess[0]
                        st.session_state.displayed_word = st.session_state.first_letter + " _ " * (num_letters - 1)
                        st.session_state.attempt = 0  # Reset attempts for the new word
                    else:
                        st.error("No more words available.")
                else:
                    # Update displayed word
                    st.session_state.displayed_word = st.session_state.first_letter + " _ " * (num_letters - 1)

    # Display the correct words table
    st.subheader("📝 Correctly Guessed Words:")
    st.text(display_correct_words())

if st.button("Reset Game"):
    correct_words.clear()
    st.session_state.attempt = 0
    st.session_state.word_to_guess = None
    st.session_state.first_letter = ""
    st.session_state.displayed_word = ""
    st.session_state.correct_guess = False
    st.session_state.previous_guesses.clear()
    st.success("🔄 Game has been reset.")

# Save option
if st.button("Save Words"):
    with open("correct_words.txt", "w") as f:
        for word in correct_words:
            f.write(word + "\n")
    st.success("✅ Correct words saved to correct_words.txt!")
