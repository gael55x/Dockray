#!/bin/sh

# Dockray eBPF Side-car Entrypoint
# Starts the eBPF monitoring service with proper error handling

set -e

echo "🚀 Starting Dockray eBPF Monitor..."

# Check if we have necessary privileges for eBPF
if [ ! -r /sys/kernel/debug/tracing/trace ]; then
    echo "⚠️  WARNING: Cannot access eBPF tracing. Ensure container runs with:"
    echo "   --privileged OR --cap-add=SYS_ADMIN"
    echo "   -v /sys/kernel/debug:/sys/kernel/debug:rw"
fi

# Verify Docker socket access
if [ ! -S /var/run/docker.sock ]; then
    echo "⚠️  WARNING: Docker socket not mounted. Container mapping will be limited."
    echo "   Mount with: -v /var/run/docker.sock:/var/run/docker.sock:ro"
fi

# Check if running as root (needed for eBPF)
if [ "$(id -u)" != "0" ]; then
    echo "⚠️  WARNING: Not running as root. eBPF probes may fail."
    echo "   Override with: --user root"
fi

# Start the main monitoring service
echo "🔍 Initializing eBPF probes..."
exec python3 -m src.main 