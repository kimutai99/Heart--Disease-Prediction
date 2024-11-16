FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
RUN pip install pipenv
WORKDIR /app
COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pipenv install --deploy --system
COPY ["app.py", "best_model.pkl", "./"]
EXPOSE 8000
ENTRYPOINT ["waitress-serve", "--listen=0.0.0.0:8000", "app:app"]