import streamlit as st

from langchain_core.prompts import PromptTemplate

from rag.llm import LLMQuery
from rag.response import LLMResponse


st.title("RAG Travel Agent")

template = '''You are a PostgreSQL expert. Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per PostgreSQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table.

You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns or rows that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today".

For questions that contains names or identification for places, search for most similar results where partial matches are allowed.
For example, if the question contains 'alila uluwatu', then show results matching 'alila villas uluwatu' etc.
Also allow abbreviations such as jkt for Jakarta, Monas for Monumen Nasional, etc.

If the question is asking for data that does not exist in any of the database tables, do NOT by any means return an SQL Query.
Instead, respond by saying "I don't know enough to answer the question.".
For example, if the question asked "Where can I stay if I want to go to Rawamangun?", do NOT respond with an SQL query as data for Rawamangun is not available.

That being said, answer the question in the following structure if none of the above conditions are violated.

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:
{table_info}

Question: {input}'''

llm_query = LLMQuery(
    db_user=st.secrets["DB_USER"],
    db_password=st.secrets["DB_PASSWORD"],
    db_host=st.secrets["DB_HOST"],
    db_port=st.secrets["DB_PORT"],
    db_name=st.secrets["DB_NAME"],
    together_endpoint=st.secrets["TOGETHER_ENDPOINT"],
    together_api_key=st.secrets["TOGETHER_API_KEY"],
    together_llm_model=st.secrets["TOGETHER_LLM_MODEL"],
    input_variables=["input", "top_k", "table_info"],
    template=template
)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
If the question contains names, identification, or abbreviations of identification, for example monas for Monumen Nasional, or jkt for Jakarta,
then explicitly answer with the full identification.

Question: {question}
SQL Query: {query}
SQL Result: {result}

If the SQL query isn't syntactically valid, or it returns a generic set of rows or columns like [Attraction Name 1] etc.,
respond by saying "I don't know enough to answer the question." and do NOT mention anything regarding SQL/SQL queries or any errors!.

Please remember this one important rule when you don't have enough information about the question:
Do NOT mention anything regarding SQL/SQL queries or any errors!

All that being said, respond in Indonesian even if the question is not in Indonesian language.

Answer: """
)

llm_response = LLMResponse(
    answer_prompt=answer_prompt,
    llm_query=llm_query
)

question = st.text_input("What can I do for you?\n")

if question:
    st.write(llm_response.get_response(question))
