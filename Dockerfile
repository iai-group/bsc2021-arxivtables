FROM python:3.9

WORKDIR /

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "run_tables.py"]