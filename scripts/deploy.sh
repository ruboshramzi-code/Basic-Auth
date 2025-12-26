#!/bin/bash

# AWS Lambda Deployment Script
# This script packages and deploys the Lambda function

set -e  # Exit on error

echo "=================================="
echo "AWS Lambda Deployment Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
FUNCTION_NAME="auth-lambda-function"
HANDLER="lambda_function.lambda_handler"
RUNTIME="python3.12"
REGION="eu-north-1"
PACKAGE_NAME="lambda-deployment.zip"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}✗ AWS CLI not found. Please install it first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ AWS CLI found${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit .env file with your configuration before deploying!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ .env file found${NC}"

# Create package directory
echo ""
echo "Creating deployment package..."
rm -rf package
mkdir -p package

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -t package/ --quiet

# Copy application code
echo "Copying application code..."
cp -r config package/
cp -r utils package/
cp -r middleware package/
cp -r handlers package/
cp lambda_function.py package/
cp .env package/

# Create ZIP file
echo "Creating ZIP archive..."
cd package
zip -r ../${PACKAGE_NAME} . -q
cd ..

echo -e "${GREEN}✓ Deployment package created: ${PACKAGE_NAME}${NC}"
echo ""

# Get package size
PACKAGE_SIZE=$(du -h ${PACKAGE_NAME} | cut -f1)
echo "Package size: ${PACKAGE_SIZE}"
echo ""

# Ask for confirmation
read -p "Deploy to AWS Lambda? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "Deploying to AWS Lambda..."
echo "Function: ${FUNCTION_NAME}"
echo "Region: ${REGION}"
echo "Runtime: ${RUNTIME}"
echo ""

# Check if function exists
if aws lambda get-function --function-name ${FUNCTION_NAME} --region ${REGION} &> /dev/null; then
    echo "Updating existing function..."
    aws lambda update-function-code \
        --function-name ${FUNCTION_NAME} \
        --zip-file fileb://${PACKAGE_NAME} \
        --region ${REGION} \
        --no-cli-pager
    
    echo -e "${GREEN}✓ Function updated successfully!${NC}"
else
    echo -e "${YELLOW}Function does not exist. Please create it manually first with:${NC}"
    echo ""
    echo "aws lambda create-function \\"
    echo "  --function-name ${FUNCTION_NAME} \\"
    echo "  --runtime ${RUNTIME} \\"
    echo "  --role YOUR_LAMBDA_EXECUTION_ROLE_ARN \\"
    echo "  --handler ${HANDLER} \\"
    echo "  --zip-file fileb://${PACKAGE_NAME} \\"
    echo "  --region ${REGION} \\"
    echo "  --timeout 30 \\"
    echo "  --memory-size 512"
    echo ""
    exit 1
fi

# Cleanup
echo ""
read -p "Clean up deployment package? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf package
    rm ${PACKAGE_NAME}
    echo -e "${GREEN}✓ Cleanup complete${NC}"
fi

echo ""
echo "=================================="
echo "Deployment Complete!"
echo "=================================="
