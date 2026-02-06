# 🔄 Flow Diagrams

Visual guide to system workflows.

---

## 1️⃣ Architecture

```mermaid
graph TB
    WEB["🌐 Web Form"]
    API["🔌 REST API"]
    SCRIPT["🐍 Python"]
    
    INGEST["📥 Ingest"]
    DB[(🗄️ PostgreSQL)]
    DETECTOR["🔍 Detector<br/>5 min"]
    ALERTS["📧 Email"]
    DASH["📊 Dashboard"]

    WEB --> INGEST
    API --> INGEST
    SCRIPT --> INGEST
    
    INGEST --> DB
    DB --> DETECTOR
    DETECTOR --> ALERTS
    DB --> DASH
```

---

## 2️⃣ Submit Log

```mermaid
sequenceDiagram
    User->>Form: Submit
    Form->>API: POST
    API->>DB: Save
    DB-->>User: ✅ Done
```

---

## 3️⃣ Detect Anomaly

```mermaid
graph LR
    A["⏰ Every 5 min"] --> B["🔍 Detector"]
    B --> C["Count errors<br/>last 5 min"]
    C --> D{{"≥ 5?"}}
    D -->|No| E["✅ OK"]
    D -->|Yes| F["⚠️ Alert!"]
    F --> G["📧 Email"]
```

---

## 4️⃣ REST API

```mermaid
graph LR
    A["POST /api/logs/"] --> B["Validate"]
    B --> C{Valid?}
    C -->|No| D["❌ 400"]
    C -->|Yes| E["💾 Save"]
    E --> F["✅ 200"]
```

---

## 5️⃣ Dashboard

```mermaid
graph TB
    LOGS["📋 Logs"] --> STATS["📊 Stats"]
    ANOM["⚠️ Anomalies"] --> STATS
    ALERT["📧 Alerts"] --> STATS
    STATS --> DISPLAY["Show:<br/>logs, errors<br/>anomalies"]
```

---

## 6️⃣ Email Alert

```mermaid
graph TD
    A["⚠️ Anomaly"] --> B["📧 Compose"]
    B --> C["Send SMTP"]
    C --> D{Success?}
    D -->|Yes| E["✅ Saved"]
    D -->|No| E["❌ Failed"]
```

---

## 7️⃣ Log Lifecycle

```mermaid
graph TD
    A["Submit"] --> B["Validate"]
    B -->|Valid| C["Store"]
    B -->|Error| D["Reject"]
    C --> E["Wait 5 min"]
    E --> F["Detector"]
    F -->|Normal| G["✅ Done"]
    F -->|Anomaly| H["Alert → Email"]
    H --> I["📊 Dashboard"]
    G --> I
```

---

## 📝 Components

| File | Purpose |
|------|---------|
| `urls.py` | URL routing |
| `views.py` | Requests |
| `models.py` | Database |
| `serializers.py` | Validation |
| `anomaly_engine.py` | Detection |
| `alerts.py` | Email |

---

**Threshold**: 5 errors | **Interval**: 5 min | **Mail**: Gmail
