# System Design
## Architecture
- **Backend**: FastAPI server with SQLite for function metadata.
- **Execution**: Docker containers for Python/JavaScript functions.
- **Frontend** (Week 3): Streamlit for dashboard.
- **Metrics** (Week 2): SQLite for execution metrics.
## Decisions
- SQLite for lightweight storage.
- Docker with WSL 2 for virtualization.
- Python 3.9.13, Node.js 20.19.0 compatible.
