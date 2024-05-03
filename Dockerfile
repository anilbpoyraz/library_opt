FROM python:3.9-alpine3.13
LABEL maintainer="anilbpoyrazoglu"

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Copy the rest of the application code
COPY . /app
# Set working directory
WORKDIR /app
# Expose port
EXPOSE 8000

# Copy requirements file
# COPY requirements.txt .

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV == 'true' ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        fastapi-user

ENV PATH="/py/bin:$PATH"

USER fastapi-user


# Command to run the application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
