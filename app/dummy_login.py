import streamlit as st
from streamlit_option_menu import option_menu

# --- Dummy User Credentials ---
USER_CREDENTIALS = {"admin": "password123", "user1": "userpass"}

# --- Login Page ---
def login():
    st.title("Login Page")
    with st.form("Login Form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password!")

# --- Page 1 ---
def page1():
    st.title("Page 1: Dashboard")
    st.write("Welcome to the Dashboard!")

# --- Page 2 ---
def page2():
    st.title("Page 2: Profile")
    st.write(f"Welcome, {st.session_state.get('username', 'Guest')}!")
    st.write("This is your profile page.")

# --- Page 3 ---
def page3():
    st.title("Page 3: Settings")
    st.write("Here you can change your settings.")

# --- Main App ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()
    else:
        # Sidebar Navigation
        with st.sidebar:
            choice = option_menu(
                menu_title="Navigation",
                options=["Dashboard", "Profile", "Settings", "Logout"],
                icons=["house", "person", "gear", "box-arrow-left"],
                menu_icon="cast",
                default_index=0,
            )
        
        # Route to Selected Page
        if choice == "Dashboard":
            page1()
        elif choice == "Profile":
            page2()
        elif choice == "Settings":
            page3()
        elif choice == "Logout":
            st.session_state['logged_in'] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
