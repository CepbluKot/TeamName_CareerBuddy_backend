sudo docker compose down
sudo rm -rf docker_data
if [ ! -f .env ]; then
    echo -e "AIRFLOW_UID=$(id -u)
CRON_SCHEDULE_CHANNEL_DATA_UPDATE=\"1-59/15 * * * *\"" > .env
echo "created .env file"
fi
export $(cat .env | xargs)
docker build -f dockerfile.dag -t ml_model .
sudo chmod -R a+rwX  /var/run/docker.sock
sudo chmod -R a+rwX  /var/run/
sudo docker compose up airflow-init
sudo docker compose up --build