#!/bin/bash
exec > /home/ubuntu/codedeploy_log.txt 2>&1
set -x

AWS_REGION="ap-south-1"
ENV_FILE="/home/ubuntu/app/.env"
IMAGE="869894982980.dkr.ecr.ap-south-1.amazonaws.com/akshatsharma2407/autonexus:latest"

# Ensure docker is started
sudo systemctl start docker
sleep 3

# Helper function to fetch from SSM (auto decrypts SecureString)
get_param() {
  aws ssm get-parameter \
    --name "$1" \
    --with-decryption \
    --region "$AWS_REGION" \
    --query "Parameter.Value" \
    --output text
}

# Fetch all your parameters
DB_USERNAME=$(get_param "/autonexus/DB_USERNAME")
DB_PASSWORD=$(get_param "/autonexus/DB_PASSWORD")
DB_HOSTNAME=$(get_param "/autonexus/DB_HOSTNAME")
DB_PORT=$(get_param "/autonexus/DB_PORT")
DB_NAME=$(get_param "/autonexus/DB_NAME")
ALGORITHM=$(get_param "/autonexus/ALGORITHM")
ACCESS_TOKEN_EXPIRY_MINUTES=$(get_param "/autonexus/ACCESS_TOKEN_EXPIRY_MINUTES")
DAGSHUB_PAT=$(get_param "/autonexus/DAGSHUB_PAT")
SECRET_KEY=$(get_param "/autonexus/SECRET_KEY")

# Create .env file fresh
sudo mkdir -p /home/ubuntu/app
sudo rm -f "$ENV_FILE"
sudo touch "$ENV_FILE"

sudo bash -c "cat <<EOF > $ENV_FILE
DB_USERNAME=$DB_USERNAME
DB_PASSWORD=$DB_PASSWORD
DB_HOSTNAME=$DB_HOSTNAME
DB_PORT=$DB_PORT
DB_NAME=$DB_NAME
ALGORITHM=$ALGORITHM
ACCESS_TOKEN_EXPIRY_MINUTES=$ACCESS_TOKEN_EXPIRY_MINUTES
DAGSHUB_PAT=$DAGSHUB_PAT
SECRET_KEY=$SECRET_KEY
REGION_NAME=$AWS_REGION
EOF"

sudo chmod 600 "$ENV_FILE"

# Login, pull, stop old container, run new one
aws ecr get-login-password --region "$AWS_REGION" | \
  sudo docker login --username AWS --password-stdin 869894982980.dkr.ecr.ap-south-1.amazonaws.com

sudo docker pull "$IMAGE"

sudo docker stop my-app || true
sudo docker rm my-app || true

sudo docker run -d -p 80:8000 \
  --env-file "$ENV_FILE" \
  --name my-app \
  "$IMAGE"
