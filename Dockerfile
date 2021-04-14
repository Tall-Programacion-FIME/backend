FROM public.ecr.aws/m9g7f8o4/tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app /app
