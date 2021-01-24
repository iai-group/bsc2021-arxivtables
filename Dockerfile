FROM python:3.9-alpine

WORKDIR /

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "run_tables.py"]