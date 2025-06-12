# Dockray eBPF Side-car
FROM alpine:3.18

# Install Python 3, eBPF dependencies, and build tools
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    linux-headers \
    clang \
    llvm \
    make \
    gcc \
    musl-dev \
    elfutils-dev \
    zlib-dev \
    libbpf-dev \
    bcc-tools \
    bcc-dev \
    py3-bcc

# Create app directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set up non-root user for security
RUN addgroup -g 1001 dockray && \
    adduser -D -u 1001 -G dockray dockray

# Switch to non-root user
USER dockray

# Health check to ensure the service is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Expose gRPC port
EXPOSE 8080

# Start the eBPF monitor
ENTRYPOINT ["./entrypoint.sh"] 