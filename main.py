import streamlit as st
import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Get the MongoDB connection string and security code from environment variables
MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING")
SECURITY_CODE = os.environ.get("SECURITY_CODE")

# Username instructions
USERNAME_INFO = """
Please use the following information to create your username (use lowercase letters without whitespace):
1. First letter of the first name of your mother (or primary female reference in childhood):
2. First letter of the first name of your father (or primary male reference in childhood):
3. First letter of your birthplace:
4. Birth month of your mother as a number (01-12):
5. Birth year of your father in yyyy format:
Example: hag061960
"""

async def fetch_user_passwords():
    """Fetch all user passwords from MongoDB asynchronously."""
    try:
        client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
        db = client["owlMentor"]
        collection = db["user"]

        # Fetch user passwords from MongoDB
        cursor = collection.find()
        user_passwords = {}
        async for doc in cursor:
            user_passwords[doc["name"]] = doc["pwd"]

        return user_passwords
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {str(e)}")
        return None

def run_asyncio_fetch():
    """Helper function to run async fetch function in Streamlit."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_user_passwords())

def main():
    st.title("OM Password App")
    st.markdown(USERNAME_INFO)

    username = st.text_input("Enter your username:")
    security_code = st.text_input("Enter your security code:")

    if st.button("Retrieve Password"):
        user_passwords = run_asyncio_fetch()
        if user_passwords:
            if username in user_passwords and security_code == SECURITY_CODE:
                st.success(f"Your password is: {user_passwords[username]}")
            else:
                st.error("Invalid username or security code. Please try again.")
        else:
            st.error("Error fetching user data from MongoDB. Please try again later.")

if __name__ == "__main__":
    main()
