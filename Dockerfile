FROM python:alpine

# Get latest root certificates
RUN apk add --no-cache ca-certificates && update-ca-certificates

RUN mkdir -p /app/conf && chown nobody: /app/conf

# Install the required packages
RUN pip install --no-cache-dir redis https://github.com/mher/flower/zipball/master

# PYTHONUNBUFFERED: Force stdin, stdout and stderr to be totally unbuffered. (equivalent to `python -u`)
# PYTHONHASHSEED: Enable hash randomization (equivalent to `python -R`)
# PYTHONDONTWRITEBYTECODE: Do not write byte files to disk, since we maintain it as readonly. (equivalent to `python -B`)
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1

# Default port
EXPOSE 5555

COPY _local/flowerconfig.py /app/conf/
RUN chown nobody: /app/conf/flowerconfig.py

# Run as a non-root user by default, run as user with least privileges.
USER nobody

ENTRYPOINT ["flower", "--conf=/app/conf/flowerconfig.py", "--broker=amqp://admin:admin@127.0.0.1:5672//"]
