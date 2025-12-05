FROM python:3.10

### Create working directory
WORKDIR /transactions_analytics_01

### Copy files
COPY . /transactions_analytics_01/


EXPOSE 30006

# Install dependencies
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30006"]