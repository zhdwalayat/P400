# Educational Material Automation System

Role-based, subject-agnostic workflow automation system for university lecturers to automate creation of educational materials (notes, quizzes, presentations) with integrated Task Management API.

## How to Run This Project

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Step 1: Install Dependencies

Open Command Prompt (CMD) and run:

```cmd
cd H:\P400\PROJECT1
pip install -r requirements.txt
```

### Step 2: Start the API Server

```cmd
python -m uvicorn api.main:app --reload
```

**Note:** If you see a warning about "frozen importlib", you can ignore it - the server will still run.

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Step 3: Run Tests

```cmd
python -m pytest api/tests/ -v
```

Expected output: **56 tests passed**

### Step 4: Test the API (Windows CMD)

```cmd
REM Health check
curl http://localhost:8000/api/health

REM Create a subject (Windows CMD uses double quotes)
curl -X POST http://localhost:8000/api/subjects -H "Content-Type: application/json" -d "{\"name\": \"Data Structures\"}"

REM List all subjects
curl http://localhost:8000/api/subjects
```

### Step 4 Alternative: Test via Browser

Simply open these URLs in your browser:
- http://localhost:8000/docs (Interactive Swagger UI)
- http://localhost:8000/api/health
- http://localhost:8000/api/subjects

## Technology Stack

| Component | Technology |
|-----------|------------|
| API Framework | FastAPI |
| Database | SQLModel (SQLite) |
| Testing | pytest (56 tests) |
| Document Generation | python-docx, python-pptx, reportlab |

## Project Structure

```
PROJECT1/
├── api/                    # Task Management API
│   ├── main.py             # Entry point
│   ├── config.py           # Settings
│   ├── database.py         # SQLite connection
│   ├── models/             # Database models
│   ├── schemas/            # Request/response schemas
│   ├── services/           # Business logic
│   ├── routes/             # API endpoints
│   └── tests/              # Test suite (56 tests)
├── shared/                 # Utilities
│   ├── formatters/         # PDF, DOCX, PPTX generators
│   ├── validators/         # Input validation
│   └── utils/              # File/version management
├── skills/                 # Educational skills
│   ├── project-organization/
│   ├── notes/
│   ├── quiz/
│   └── presentation/
├── requirements.txt
└── pytest.ini
```

## API Endpoints

### Subjects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/subjects` | List all subjects |
| POST | `/api/subjects` | Create subject |
| GET | `/api/subjects/{slug}` | Get subject |
| PUT | `/api/subjects/{slug}` | Update subject |
| DELETE | `/api/subjects/{slug}` | Delete subject |

### Topics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/topics` | List topics |
| POST | `/api/topics` | Create topic |
| GET | `/api/topics/{id}` | Get topic |
| PUT | `/api/topics/{id}` | Update topic |
| DELETE | `/api/topics/{id}` | Delete topic |

### Materials
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/materials` | List materials |
| POST | `/api/materials` | Create material |
| GET | `/api/materials/{id}` | Get material |
| POST | `/api/materials/{id}/increment-version` | Increment version |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List tasks |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks/{id}` | Get task |
| PUT | `/api/tasks/{id}/status` | Update status |
| GET | `/api/tasks/pending` | Get pending tasks |
| GET | `/api/tasks/stats` | Get statistics |

### Utilities
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/utils/sanitize` | Sanitize name to slug |
| GET | `/api/utils/bloom-keywords` | Get Bloom's keywords |
| GET | `/api/health` | Health check |

## Database Models

- **Subject**: Academic subjects (name, slug)
- **Topic**: Topics within subjects
- **Material**: Generated files (type, format, version, path)
- **Task**: Generation tasks (status, params)
- **CLO**: Course Learning Outcomes

## Troubleshooting

### "frozen importlib" warning
This is a Python warning and can be safely ignored. The server will still run correctly.

### curl not found
If curl is not installed, use your browser to test the API at http://localhost:8000/docs

### Port 8000 already in use
Use a different port:
```cmd
python -m uvicorn api.main:app --reload --port 8001
```

## Dependencies

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlmodel>=0.0.14
pydantic>=2.5.0
python-docx>=1.1.0
python-pptx>=0.6.23
reportlab>=4.0.0
pytest>=7.4.0
httpx>=0.25.0
```

---

**Built with**: FastAPI | SQLModel | pytest
