FROM python:3.10-slim

# Install openssl so that we can generate self‑signed certificates during the build.
RUN apt-get update && apt-get install -y --no-install-recommends openssl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the server code into the container.
COPY server.py .

# Generate a self‑signed TLS certificate and private key.  The Common Name (CN)
# is set to "localhost" so that browsers/clients connecting to https://localhost:4443
# will match the certificate.  The certificate is valid for one year (365 days).
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -subj "/CN=localhost" \
    -keyout key.pem -out cert.pem

EXPOSE 4443

# Entrypoint runs the Python HTTPS server.  See server.py for implementation.
CMD ["python", "server.py"]