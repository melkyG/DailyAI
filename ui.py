import streamlit as st

def show_outfit_suggestion(suggestion):
    st.title("AI Outfit Suggestion")
    st.write(suggestion)

if __name__ == "__main__":
    # For manual testing
    show_outfit_suggestion("It's sunny and warm. Wear a t-shirt and shorts!")
