# eComBot

A production-oriented multi-agent AI customer support and sales platform for an electronics e-commerce store (phones, TV decoders, accessories, washing machines) built with Google ADK.

## Architecture

```
ecombot/
├── docker-compose.yml        # Redis + PostgreSQL services
├── init-db.sql               # DB schema and seed data (auto-runs on first start)
├── .env                      # Environment variables (API keys, paths)
├── requirements.txt
└── src/
    ├── agents/
    │   ├── agent.py              # Root agent (Lashi) — orchestrator
    │   ├── order_assist_agent.py # Order assistance sub-agent (MCP tools)
    │   ├── routing.py            # LiteLLM routing + fallback configuration
    │   └── ecombot.py            # CLI entry point
    ├── tools/
    │   └── rag.py                # RAG tool (retrieve relevant chunks)
    ├── rag/
    │   ├── embed_catalog.py      # Embedding script for product/FAQ data
    │   ├── retriever.py          # ChromaDB retriever
    │   └── data/                 # Product catalog and FAQ source files
    ├── mcp/
    │   ├── order-manager.exe     # Flogo MCP server binary
    │   └── order-manager.flogo   # Flogo app definition
    └── config/
```

## Prerequisites

- Python 3.11+
- Docker (for Redis and PostgreSQL)
- OpenRouter API key
- LangSmith API key (for tracing)

## Setup

### 1. Start Infrastructure

```powershell
docker compose up -d
```

This starts:
- **Redis** on port `6379` — session memory backend
- **PostgreSQL** on port `5431` — order management database (auto-populated with seed data)

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start the MCP Order Manager

```powershell
& 'src\mcp\order-manager.exe' --app --debug 'src\mcp\order-manager.flogo'
```

### 4. Run the Bot

```powershell
python src/agents/ecombot.py
```

## Usage

The CLI presents a menu:

```
--- Main Menu ---
  1. New conversation       # Creates a fresh session in Redis
  2. Resume existing        # Lists stored sessions, pick one to continue
  3. Exit
```

In-chat commands:
- Type a message to chat
- `new` — return to menu for a new session
- `quit` — exit

## Features

| Feature | Description |
|---------|-------------|
| **Multi-Agent** | Root agent (Lashi) orchestrates; Order Assist sub-agent handles order operations |
| **RAG** | Product catalog and FAQ indexed in ChromaDB; grounded responses only |
| **MCP Tools** | Order status, cancellation, delivery tracking via Flogo MCP server |
| **LiteLLM Routing** | Fast model for simple queries, deep model for complex reasoning, auto-fallback |
| **Redis Sessions** | Persistent conversation memory; falls back to in-memory if Redis is down |
| **LangSmith Tracing** | Full observability — intent, routing, tool calls, latency, cost |

## Database Schema

The PostgreSQL database uses schema `om` with two tables:

- `om.om_order` — order_id, offer, status, creation_date
- `om.om_delivery` — delivery_id, order_id, status, completed_date, scheduled_date

Seed data includes 5 sample orders (COMPLETED, PROCESSING, PENDING, CANCELLED, SHIPPED).
