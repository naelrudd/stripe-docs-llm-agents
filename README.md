# Stripe Docs for LLM Agents

An unofficial, machine-readable mirror of the official [Stripe developer documentation](https://docs.stripe.com/) — **473 pages** mirrored as plain Markdown for **LLM ingestion, RAG pipelines, and knowledge graph exploration**.

Stripe is a global payments and financial infrastructure platform. This repo lets AI assistants answer integration questions — payments, Checkout, Billing, Connect, webhooks, API reference, and more — directly from first-party documentation text.

## Contents

The folder tree mirrors `docs.stripe.com/...` 1:1 by URL path:

| Area | Path | Notes |
|------|------|-------|
| Payments | [`payments/`](payments.md) | Payment methods, Payment Intents, refunds, disputes |
| Checkout | [`checkout/`](checkout.md) | Hosted Checkout & embedded Checkout |
| Billing | [`billing/`](billing.md) | Subscriptions, invoices, revenue recognition |
| Connect | [`connect/`](connect.md) | Platform integrations, marketplaces |
| API Reference | [`api/`](api/) | v1 API reference (per-endpoint pages) |
| Webhooks | [`webhooks/`](webhooks.md) | Event delivery, signatures, retries |
| More | [`terminal/`](terminal.md), [`issuing/`](issuing.md), [`treasury/`](treasury.md), [`tax/`](tax.md), [`radar/`](radar.md), [`identity/`](identity.md), [`elements/`](elements.md) | Stripe financial products |

## Quick Start

```bash
git clone https://github.com/naelrudd/stripe-docs-llm-agents.git
cd stripe-docs-llm-agents

# Feed the markdown files directly to your LLM
cat payments.md | your-llm-prompt

# Or use with LangChain / LlamaIndex
python - <<'PY'
from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader(".", glob="**/*.md", exclude=["README.md", "INDEX.md"])
docs = loader.load()
PY
```

For discovery, start from the curated [`INDEX.md`](INDEX.md) or the official [`llms.txt`](llms.txt). Stripe's own index includes an [LLM best-practices section](llms.txt) — read it first when integrating.

## RAG Starter Kit

Local semantic search over the docs:

```bash
pip install chromadb
python rag.py build                    # index Markdown pages into ./rag_chroma
python rag.py query "your question"    # retrieve top-k relevant chunks
python rag.py info                     # corpus stats
```

Re-running `build` is idempotent and incremental.

## Updating

Re-mirror from the official index:

```bash
curl -sL -o llms.txt https://docs.stripe.com/llms.txt
# parse each https://docs.stripe.com/*.md link and download, preserving the URL path
```

Note: a few pages in Stripe's index return 404 upstream (dead links) and are omitted.

## License & attribution

- This repository is **not affiliated with, endorsed by, or sponsored by Stripe, Inc.**
- All documentation content is © Stripe, Inc. and belongs to its respective owners. It is mirrored "as is" from the official [Stripe docs](https://docs.stripe.com/), which serves these pages as Markdown for AI consumption.
- Refer to [docs.stripe.com](https://docs.stripe.com/) for authoritative, always-current documentation.
- No API keys, secrets, or credentials are (or should be) stored here.
