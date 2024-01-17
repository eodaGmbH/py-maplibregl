FROM python:3.11.5

COPY ./app.py ./app.py

RUN pip install maplibre pandas shapely

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8050"]
