# rag-travel-agent

Part of Bahasa.ai's Product Engineer, AI Backend pre-employment test.

## Quickstart (local)

1. Clone repository:

    ```bash
    git clone https://github.com/rayhanrandi/rag-travel-agent.git
    ```

2. Go to directory, create Python virtual environment, activate environment:

    ```bash
    cd rag-travel-agent
    ```

    ```bash
    python -m venv .venv
    ```

    ```bash
    .venv\Scripts\activate.bat
    ```

3. Install requirements:

    ```bash
    pip install -r requirements.txt
    ```

4. Adjust database to local and together.ai's configuration in `app.py`:

    ```python
    llm_query = LLMQuery(
        db_user="<insert-here>",
        db_password="<insert-here>",
        db_host="<insert-here>",
        db_port="<insert-here>",
        db_name="<insert-here>",
        together_endpoint="<insert-here>",
        together_api_key="<insert-here>",
        together_llm_model="<insert-here>",
        input_variables=["input", "top_k", "table_info"],
        template=template
    )
    ```

5. Run app with Streamlit:

    ```bash
    streamlit run app.py & npx localtunnel --port 8501
    ```
