# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- eBPF → gRPC event stream implementation
- FastAPI WebSocket bridge
- Next.js force graph UI
- PID ↔ Container mapping via /proc/$PID/cgroup
- One-click tcpdump with network namespace isolation
- CLI installer with auto-generated dockray.override.yml

## [0.1.0] - 2024-12-30

### Added
- Initial project setup with MIT license
- Comprehensive README with problem statement and architecture overview
- Business model documentation (MIT core + Dockray Pro)
- 6-week MVP roadmap
- Contributing guidelines
- This changelog

### Documentation
- Project positioning: "Real-time X-ray for Docker Compose"
- Clear value proposition: "Know exactly which container is nuking your DB—before prod melts"
- Technical architecture: eBPF → gRPC → FastAPI → Next.js flow
- Target market analysis: >70% greenfield projects on single-host Compose

### Infrastructure
- Git repository initialized
- GitHub repository configured at github.com:gael55x/Dockray.git
- Clean commit history with descriptive messages 