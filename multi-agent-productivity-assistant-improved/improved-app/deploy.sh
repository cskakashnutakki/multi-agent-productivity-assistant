#!/bin/bash

# Multi-Agent Productivity Assistant - Cloud Run Deployment Script
# Author: Nutakki Chandra Sekhara Krishna Akash

set -e

# Configuration
PROJECT_ID="your-gcp-project-id"
SERVICE_NAME="multi-agent-assistant"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Multi-Agent Productivity Assistant to Cloud Run"
echo "============================================================"

# Build the container image
echo "📦 Building container image..."
gcloud builds submit --tag ${IMAGE_NAME}

# Deploy to Cloud Run
echo "☁️  Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0

echo "✅ Deployment complete!"
echo ""
echo "🔗 Service URL:"
gcloud run services describe ${SERVICE_NAME} --platform managed --region ${REGION} --format 'value(status.url)'
