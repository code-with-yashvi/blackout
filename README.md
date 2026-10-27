# ⚡ BLACKOUT
> An advanced, multiprocessing anti-keylogging and behavioral telemetry-defense suite designed to blind, intercept, and disrupt unauthorized input monitoring.

## 🛡️ Core Architecture
BLACKOUT utilizes a decoupled multi-process architecture to ensure robust system defense:
- **Interceptor Core**: Low-level hook suppression and real-time input shielding.
- **Behavioral Monitor Core**: Continuous background heuristics tracking process access anomalies.
- **Chaff Engine (`core/chaff.py`)**: High-entropy background decoy generation (`logs/decoy_stream.log`) with timestamped ASCII session headers.
- **RAM-Level Encryption**: Secure configuration and state management powered by `Fernet`.
- **Global Emergency Killswitch**: Instant `F12` system unhooking and clean core teardown.

---

## 🚀 Quick Start

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/code-with-yashvi/blackout.git](https://github.com/code-with-yashvi/blackout.git)
   cd blackout