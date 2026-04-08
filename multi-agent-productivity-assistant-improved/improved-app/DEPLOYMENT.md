# Deployment Guide

## Multi-Agent Productivity Assistant

### Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- Google Cloud SDK (for Cloud Run deployment)

---

## Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/multi-agent-productivity-assistant.git
cd multi-agent-productivity-assistant
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Execute a command
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "add task finish project report"}'
```

---

## Docker Deployment

### Build the Image

```bash
docker build -t multi-agent-assistant .
```

### Run the Container

```bash
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  multi-agent-assistant
```

The `-v` flag mounts a local directory to persist the SQLite database.

---

## Google Cloud Run Deployment

### Prerequisites

1. Install Google Cloud SDK
2. Authenticate: `gcloud auth login`
3. Set project: `gcloud config set project YOUR_PROJECT_ID`

### Option 1: Using the Deployment Script

```bash
# Edit deploy.sh and set your PROJECT_ID
nano deploy.sh

# Run deployment
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Deployment

```bash
# Set variables
export PROJECT_ID=your-gcp-project-id
export SERVICE_NAME=multi-agent-assistant
export REGION=us-central1

# Build and push image
gcloud builds submit --tag gcr.io/${PROJECT_ID}/${SERVICE_NAME}

# Deploy to Cloud Run
gcloud run deploy ${SERVICE_NAME} \
  --image gcr.io/${PROJECT_ID}/${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1
```

### Get the Service URL

```bash
gcloud run services describe ${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --format 'value(status.url)'
```

---

## Environment Variables

Create a `.env` file for local development:

```env
DATABASE_URL=sqlite:///./data/app.db
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

For Cloud Run, set environment variables:

```bash
gcloud run services update ${SERVICE_NAME} \
  --set-env-vars="ENVIRONMENT=production"
```

---

## Database Management

### Initialize Database

The database is automatically initialized on application startup. Tables are created if they don't exist.

### Backup Database

```bash
# Local
cp data/app.db data/backup_$(date +%Y%m%d).db

# Docker
docker exec <container_id> cp /app/data/app.db /app/data/backup.db
docker cp <container_id>:/app/data/backup.db ./backup.db
```

### Reset Database

```bash
rm data/app.db
# Restart the application - database will be recreated
```

---

## Monitoring

### Health Check

```bash
curl https://your-service-url/health
```

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-04-07T12:00:00"
}
```

### System Status

```bash
curl https://your-service-url/status
```

Response:
```json
{
  "success": true,
  "coordinator": "Coordinator",
  "agents": {
    "task": "TaskAgent",
    "calendar": "CalendarAgent",
    "notes": "NotesAgent"
  },
  "task_count": 5,
  "event_count": 3,
  "note_count": 7
}
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Lock Issues

```bash
# Ensure no other process is accessing the database
# Restart the application
```

### Cloud Run Deployment Fails

```bash
# Check logs
gcloud run services logs read ${SERVICE_NAME} --limit=50

# Verify container builds locally
docker build -t test-image .
docker run -p 8000:8000 test-image
```

---

## Scaling

### Cloud Run Auto-Scaling

Cloud Run automatically scales based on traffic:

```bash
gcloud run services update ${SERVICE_NAME} \
  --min-instances=0 \
  --max-instances=10 \
  --concurrency=80
```

### Performance Optimization

- Use connection pooling for database
- Implement caching for frequently accessed data
- Add request rate limiting
- Use async endpoints for long-running operations

---

## Security

### HTTPS

Cloud Run automatically provides HTTPS endpoints.

### Authentication

To add authentication:

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/execute")
async def execute_command(
    request: CommandRequest,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    # Verify token
    # ...
```

### CORS Configuration

Update CORS settings in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## Cost Estimation (Cloud Run)

- **Free Tier**: 2 million requests/month
- **After Free Tier**: ~$0.40 per million requests
- **Memory**: $0.0000025 per GB-second
- **CPU**: $0.00002400 per vCPU-second

Estimated monthly cost for moderate usage (100K requests): **$2-5**

---

## Support

For issues or questions:
- GitHub Issues: [Repository URL]
- Email: your-email@example.com
- Documentation: https://docs.yourproject.com
