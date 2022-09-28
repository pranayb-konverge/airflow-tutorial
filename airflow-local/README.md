# On local Ubuntu machine/ your Konverge.AI laptop

## Installation of Airflow:
### Inside your laptop Ubuntu terminal perform below tasks.
- `python3 -m venv sandbox`
- `source sandbox/bin/activate`
- `pip3 install wheel`
- `pip3 --no-cache-dir install apache-airflow==2.1.0 --constraint https://gist.githubusercontent.com/marclamberti/742efaef5b2d94f44666b0aec020be7c/raw/21c88601337250b6fd93f1adceb55282fb07b7ed/constraint.txt`
- Docker compose to use - https://github.com/pranayb-konverge/airflow-tutorial/blob/main/airflow-local/docker-compose_local_executor.yaml

# Use docker-compose for running Airflow in multiple containers - `airflow-local` folder.
## To install and run docker-compose.yaml
1. Install the docker Engine from https://docs.docker.com/engine/install/ubuntu/
2. Then docker desktop - https://docs.docker.com/desktop/linux/install/ubuntu/
3. Read and understand the flow - https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html. Run these commands - https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html#setting-the-right-airflow-user
4. Then in the docker desktop setting >> General >> Enable Docker Compose V1/V2 compatibility mode.
5. Then run the command - `docker-compose -f docker-compose.yaml up -d`
6. Note: normally you will see the docker-compose -v as 1.2.5 but after point (4) you should see `Docker Compose version v2.5.0`.
7. Note: I my case the current folder has 2 files `docker-compose_celery_executor.yaml` & `docker-compose_local_executor.yaml`, I using the local executor one to run. So the command will be `docker-compose -f docker-compose_local_executor.yaml up -d`. The local executor will run the task parallely.
8. The airflow will be running on the port `8080`. Use `http://localhost:8080/home` to access the airflow UI. Password will be `airflow`/`airflow`.

## ERROR: 8080 port already in use
- When I run the command `docker-compose -f docker-compose.yaml up -d`, for webserver 
    - I got this error - `Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:8080 -> 0.0.0.0:0: listen tcp 0.0.0.0:8080: bind: address already in use`
- I check the port access for 8080 - `sudo lsof -t -i:8080` it gave me 2 ports in use `2078, 2084`
- The netstat cmd will give the name of the services these port are running - `sudo netstat -tulpn | grep LISTEN`, Services - `2078/docker-proxy`, `2084/docker-proxy`.
- I killed them using - `sudo kill -9 2078`
- Run the command `docker-compose -f docker-compose.yaml up -d` again.

## Note
- If the dags are not visible please restart the docker containers for webserver and scheduler.

### If you want to run docker as non-root user then you need to add it to the docker group.
- Create the docker group if it does not exist: `sudo groupadd docker`
- Add your user to the docker group: `sudo usermod -aG docker $USER`
- Run the following command or Logout and login again and run (if that doesn't work you may need to reboot your machine first): $ `newgrp docker`
- Check if docker can be run without root: `docker run hello-world`
- Reboot if still got the error: `reboot`


# Block flow of Airflow setup
![Airflow Setup diagram](https://github.com/pranayb-konverge/airflow-tutorial/blob/main/airflow-local/Airflow%20setup%20diagram.jpg)
