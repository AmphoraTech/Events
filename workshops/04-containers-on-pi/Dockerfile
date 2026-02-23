# ARM32 for Raspberry Pi 3. Build: docker build -t myhandler .
FROM arm32v7/python:3-alpine
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
