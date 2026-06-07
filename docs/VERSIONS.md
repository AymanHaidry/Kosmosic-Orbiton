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
| 1 | **Tokyo** | Basic reasoning, voice commands, web search, file management, aviation tools, toxic motivation. | `1.x.x` | **Current** |
| 2 | **Odyssey** | Large-scale growth. Advanced reasoning, local LLM integration, long-term memory, personalization engine. | `2.x.x` | Planned |
| 3 | **Genesis** | Agentic behavior. Long-running tasks, predictive execution, multi-step workflows, scraper living on your PC. | `3.x.x` | Planned |
| 4 | **Micron** | Lite version. All core functionality, stripped of heavy dependencies, for older hardware or minimal installs. ROI-dependent. | `4.x.x` | Planned (ROI-dependent) |
| 5 | **Aphrodite** | Expansion beyond the original vision. IoT integration, multi-language support, various voices, wake word customization. | `5.x.x` | Planned |
| 6 | **Singularity** | Full autonomy. Multi-device ecosystem, predictive everything, self-maintenance, multi-device continuity. | `6.x.x` | Vision |
| 7 | **Utopia** | Final evolution. The absolute top. Orbiton becomes the second user of your computer. | `7.x.x` | Final Vision |

---

## Current Generation

### Generation 1 — Tokyo

The founding generation of Kosmosic.

The point at which isolated ideas became a connected command ecosystem.

Version Range: `1.x.x`

Examples:

* `1.0.0` — Initial Public Release
* `1.1.0` — Intelligence Module (NLP, knowledge base, Wikimedia)
* `1.2.0` — File Explorer Integration + Boot Sequence
* `1.3.0` — Sleep/Wake Controls + Reboot System
* `1.4.0` — Test Suite + CI/CD Pipeline
* `1.4.1` — Platform-aware subprocess mocking
* `1.4.2` — Documentation Suite (PHILOSOPHY, ROADMAP, CONTRIBUTING)
* `1.4.3` — Changelog + Versioning System

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
