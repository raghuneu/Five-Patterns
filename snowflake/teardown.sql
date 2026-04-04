-- ============================================================================
-- AGENTIC SYSTEMS BOOK — Chapter 04: Five Agentic Patterns
-- Snowflake Teardown Script
--
-- Drops all Chapter 04 objects and the database itself for a clean slate.
-- Run this before re-running setup.sql during demo iterations.
--
-- Order matters: tables first, then schema, then database, then warehouse.
-- CASCADE on the schema drop handles tables, but explicit drops are
-- included for clarity and selective teardown.
-- ============================================================================

USE DATABASE AGENTIC_SYSTEMS_BOOK;
USE SCHEMA CHAPTER04;

-- Drop all Chapter 04 tables
DROP TABLE IF EXISTS CHAPTER04.LLM_CALL_LOG;
DROP TABLE IF EXISTS CHAPTER04.AGENT_MEMORY;
DROP TABLE IF EXISTS CHAPTER04.AGENT_MESSAGES;
DROP TABLE IF EXISTS CHAPTER04.REFLECTION_ROUNDS;
DROP TABLE IF EXISTS CHAPTER04.EXECUTION_PLANS;
DROP TABLE IF EXISTS CHAPTER04.PATTERN_EVALUATIONS;

-- Drop the schema (CASCADE would also remove tables, but they are already gone)
DROP SCHEMA IF EXISTS CHAPTER04;

-- Drop the database
DROP DATABASE IF EXISTS AGENTIC_SYSTEMS_BOOK;

-- Drop the demo warehouse
DROP WAREHOUSE IF EXISTS AGENTIC_DEMO_WH;
