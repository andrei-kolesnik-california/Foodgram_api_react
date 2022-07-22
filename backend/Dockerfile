FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir
COPY api_foodgram .

LABEL author='Andrei Kolesnik' version=1 broken_keyboards=3
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["run"]