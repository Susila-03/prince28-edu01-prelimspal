# PrelimsPal


# PrelimsPal

[![CI](https://github.com/Susila-03/prince28-edu01-prelimspal/actions/workflows/ci.yml/badge.svg)](https://github.com/Susila-03/prince28-edu01-prelimspal/actions/workflows/ci.yml)
[![Live](https://img.shields.io/website?url=https%3A%2F%2Fprelimspal-new.onrender.com%2Fhealth&label=live)](https://prelimspal-new.onrender.com/docs)
[![Uptime (30 days)](https://img.shields.io/uptimerobot/ratio/m804757953-663e99d4ba8f250308d4a0d8)](https://prelimspal-new.onrender.com/health)

**Status:** Week 1 complete · live at https://prelimspal-new.onrender.com

PrelimsPal is an AI-powered platform that helps students prepare for UPSC preliminary examinations using NCERT textbooks and previous year questions.


**Status:** Day 1 – Project foundation.

## Who it's for

Students preparing for UPSC Civil Services preliminary examinations.

## The problem

Students preparing for UPSC exams often find it difficult to understand concepts from different textbooks. They may struggle to connect previous year questions with the correct syllabus topics. Finding the right information from NCERT textbooks can also take a lot of time. PrelimsPal aims to make learning easier by providing clear explanations and useful references.

## Data sources

- UPSC previous year question papers.
- UPSC Civil Services syllabus.
- NCERT textbooks (Classes 6–12).

Useful links:
- https://upsc.gov.in/
- https://ncert.nic.in/textbook.php

## Hardest problem

Explaining statement-based questions accurately by checking multiple NCERT textbook pages and providing proper references for each statement.

## Signature feature

Question Explainer – Students can select previous year questions and understand the answers with explanations and NCERT page references.

## Target metric

Provide correct answers with valid NCERT citations for at least 80% of 100 tested questions.

## Run it locally

```bash
uv sync
copy .env.example .env
uv run uvicorn prelimspal.api.main:create_app --factory --reload
```

Open: http://localhost:8000/docs

## Checks

```bash
uv run pytest
uv run ruff check .
```

## Run locally in one command

You need Docker Desktop running. From a fresh clone:

```bash
docker compose up --build
```

This starts Postgres (with pgvector), Redis, runs the migrations and loads the sample data once, then starts the API.

- API docs: http://localhost:8000/docs
- Liveness: http://localhost:8000/health
- Readiness (checks the database): http://localhost:8000/ready

Stop with `Ctrl+C`, then `docker compose down`. Add `-v` to also delete the database volume.

## Develop and test

| Task | Mac / Linux | Windows |
|---|---|---|
| Run the API with reload | `make dev` | `uv run poe dev` |
| Unit tests (no network) | `make test` | `uv run poe test` |
| Integration tests (needs `docker compose up`) | `make test-integration` | `uv run poe test-integration` |
| Coverage report | `make cov` | `uv run poe cov` |
| Lint and format check | `make lint` | `uv run poe lint` |
