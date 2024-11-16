FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
RUN pip install pipenv
WORKDIR /app
COPY ["Pipfile","Pipfile.lock","./"]
RUN pipenv install --system--deploy
COPY ["app.py", "best_model.pkl", "./"]
EXPOSE 8000
CMD ["python","app.py"]