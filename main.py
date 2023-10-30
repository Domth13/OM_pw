import streamlit as st
import os
import motor.motor_asyncio


# Get the MongoDB connection string from an environment variable
MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING")
SECURITY_CODE = os.environ.get("SECURITY_CODE")
USERNAME_INFO = """
Please use the following infos to create your username (use lowercase letters and write them in the same sequence without whitespace between.) \n
1. First letter of the first name of your mother (or the most important female reference person in your childhood):\n
2. First letter of the first name of your father (or the most important male reference person in your childhood):\n
3. First letter of your birthplace:\n
4. Birth month of your mother as number (or the most important female reference person in your childhood):\n
5. Birth year of your father (in this format yyyy) (or the most important male reference person in your childhood):\n

Example: hag061960
"""

async def fetch_user_passwords():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
        db = client["owlMentor"]  
        collection = db["user"]  

        cursor = collection.find()
        user_passwords = {}
        async for doc in cursor:
            user_passwords[doc["name"]] = doc["pwd"]
        
        return user_passwords
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {str(e)}")
        return None

async def main():
    st.title("OM Password App")

    st.markdown(USERNAME_INFO)

    username = st.text_input("Enter your username:")
    security_code = st.text_input("Enter your security code:")

    user_passwords = await fetch_user_passwords()
    
    if st.button("Retrieve Password"):
        if user_passwords is not None:
            if username in user_passwords and security_code == SECURITY_CODE:
                st.success(f"Your password is: {user_passwords[username]}")
            else:
                st.error("Invalid username or security code. Please try again.")
        else:
            st.error("Error fetching user data from MongoDB. Please try again later.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

