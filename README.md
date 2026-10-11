# 🌿 TrailPulse — Touch Grass Outdoor Companion

> **An open-source, anti-screen micro-planner powered by open-weight AI (Gemma 2) that gets you off your device and into the real world in under 30 seconds.**

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-Touch%20Grass%20Challenge-2e7d32)](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](Dockerfile)
[![Open Weights](https://img.shields.io/badge/Model-Google%20Gemma%202-purple)](https://huggingface.co/google/gemma-2-2b-it)

---

## 🎯 The Philosophy: "Shortest Screen Time Wins"

Most outdoor apps trap you in your screen: scrolling feeds, checking leaderboards, and monitoring badges while you're supposed to be outside. 

**TrailPulse is built around the opposite philosophy:**
1. **Choose your environment** (park, trail, backyard, urban walk) and your available time (10m - 60m).
2. **Generate a 3-point sensory micro-mission** powered by open-weight AI in under 3 seconds.
3. **Listen hands-free or lock the screen** into "Pocket Disconnect Mode" and go touch grass.

---

## ✨ Features

- 🧠 **Open-Weight AI at the Core:** Leverages Google's **Gemma 2** (`google/gemma-2-2b-it`) for grounded, creative sensory field tasks.
- 📵 **Pocket Disconnect Mode:** Turns the screen black with a soft ambient timer, discouraging digital distraction while tracking your outdoor session.
- 🔊 **Hands-Free Audio:** One-click spoken mission briefing so you can leave your phone in your pocket with earbuds.
- 🛡️ **100% Offline Resilience:** Operates via live open-weight API or falls back to an offline heuristic engine when you're off-grid on a trail with zero cell reception.
- 🐳 **Docker-First:** Zero setup friction. Up and running anywhere with a single command.

---

## 🚀 Quick Start with Docker

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose

### 1. Clone & Enter Directory
```bash
git clone https://github.com/your-username/TrailPulse.git
cd TrailPulse