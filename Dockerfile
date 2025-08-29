FROM python:3.10

### Create working directory
WORKDIR /transactions_analytics

### Copy files
COPY ./customer_online_transactions_analytics /transactions_analytics/customer_online_transactions_analytics
COPY ./main.py /transactions_analytics
COPY ./logger.py /transactions_analytics
COPY ./requirements.txt /transactions_analytics

EXPOSE 30005

# Install dependencies
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30005"]