# Dockray

Dockray is a powerful real-time network monitoring and visualization tool specifically designed for Docker Compose environments. It provides deep insights into container-to-container communication using eBPF technology, offering a live traffic graph and one-click packet capture capabilities.

## Features

- **Real-time Traffic Visualization**: Monitor container-to-container communication in real-time with an interactive force-directed graph
- **eBPF-powered Monitoring**: Low-overhead packet inspection using eBPF probes
- **One-click Packet Capture**: Instantly capture and analyze network traffic between containers
- **Container-aware**: Automatically maps processes to containers for clear visibility
- **Lightweight**: Minimal performance impact on your Docker Compose environment
- **Developer-friendly**: Designed specifically for local development and CI/CD environments

## Why Dockray?

- **Beyond Logs**: While logs show application events, Dockray shows the actual network packets
- **Container-specific**: Unlike general monitoring tools, Dockray focuses on container-to-container communication
- **Real-time Insights**: See network traffic patterns as they happen, not just historical data
- **Easy Debugging**: Quickly identify which container is causing network issues
- **Perfect for Compose**: Optimized for Docker Compose environments, unlike Kubernetes-focused tools

## Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│ eBPF Probes     │───▶│ FastAPI      │───▶│ Next.js         │
│ (tcp_connect,   │    │ WebSocket    │    │ Force Graph     │
│  tcp_sendmsg)   │    │ Bridge       │    │ UI              │
└─────────────────┘    └──────────────┘    └─────────────────┘
```

The system consists of three main components:
1. **eBPF Probes**: Capture network events at the kernel level
2. **FastAPI WebSocket Bridge**: Stream events to the frontend
3. **Next.js UI**: Interactive visualization of network traffic

## Quick Start

1. Install Dockray:
```bash
# Clone the repository
git clone https://github.com/yourusername/dockray.git
cd dockray

# Start with example configuration
docker compose -f examples/basic.yml -f dockray.override.yml up -d
```

2. Access the web interface at `http://localhost:3000`

## Development Roadmap

- [ ] eBPF → gRPC event stream
- [ ] FastAPI WebSocket bridge  
- [ ] Next.js force graph UI
- [ ] PID ↔ Container mapping via /proc/$PID/cgroup
- [ ] One-click tcpdump with network namespace isolation
- [ ] CLI installer with auto-generated dockray.override.yml

## Business Model

- **MIT Core**: Live traffic graph visualization
- **Dockray Pro**: 24h replay, anomaly alerts, OAuth/SSO, VS Code plugin
- **Pricing**: $12/dev/month, seat-based

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact us at support@dockray.io
