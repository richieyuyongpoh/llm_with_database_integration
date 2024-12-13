

import streamlit as st
import pandas as pd
import sqlite3
import openai 
import re

openai.api_key = st.secrets["OPENAI_API_KEY"]


# --- Part 1: Schema Upload and SQL Generation ---

st.title("LLM-Powered Chatbot with Database Integration")

# Checkbox for demo information
if st.checkbox("Show Demo Information"):
    st.write(
        """
        This app demonstrates a simple demo on LLM with database integration. 
        It uses a schema provided by [Ankit Kumar](https://github.com/ankittkp/Bank-Database-Design). 
        The database is created using dummy data. Only a few entries are inserted in the database.

        **Example Queries:**

        1. List all branches
        2. List count of customer from different branches
        3. What is the branch with the highest count of customers 
        """
    )

# Optional user name input
user_name = st.text_input("Your Name (optional):")

# File upload for database schema (text file)
uploaded_file = st.file_uploader("Upload Database Schema (Text):", type="txt")

if uploaded_file is not None:
    # Read the schema from the uploaded text file
    schema = uploaded_file.read().decode("utf-8") 
  #  st.write("Uploaded Schema:")
  #  st.text(schema)  # Display the schema as text

    # User query input
    user_query = st.text_input("Ask a question about your data:")

    if user_query:
        # Generate SQL code using GPT-4o-mini
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that generates SQLITE SQL code based on user queries and database schemas.Strictly SQlite codes only. No description"},
                {"role": "user", "content": f"Schema:\n{schema}\n\nQuery: {user_query}"}
            ]
        )
        
        generated_sql = response.choices[0].message.content
        clean_sql = re.sub(r"```sql\s*(.*?)\s*```", r"\1", generated_sql)

        st.code(clean_sql, language="sql")
        
        st.write("Copy and paste the SQL code below to execute and get the answer.")

# --- Part 2: SQL Execution and Response ---

    # SQL code input (for user to paste the generated code)
    sql_code = st.text_area("Paste SQL Code Here:")

    if st.button("Execute SQL"):
        # Connect to the SQLite database 
        conn = sqlite3.connect('bank11.sqlite')
        cursor = conn.cursor()

        try:
            # Execute the SQL code
            cursor.execute(sql_code)
            results = cursor.fetchall()

            # Display the results
            st.write("Results:")
         #   st.dataframe(results)

            # Generate a response using GPT-4o-mini, optionally including the user's name
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a helpful AI assistant. {'Address the user as ' + user_name if user_name else ''}"},
                    {"role": "user", "content": f"SQL results:\n{results}\n\nAnswer the user's original query: {user_query}"}
                ]
            )
            # Display the chatbot's response
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error executing SQL: {e}")

        finally:
            # Close the database connection
            conn.close()
