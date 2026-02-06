# 🔄 System Workflow Diagram

This diagram shows how logs are processed and alerts are generated.

```mermaid
graph TB
    USER["👤 User / Application"]
    API["🔌 Log API"]
    BACKEND["🐍 Django Backend"]
    DB[(🗄️ Database)]
    DETECTOR["🔍 Anomaly Detector"]
    EMAIL["📧 Email Alert"]
    DASH["📊 Dashboard"]

    USER --> API
    API --> BACKEND
    BACKEND --> DB
    DB --> DETECTOR
    DETECTOR --> EMAIL
    DB --> DASH

    DETECTOR -->|Every 5 min| DB
    DB -->|Count Errors| DETECTOR
