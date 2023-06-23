FROM python:3

WORKDIR /home/ol/Documents/GitHub/acase

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3"]