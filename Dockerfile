FROM python:3.9.8

WORKDIR /src

COPY requirements.txt /src
RUN pip install -r requirements.txt

COPY . /src/

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]