import streamlit as st
from http.cookies import SimpleCookie
import hashlib
import time

# === Helper Functions ===
def set_cookie(name, value, minutes=2):
    """Set a cookie with a specified expiry time in minutes."""
    expiration = time.time() + (minutes * 60)  # Chuyển đổi phút thành giây
    js_code = f"""
    <script>
    console.log("Setting cookie: {name}={value}");
    document.cookie = "{name}={value}; expires={time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(expiration))}; path=/";
    console.log("Cookie set successfully.");
    </script>
    """
    st.write(js_code, unsafe_allow_html=True)


def get_cookie(name):
    """Get the value of a specific cookie."""
    
    cookie = SimpleCookie()
    cookie.load(st.query_params.get("cookies", ""))
    return cookie[name].value if name in cookie else None

def delete_cookie(name):
    """Delete a cookie by setting its expiration date to the past."""
    st.write(f'<script>document.cookie = "{name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";</script>', unsafe_allow_html=True)

def hash_password(password):
    """Hash the password (for demo only, use a more secure method in production)."""
    return hashlib.sha256(password.encode()).hexdigest()

# === User Database (demo) ===
USER_DB = {"admin": hash_password("1234")}

# === App Logic ===
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_DB and USER_DB[username] == hash_password(password):
            # Set cookies and session state
            set_cookie("login_token", username)
            st.session_state["user"] = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def logout():
    if "user" in st.session_state:
        del st.session_state["user"]
    delete_cookie("login_token")
    st.success("Logged out!")
    st.rerun()

def main_app():
    st.title("Welcome to the App!")
    st.write(f"Hello, {st.session_state['user']}!")
    if st.button("Logout"):
        logout()

# === Check Login Status ===
if "user" not in st.session_state:
    # Check cookies
    user_from_cookie = get_cookie("login_token")
    st.write(user_from_cookie)
    if user_from_cookie:
        st.session_state["user"] = user_from_cookie
cookie_ps = st.query_params.get_all("cookies")
st.write(cookie_ps)       
# === App Entry Point ===
if "user" in st.session_state:
    main_app()
else:
    login()
