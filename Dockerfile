FROM tiangolo/uvicorn-gunicorn:python3.10

WORKDIR /src

ADD ./ /src

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080 

CMD python -m uvicorn main:app --host 0.0.0.0 --port 8080