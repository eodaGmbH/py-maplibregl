FROM python:3.11.5

RUN pip install maplibre

COPY ./app.py ./app.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8050"]
