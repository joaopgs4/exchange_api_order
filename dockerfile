FROM python:3.12-slim
WORKDIR /order
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x ./uvicorn.sh
ENV PYTHONPATH=/order/app
CMD ["/bin/bash", "./uvicorn.sh"]
