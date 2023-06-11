FROM python:3.11.3-bullseye

ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT
ARG BUILD_URL
ENV BUILD_URL=$BUILD_URL
ARG BUILD_ID
ENV BUILD_ID=$BUILD_ID
ARG BUILD_NUMBER
ENV BUILD_NUMBER=$BUILD_NUMBER

ENV PYTHONPATH=$PYTHONPATH:/app
COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip setuptools
RUN pip install -r /app/requirements.txt

# Copy application source code
COPY . /app
WORKDIR /app
ENTRYPOINT ["python", "fastapi_example/main.py"]