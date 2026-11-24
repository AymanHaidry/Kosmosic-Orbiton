# Kosmosic Versioning System

Kosmosic uses the format:

**Generation.Feature.Build**

Example: `1.4.3`

| Position | Meaning |
|----------|---------|
| Generation | Major era of the product |
| Feature | Significant feature release within that era |
| Build | Fixes, improvements, and refinements |

---

## Model Classes & Generations

Each generation is named after a model class. The class order is fixed and represents the evolution of Orbiton's intelligence and capability.

| Generation | Class | Description | Version Range | Status |
|------------|-------|-------------|---------------|--------|
| 1 | **Tokyo** | Basic reasoning, voice commands, web search, file management, aviation tools, toxic motivation. | `0.x.x` (current release: `v0.8.0`) | **Current** |
| 2 | **Odyssey** | Large-scale growth. Advanced reasoning, local LLM integration, long-term memory, personalization engine. | `1.x.x` | Planned |
| 3 | **Genesis** | Agentic behavior. Long-running tasks, predictive execution, multi-step workflows, scraper living on your PC. | `2.x.x` | Planned |
| 4 | **Micron** | Lite version. All core functionality, stripped of heavy dependencies, for older hardware or minimal installs. ROI-dependent. | `3.x.x` | Planned (ROI-dependent) |
| 5 | **Aphrodite** | Expansion beyond the original vision. IoT integration, multi-language support, various voices, wake word customization. | `4.x.x` | Planned |
| 6 | **Singularity** | Full autonomy. Multi-device ecosystem, predictive everything, self-maintenance, multi-device continuity. | `5.x.x` | Vision |
| 7 | **Utopia** | Final evolution. The absolute top. Orbiton becomes the second user of your computer. | `6.x.x` | Final Vision |

---

## Current Generation

### Generation 1 — Tokyo

The founding generation of Kosmosic.

The point at which isolated ideas became a connected command ecosystem.

Version Range: `0.x.x`

Examples:

* `0.1.0` — Initial project structure and proof-of-concept voice input
* `0.3.0` — Initial voice command framework
* `0.4.0` — Intelligence module, NLP, and knowledge lookups
* `0.6.2` — Spoken-math normalization and safe evaluation
* `0.7.0` — Standalone troubleshooter and expanded test suite
* `0.7.3` — Post-TTS silence cooldown
* `0.8.0` — Cross-platform device-control suite

---

## Future Generations

### Generation 2 — Odyssey

The beginning of large-scale growth.

Advanced reasoning, local LLM integration, long-term memory, personalization engine, agentic tasks.

Version Range: `2.x.x`

### Generation 3 — Genesis

Agentic behavior and true automation.

Long-running tasks, predictive execution, multi-step workflows, scraper living on your PC, OTA intel updates.

Version Range: `3.x.x`

### Generation 4 — Micron

Lite version for constrained environments.

All core functionality, stripped of heavy dependencies, for older hardware or minimal installs. Only built if Odyssey and Genesis prove ROI.

Version Range: `4.x.x`

### Generation 5 — Aphrodite

Expansion beyond the original vision.

IoT integration, multi-language support, various voices, wake word customization, PC management, email, calls, calendar.

Version Range: `5.x.x`

### Generation 6 — Singularity

Full autonomy. The second user of your computer.

Multi-device ecosystem, predictive everything, self-maintenance, multi-device continuity, wearables, smart glasses, SBCs.

Version Range: `6.x.x`

### Generation 7 — Utopia

Final evolution. The absolute top.

Orbiton becomes an ecosystem. Replaces bloatware AIs. Lives on every device you own. Knows what you need before you ask.

Version Range: `7.x.x`

---

## Release Rules

### Generation Increment

Increase the Generation number when:

* Core architecture changes significantly
* Product vision expands substantially
* Major redesigns occur
* A new era of Kosmosic begins

Example: `1.9.7` → `2.0.0` (Tokyo → Odyssey)

---

### Feature Increment

Increase the Feature number when:

* New major functionality is released
* New systems are introduced
* User-facing capabilities expand

Example: `1.3.4` → `1.4.0` (added CI/CD pipeline)

---

### Build Increment

Increase the Build number when:

* Bugs are fixed
* Performance improves
* UI refinements are shipped
* Minor improvements are released

Example: `1.4.2` → `1.4.3` (added documentation)

---

## Release Naming Convention

Releases may be referred to using either:

**Kosmosic Tokyo 1.4.3**

or

**v1.4.3 "Tokyo"**

Both formats are considered official.

---

> *"The future is built one session at a time."*
