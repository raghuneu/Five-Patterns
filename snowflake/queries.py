"""
snowflake/queries.py
Python connection layer for the Chapter 04 demo.

Provides a thin wrapper around snowflake-connector-python so every
notebook cell and script can call `get_connection()` instead of
duplicating credential-loading logic.
"""

import os
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()


def get_connection() -> snowflake.connector.SnowflakeConnection:
    """Return an authenticated Snowflake connection using .env credentials."""
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )


def run_query(sql: str, params: tuple | None = None) -> list[dict]:
    """Execute a SQL query and return results as a list of dicts."""
    with get_connection() as conn:
        cur = conn.cursor(snowflake.connector.DictCursor)
        cur.execute(sql, params)
        return cur.fetchall()


def call_cortex(prompt: str, model: str | None = None) -> str:
    """Call Snowflake Cortex COMPLETE and return the response text."""
    model = model or os.getenv("CORTEX_MODEL", "mistral-large")
    sql = """
        SELECT SNOWFLAKE.CORTEX.COMPLETE(%(model)s, %(prompt)s) AS response
    """
    with get_connection() as conn:
        cur = conn.cursor(snowflake.connector.DictCursor)
        cur.execute(sql, {"model": model, "prompt": prompt})
        row = cur.fetchone()
        return row["RESPONSE"] if row else ""


def log_llm_call(
    pattern_name: str,
    call_type: str,
    prompt: str,
    response: str,
    model_used: str,
    tokens_used: int,
    latency_ms: float,
) -> None:
    """Insert a row into CHAPTER04.LLM_CALL_LOG."""
    sql = """
        INSERT INTO CHAPTER04.LLM_CALL_LOG
            (pattern_name, call_type, prompt, response, model_used, tokens_used, latency_ms)
        VALUES (%(pattern_name)s, %(call_type)s, %(prompt)s, %(response)s,
                %(model_used)s, %(tokens_used)s, %(latency_ms)s)
    """
    with get_connection() as conn:
        conn.cursor().execute(sql, {
            "pattern_name": pattern_name,
            "call_type": call_type,
            "prompt": prompt,
            "response": response,
            "model_used": model_used,
            "tokens_used": tokens_used,
            "latency_ms": latency_ms,
        })
