import streamlit as st
import psycopg2
import pandas as pd

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname='votes_e29f',
    user='votes_e29f_user',
    password='OyKZT8cTOkwF0EdmVmxSg2Zu5tGBj8O6',
    host='dpg-cr6p3pd6l47c7397q0qg-a',
    port='5432'
)
cursor = conn.cursor()

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 0
    st.session_state.registration_number = ""
    st.session_state.votes = {
        "President": None,
        "Secretary": None,
        "Vice President": None,
        "Assistant Secretary": None
    }
    st.session_state.has_voted = False

# Function to check if the registration number has already voted
def has_voted(registration_number):
    query = "SELECT COUNT(*) FROM votes WHERE registration_number = %s"
    cursor.execute(query, (registration_number,))
    count = cursor.fetchone()[0]
    return count > 0

# Define candidate lists
candidates = {
    "President": ["Candidate A", "Candidate B", "Candidate C"],
    "Secretary": ["Candidate D", "Candidate E"],
    "Vice President": ["Candidate F", "Candidate G", "Candidate H"],
    "Assistant Secretary": ["Candidate I", "Candidate J"]
}

# Page Navigation
if st.session_state.page == 0:
    st.title("Welcome to College Voting")
    st.session_state.registration_number = st.text_input("Enter your Registration Number")

    if st.button("Next"):
        if st.session_state.registration_number:
            if has_voted(st.session_state.registration_number):
                st.session_state.has_voted = True
                st.session_state.page = 1
            else:
                st.session_state.page = 1

elif st.session_state.page == 1:
    if st.session_state.has_voted:
        st.title("Already Voted")
        st.write("You have already voted. You cannot vote again.")
    else:
        st.title("Vote for President")
        st.session_state.votes["President"] = st.radio("Select a candidate", candidates["President"])

        if st.button("Next"):
            st.session_state.page = 2

elif st.session_state.page == 2:
    if st.session_state.has_voted:
        st.title("Already Voted")
        st.write("You have already voted. You cannot vote again.")
    else:
        st.title("Vote for Secretary")
        st.session_state.votes["Secretary"] = st.radio("Select a candidate", candidates["Secretary"])

        if st.button("Next"):
            st.session_state.page = 3

elif st.session_state.page == 3:
    if st.session_state.has_voted:
        st.title("Already Voted")
        st.write("You have already voted. You cannot vote again.")
    else:
        st.title("Vote for Vice President")
        st.session_state.votes["Vice President"] = st.radio("Select a candidate", candidates["Vice President"])

        if st.button("Next"):
            st.session_state.page = 4

elif st.session_state.page == 4:
    if st.session_state.has_voted:
        st.title("Already Voted")
        st.write("You have already voted. You cannot vote again.")
    else:
        st.title("Vote for Assistant Secretary")
        st.session_state.votes["Assistant Secretary"] = st.radio("Select a candidate", candidates["Assistant Secretary"])

        if st.button("Submit"):
            st.session_state.page = 5

            # Save votes to the database
            for position, candidate in st.session_state.votes.items():
                cursor.execute(
                    "INSERT INTO votes (registration_number, position, candidate) VALUES (%s, %s, %s)",
                    (st.session_state.registration_number, position, candidate)
                )
            conn.commit()

elif st.session_state.page == 5:
    st.title("Thank You for Voting!")
    st.write("Your votes have been submitted successfully.")
    st.write("Registration Number:", st.session_state.registration_number)
    st.write("Your Votes:", st.session_state.votes)
    
    if st.button("Done"):
        # Reset session state to allow new voter input
        st.session_state.page = 0
        st.session_state.registration_number = ""
        st.session_state.votes = {
            "President": None,
            "Secretary": None,
            "Vice President": None,
            "Assistant Secretary": None
        }
        st.session_state.has_voted = False

conn.close()
