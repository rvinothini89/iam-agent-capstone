# Deployment Assumptions and Limitations

## Deployment Overview

The IAM AI Agent was deployed as a containerized application using Docker.

The deployment includes:

- Streamlit UI
- IAM Decision Agent
- IAM Security Agent
- RAG-based retrieval using FAISS
- Adaptive behavior layer
- Logging and tracing
- Runtime failure handling

The application runs locally inside a Docker container and exposes the Streamlit UI through port `8501`.

---

# Running the Agent Locally

## Run Streamlit Application

From the project root directory:

```bash
streamlit run ui/app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# Running the Agent Using Docker

## Build Docker Image

```bash
docker build --no-cache -t iam-agent .
```

---

## Run Docker Container

```bash
docker run --env-file .env -p 8501:8501 iam-agent
```

---

## Docker Port Mapping

| Host Port | Container Port | Purpose |
|---|---|---|
| 8501 | 8501 | Streamlit UI |

The application can be accessed at:

```text
http://localhost:8501
```

---

# Docker Deployment Workflow

## Dockerfile Responsibilities

The Docker container performs the following:

- Copies application source code
- Installs dependencies from `requirements.txt`
- Configures Python runtime
- Exposes Streamlit port
- Starts the Streamlit UI automatically

Example Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV PYTHONPATH=/app

CMD ["streamlit", "run", "ui/app.py"]
```

---

# Environment Variable Configuration

The deployment requires a `.env` file.

Example:

```text
OPENAI_API_KEY=<your_api_key>
OPENAI_BASE_URL=https://api.openai.com/v1
```

Environment variables are injected during runtime using:

```bash
docker run --env-file .env -p 8501:8501 iam-agent
```

This avoids embedding secrets directly inside the Docker image.

---

# Deployment Assumptions

## Environment Assumptions

| Assumption | Description |
|---|---|
| Docker installed | Docker Desktop or Docker Engine must be available |
| Internet connectivity | Required for OpenAI API access |
| Valid OpenAI API key | Required for embeddings and LLM calls |
| FAISS index exists | Vector index must already be generated |
| Streamlit supported | Used as the frontend UI |

---

## FAISS Assumptions

The deployment assumes:

- FAISS vector index exists under:

```text
rag/faiss_index/
```

- Compatible dependency versions are installed:

```text
numpy==1.26.4
faiss-cpu==1.7.4
```

This ensures compatibility between NumPy and FAISS.

---

## Agent Functional Assumptions

The IAM agent assumes:

- Policies exist inside indexed documents
- User requests contain extractable IAM attributes
- Role, access type, and resource can be identified
- Memory state remains valid during conversation flow
- Feedback adaptation rules are predefined

---

# Deployment Limitations

## Local Deployment Only

The current deployment supports:

- Local Docker execution
- Local Streamlit UI access

The system is not currently deployed to:

- Kubernetes
- AWS
- Azure
- GCP
- Production distributed environments

---

## No Authentication Layer

The current Streamlit UI does not implement:

- User authentication
- Role-based UI authorization
- Session isolation
- Multi-user access control

---

## Single Container Architecture

The deployment uses a single Docker container containing:

- UI layer
- Agent logic
- Retrieval engine
- Logging components

The architecture does not currently separate:

- API services
- Vector databases
- Logging infrastructure
- Distributed memory systems

---

## Runtime Dependency Constraints

The deployment depends on external services:

| Dependency | Purpose |
|---|---|
| OpenAI API | LLM inference and embeddings |
| Internet access | API communication |
| FAISS | Vector similarity retrieval |

If OpenAI connectivity fails, the agent cannot perform inference or embeddings.

---

## Logging Limitations

Logs are stored locally in:

```text
logs/agent.log
```

The deployment does not currently support:

- Centralized logging
- Monitoring dashboards
- Distributed tracing systems
- Cloud observability platforms

---

## Memory Persistence Limitations

Conversation memory and adaptive feedback are stored locally using JSON files.

Current limitations:

- No distributed persistence
- No database-backed storage
- No multi-user synchronization

---

## Docker Deployment Limitations

The Docker deployment currently assumes:

- CPU-only execution
- Local filesystem persistence
- Manual container startup

The deployment does not currently include:

- Docker Compose orchestration
- Persistent Docker volumes
- Container auto-scaling
- Health checks

---

# Runtime Failure Handling

Graceful failure handling was implemented using:

- `try-except` runtime protection
- Error logging
- Fallback responses

Example fallback response:

```json
{
  "request_type": "system_error",
  "decision": "error",
  "reason": "Agent failed to process request",
  "next_step": "Please retry later"
}
```

This prevents runtime crashes and improves deployment reliability.

---

# Deployment Outcome

The IAM AI Agent was successfully deployed locally using Docker with:

- Reproducible dependency management
- Environment variable injection
- RAG retrieval support
- Logging and tracing
- Runtime failure handling
- Streamlit UI integration

The deployment demonstrates production-oriented deployment readiness for an AI-driven IAM workflow.
