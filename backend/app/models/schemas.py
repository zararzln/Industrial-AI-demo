from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class EquipmentStatus(str, Enum):
    """Equipment operational status."""
    OPERATIONAL = "operational"
    WARNING = "warning"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Equipment(BaseModel):
    """Equipment model."""
    id: str
    name: str
    type: str
    location: str
    status: EquipmentStatus
    health_score: float = Field(..., ge=0, le=100)
    last_maintenance: datetime
    next_maintenance: datetime
    metrics: Dict[str, float]


class SensorReading(BaseModel):
    """Sensor reading model."""
    equipment_id: str
    timestamp: datetime
    temperature: float
    pressure: float
    vibration: float
    power_consumption: float


class MaintenanceLog(BaseModel):
    """Maintenance log entry."""
    id: str
    equipment_id: str
    timestamp: datetime
    type: str
    description: str
    technician: str
    cost: float
    duration_hours: float


class Alert(BaseModel):
    """Equipment alert model."""
    id: str
    equipment_id: str
    timestamp: datetime
    severity: AlertSeverity
    type: str
    message: str
    resolved: bool = False


class QueryRequest(BaseModel):
    """AI query request."""
    query: str
    equipment_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """AI query response."""
    answer: str
    sources: List[str] = []
    recommendations: List[str] = []
    confidence: float = Field(..., ge=0, le=1)
    agent_reasoning: Optional[str] = None


class DashboardMetrics(BaseModel):
    """Executive dashboard metrics."""
    total_equipment: int
    operational_count: int
    warning_count: int
    critical_count: int
    average_health_score: float
    total_alerts: int
    unresolved_alerts: int
    maintenance_cost_mtd: float
    energy_efficiency: float
    predicted_failures: List[Dict[str, Any]]


class OperatorMetrics(BaseModel):
    """Operator dashboard metrics."""
    equipment: List[Equipment]
    recent_alerts: List[Alert]
    pending_maintenance: List[Dict[str, Any]]
    shift_summary: Dict[str, Any]
