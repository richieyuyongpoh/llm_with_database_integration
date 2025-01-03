

import streamlit as st
import pandas as pd
import sqlite3
from openai import OpenAI
import re


client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"],base_url="https://api.deepseek.com")

# --- Part 1: Schema Upload and SQL Generation ---

st.title("LLM-Powered Chatbot with Database Integration")

# Checkbox for demo information
if st.checkbox("Read Me"):
    st.write(
        """
        This app demonstrates a simple demo on LLM with database integration. 
        It uses a schema provided by [Ankit Kumar](https://github.com/ankittkp/Bank-Database-Design). 
        You may download a copy [HERE](https://drive.google.com/file/d/1scTV3Vq_qG6cRxmi4gYO_CtSispqc1gi/view?usp=sharing)
        The database is created using dummy data. Only a few entries are inserted in the database.

        **Example Queries:**

        1. List all branches.
        2. Provide a list of branches and the number of customers at each.
        3. What is the branch with the highest count of customers ?
        4. Where is 'petaling jaya' branch located ?
        5. Who are you ?
        """
    )

# Optional user name input
user_name = st.sidebar.text_input("Your Name (optional):")

# File upload for database schema (text file)
uploaded_file = st.sidebar.file_uploader("Upload Database Schema (Text):", type="txt")

st.write("Instruction: Go to the sidebar and then upload a schema. You may use the [example](https://drive.google.com/file/d/1scTV3Vq_qG6cRxmi4gYO_CtSispqc1gi/view?usp=sharing) provided. Then ask a question about your data.")

if uploaded_file is not None:
    # Read the schema from the uploaded text file
    schema = uploaded_file.read().decode("utf-8") 
  #  st.write("Uploaded Schema:")
  #  st.text(schema)  # Display the schema as text

    
    # User query input
    user_query = st.text_input("Ask a question about your data:")

    if user_query:
        # Generate SQL code using GPT-4o-mini
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are Jane, Dr. Yu Yong Poh's PA, who is also SQL expert that generates SQLITE SQL code based on user queries and database schemas. Do not include any explanations or markdown. If users ask something not related to the schema, just state 'nothing is found' "},
                {"role": "user", "content": f"Schema:\n{schema}\n\nQuery: {user_query}"}
            ]
        )
        if response.choices[0].message.content!= 'nothing is found':
            generated_sql = response.choices[0].message.content

            clean_sql = re.sub(r"```sql\s*(.*?)\s*;", r"\1", generated_sql)
 


        

            # Connect to the SQLite database 
            conn = sqlite3.connect('bank11.sqlite')
            cursor = conn.cursor()

            try:
                # Execute the SQL code
                cursor.execute(clean_sql)
                results = cursor.fetchall()

                # Display the results
                st.write("Results:")
             #   st.dataframe(results)

                # Generate a response using GPT-4o-mini, optionally including the user's name
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": f"You are Jane, Dr. Yu Yong Poh's PA. {'Address the user as ' + user_name if user_name else ''}"},
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

        else:
            response = client.chat.completions.create(
                 model="deepseek-chat",
                messages=[
                    {"role": "system", "content": f"You are Jane, Dr. Yu Yong Poh's PA. {'Address the user as ' + user_name if user_name else ''}. Referring to user query , politely tell the user that couldn't retrieve any specific information from the database."},
                    {"role": "user", "content": f"SQL results:\n{response.choices[0].message.content}\n\nAnswer the user's original query: {user_query}"}
                ]
            )
            # Display the chatbot's response
            st.write(response.choices[0].message.content)



#########################################################################################################


# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# # --- Part 1: Schema Upload and SQL Generation ---

# st.title("LLM-Powered Chatbot with Database Integration")

# # Checkbox for demo information
# if st.checkbox("Read Me"):
#     st.write(
#         """
#         This app demonstrates a simple demo on LLM with database integration. 
#         It uses a schema provided by [Ankit Kumar](https://github.com/ankittkp/Bank-Database-Design). 
#         You may download a copy [HERE](https://drive.google.com/file/d/1scTV3Vq_qG6cRxmi4gYO_CtSispqc1gi/view?usp=sharing)
#         The database is created using dummy data. Only a few entries are inserted in the database.

#         **Example Queries:**

#         1. List all branches.
#         2. Provide a list of branches and the number of customers at each.
#         3. What is the branch with the highest count of customers ?
#         4. Where is 'petaling jaya' branch located ?
#         5. Who are you ?
#         """
#     )

# # Optional user name input
# user_name = st.sidebar.text_input("Your Name (optional):")

# # File upload for database schema (text file)
# uploaded_file = st.sidebar.file_uploader("Upload Database Schema (Text):", type="txt")

# st.write("Instruction: Go to the sidebar and then upload a schema. You may use the [example](https://drive.google.com/file/d/1scTV3Vq_qG6cRxmi4gYO_CtSispqc1gi/view?usp=sharing) provided. Then ask a question about your data.")

# if uploaded_file is not None:
#     # Read the schema from the uploaded text file
#     schema = uploaded_file.read().decode("utf-8") 
#   #  st.write("Uploaded Schema:")
#   #  st.text(schema)  # Display the schema as text

    
#     # User query input
#     user_query = st.text_input("Ask a question about your data:")

#     if user_query:
#         # Generate SQL code using GPT-4o-mini
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are Jane, Dr. Yu Yong Poh's PA, who is also SQL expert that generates SQLITE SQL code based on user queries and database schemas. Do not include any explanations or markdown. If users ask something not related to the schema, just state 'nothing is found' "},
#                 {"role": "user", "content": f"Schema:\n{schema}\n\nQuery: {user_query}"}
#             ]
#         )
#         if response.choices[0].message.content!= 'nothing is found':
#             generated_sql = response.choices[0].message.content

#             clean_sql = re.sub(r"```sql\s*(.*?)\s*```", r"\1", generated_sql)
 


        

#             # Connect to the SQLite database 
#             conn = sqlite3.connect('bank11.sqlite')
#             cursor = conn.cursor()

#             try:
#                 # Execute the SQL code
#                 cursor.execute(clean_sql)
#                 results = cursor.fetchall()

#                 # Display the results
#                 st.write("Results:")
#              #   st.dataframe(results)

#                 # Generate a response using GPT-4o-mini, optionally including the user's name
#                 response = client.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=[
#                         {"role": "system", "content": f"You are Jane, Dr. Yu Yong Poh's PA. {'Address the user as ' + user_name if user_name else ''}"},
#                         {"role": "user", "content": f"SQL results:\n{results}\n\nAnswer the user's original query: {user_query}"}
#                     ]
#                 )
#                 # Display the chatbot's response
#                 st.write(response.choices[0].message.content)

#             except Exception as e:
#                 st.error(f"Error executing SQL: {e}")

#             finally:
#                 # Close the database connection
#                 conn.close()

#         else:
#             response = client.chat.completions.create(
#                  model="gpt-4o-mini",
#                 messages=[
#                     {"role": "system", "content": f"You are Jane, Dr. Yu Yong Poh's PA. {'Address the user as ' + user_name if user_name else ''}. Referring to user query , politely tell the user that couldn't retrieve any specific information from the database."},
#                     {"role": "user", "content": f"SQL results:\n{response.choices[0].message.content}\n\nAnswer the user's original query: {user_query}"}
#                 ]
#             )
#             # Display the chatbot's response
#             st.write(response.choices[0].message.content)



