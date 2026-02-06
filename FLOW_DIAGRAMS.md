# 🔄 Flow Diagrams

Visual guide to main system workflows.

---

## 1️⃣ System Architecture

```mermaid
graph TB
    USER["👤 User / Application"]
    API["🔌 Log API"]
    BACKEND["🐍 Django Backend"]
    DB[(🗄️ PostgreSQL)]
    DETECTOR["🔍 Anomaly Detector"]
    EMAIL["📧 Email Alert"]
    DASH["📊 Dashboard"]

    USER --> API
    API --> BACKEND
    BACKEND --> DB
    DB --> DETECTOR
    DETECTOR --> EMAIL
    DB --> DASH


graph LR
    A["⏰ Every 5 min"] --> B["🔍 Detector"]
    B --> C["Count ERROR Logs"]
    C --> D{{"Errors ≥ 5 ?"}}
    D -->|No| E["✅ Continue Monitoring"]
    D -->|Yes| F["⚠️ Trigger Alert"]
    F --> G["📧 Send Email"]
