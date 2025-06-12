# Dockray
Real-time X-ray for Docker Compose. eBPF side-car → live traffic graph, 1-click tcpdump.

## Why?
* Logs ≠ packets.
* Portainer shows CPU but not bytes.
* Wireshark is a firehose for multi-container debugging.
* >70% of greenfield projects ship on single-host Compose (local dev, CI runners, edge boxes).
* Existing tools focus on Kubernetes while Compose users fly blind on intra-container traffic.

**One-liner:** Know exactly which container is nuking your DB—before prod melts.

## Current Roadmap
- [ ] eBPF → gRPC event stream
- [ ] FastAPI WebSocket bridge  
- [ ] Next.js force graph UI
- [ ] PID ↔ Container mapping via /proc/$PID/cgroup
- [ ] One-click tcpdump with network namespace isolation
- [ ] CLI installer with auto-generated dockray.override.yml

## Quick start
```bash
docker compose -f examples/basic.yml -f dockray.override.yml up -d
```

## Architecture
```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│ eBPF Probes     │───▶│ FastAPI      │───▶│ Next.js         │
│ (tcp_connect,   │    │ WebSocket    │    │ Force Graph     │
│  tcp_sendmsg)   │    │ Bridge       │    │ UI              │
└─────────────────┘    └──────────────┘    └─────────────────┘
```

## Business Model
- **MIT core**: Live traffic graph visualization
- **Dockray Pro**: 24h replay, anomaly alerts, OAuth/SSO, VS Code plugin
- **Pricing**: $12/dev/month, seat-based

## Contributing
1. Fork the repo
2. Create a feature branch
3. Add tests for new functionality  
4. Submit a pull request

## License
MIT - see [LICENSE](LICENSE) for details.
