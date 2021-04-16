# bsc2021-arxivtables

Table Extraction from Scientific Publications on arXiv

## System Requirements

- Docker
- Docker Compose
- Windows, Mac or Linux OS on x86, x64, ARM64 arch



## Setting up

### Getting the repository ready

<pre>
git clone git@github.com:iai-group/bsc2021-arxivtables
cd bsc2021-arxivtables
</pre>

At this point you may wish to customize `config.yml`.  This is not necessary, as it comes with default to run the table extraction for current date and to use MongoDB in addition to local JSON.

### First run
To run for the first time, or to update the Docker image after updating the code, run:
<pre>
docker-compose up --build [-d] 
# -d flag runs the Docker container in detached mode (aka runs in the background)
</pre>

Subsequent manual runs, without rebuilding the image, may be run by:
<pre>docker-compose up [-d]</pre>

### Cronjobs

Add the following line to crontab

<pre>0 6 * * * docker-compose up -d</pre>

This will run the `docker-compose up -d` script every day at 06:00 local time.

### Checking in
To see if the Docker containers are running, run `docker ps` in the terminal.

One can enter a Docker container's CLI by running the following command: 
<pre>
docker exec -it [container_id OR container_name]  /bin/sh 
# container_id can be retreived from `docker ps` command
</pre>

## Running tests

<pre>
python3 -m unittest tests.test -v
</pre>
