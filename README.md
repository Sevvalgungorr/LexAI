
# LexAI — AI-Powered Legal Precedent Search and Analysis

LexAI is an AI-powered legal research system designed to help legal professionals search, retrieve, and analyze Turkish court decisions.

The project aims to improve legal research through natural language processing (NLP), semantic search, and knowledge graph technologies.

## Project Objectives

- Search Turkish court decisions using natural language queries.
- Retrieve relevant legal precedents based on semantic similarity.
- Generate concise summaries of court decisions.
- Explore relationships between legal cases using knowledge graphs.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Django, Django REST Framework |
| Database | SQLite (development) |
| NLP | Turkish BERT / Transformer-based models (planned) |
| Vector Database | Milvus or Pinecone (planned) |
| Knowledge Graph | Neo4j (planned) |
| Frontend | React (planned) |

## Current Development Status

LexAI is currently in the early backend development stage.

Implemented:
- Django project and application structure
- REST API endpoint for legal search requests
- Request validation using Django REST Framework
- Service layer with a placeholder search response
- Legal decision database model and initial migration
- Initial API tests

Planned:
- Legal decision data collection and preprocessing
- Semantic search and vector database integration
- Legal-domain NLP model adaptation
- AI-powered decision summarization
- Knowledge graph integration
- Frontend development

## API Endpoint

### POST /api/search/

Accepts a legal search query and the requested number of results.

Example request:

```json
{
  "query": "Haksız işten çıkarılma ile ilgili emsal kararlar",
  "top_k": 5
}
```

Currently, the endpoint validates requests and returns a placeholder response. Semantic retrieval has not yet been implemented.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sevvalgungorr/LexAI.git
cd LexAI
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/api/search/`

## Running Tests

```bash
python manage.py test backend.search_app
```

## Project Status

Under active development as a Computer Engineering graduation project.
