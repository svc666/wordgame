import random
import streamlit as st
from prettytable import PrettyTable

# A larger static list of words (can be expanded)
words_list = [
    "apple", "banana", "grape", "orange", "kiwi", "peach", "berry", "melon",
    "pear", "fig", "date", "plum", "lime", "lemon", "cherry", "citrus",
    "mango", "apricot", "papaya", "dragonfruit", "watermelon", "strawberry",
    "raspberry", "blueberry", "coconut", "pomegranate", "kiwifruit", 
    "tangerine", "persimmon", "blackberry", "cantaloupe", "nectarine",
    "clementine", "bloodorange", "jackfruit", "starfruit", "currant", 
    "hazelnut", "chestnut", "walnut", "almond", "pecan", "pumpkin", 
    "zucchini", "eggplant", "carrot", "radish", "beet", "celery", 
    "asparagus", "spinach", "broccoli", "cauliflower", "tomato"
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
st.title("🎉 Word Guessing Game 🎉")
st.markdown(
    """
    <style>
    .big-font {
        font-size:30px !important;
        color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

num_letters = st.sidebar.selectbox("Choose the number of letters (2 to 8):", range(2, 9))

if st.button("Start Game"):
    word_to_guess = random.choice(get_words_by_length(num_letters))

    first_letter = word_to_guess[0]
    attempts = 3  # Number of attempts allowed
    st.write(f"🔤 The word starts with **'{first_letter}'** and has **{num_letters} letters**.")

    for attempt in range(attempts):
        guess = st.text_input(f"Attempt {attempt + 1}: You have {attempts - attempt} attempts left. Guess the word:", "")
        
        if guess:
            if guess == word_to_guess:
                st.success("🎉 Congratulations! You guessed the word!")
                correct_words.append(word_to_guess)
                break
            elif guess.startswith(first_letter):
                st.warning("🔑 You got the first letter right! Keep trying...")
            else:
                st.error("❌ Incorrect guess, try again.")

            if attempt == attempts - 1:
                st.error(f"😢 Sorry, the correct word was: **{word_to_guess}**")

    # Display the correct words table
    st.subheader("📝 Correctly Guessed Words:")
    st.text(display_correct_words())

if st.button("Reset Game"):
    correct_words.clear()
    st.success("🔄 Game has been reset.")

# Save option
if st.button("Save Words"):
    with open("correct_words.txt", "w") as f:
        for word in correct_words:
            f.write(word + "\n")
    st.success("✅ Correct words saved to correct_words.txt!")
