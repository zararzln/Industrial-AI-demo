import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

from app.models.schemas import (
    Equipment, SensorReading, MaintenanceLog, Alert,
    EquipmentStatus, AlertSeverity, DashboardMetrics, OperatorMetrics
)

logger = logging.getLogger(__name__)


class DataService:
    """Service for managing industrial data."""
    
    def __init__(self):
        """Initialize data service with in-memory storage."""
        self.equipment: Dict[str, Equipment] = {}
        self.sensor_readings: List[SensorReading] = []
        self.maintenance_logs: List[MaintenanceLog] = []
        self.alerts: List[Alert] = []
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with realistic sample data."""
        # Sample equipment
        equipment_data = [
            {
                "id": "COMP-001",
                "name": "Air Compressor Unit 1",
                "type": "Compressor",
                "location": "Building A - Floor 1",
                "status": EquipmentStatus.OPERATIONAL,
                "health_score": 87.5,
                "metrics": {
                    "temperature": 72.3,
                    "pressure": 120.5,
                    "vibration": 0.8,
                    "efficiency": 89.2
                }
            },
            {
                "id": "TURB-003",
                "name": "Gas Turbine 3",
                "type": "Turbine",
                "location": "Power Plant - Section B",
                "status": EquipmentStatus.WARNING,
                "health_score": 72.1,
                "metrics": {
                    "temperature": 485.2,
                    "pressure": 340.8,
                    "vibration": 2.3,
                    "efficiency": 76.4
                }
            },
            {
                "id": "PUMP-007",
                "name": "Hydraulic Pump 7",
                "type": "Pump",
                "location": "Building C - Floor 2",
                "status": EquipmentStatus.CRITICAL,
                "health_score": 45.8,
                "metrics": {
                    "temperature": 95.7,
                    "pressure": 85.2,
                    "vibration": 4.5,
                    "efficiency": 58.3
                }
            },
            {
                "id": "CONV-012",
                "name": "Conveyor Belt 12",
                "type": "Conveyor",
                "location": "Warehouse - Zone 3",
                "status": EquipmentStatus.OPERATIONAL,
                "health_score": 91.2,
                "metrics": {
                    "temperature": 45.3,
                    "pressure": 0.0,
                    "vibration": 0.5,
                    "efficiency": 94.7
                }
            },
            {
                "id": "HVAC-005",
                "name": "HVAC System 5",
                "type": "HVAC",
                "location": "Building B - Floor 3",
                "status": EquipmentStatus.MAINTENANCE,
                "health_score": 68.5,
                "metrics": {
                    "temperature": 22.5,
                    "pressure": 14.7,
                    "vibration": 0.3,
                    "efficiency": 82.1
                }
            }
        ]
        
        now = datetime.now()
        for eq_data in equipment_data:
            equipment = Equipment(
                **eq_data,
                last_maintenance=now - timedelta(days=random.randint(10, 90)),
                next_maintenance=now + timedelta(days=random.randint(5, 30))
            )
            self.equipment[equipment.id] = equipment
        
        # Generate sample alerts
        self.alerts = [
            Alert(
                id="ALT-001",
                equipment_id="PUMP-007",
                timestamp=now - timedelta(hours=2),
                severity=AlertSeverity.CRITICAL,
                type="High Vibration",
                message="Vibration levels exceeded threshold (4.5mm/s)",
                resolved=False
            ),
            Alert(
                id="ALT-002",
                equipment_id="TURB-003",
                timestamp=now - timedelta(hours=5),
                severity=AlertSeverity.MEDIUM,
                type="Temperature Warning",
                message="Operating temperature higher than normal range",
                resolved=False
            ),
            Alert(
                id="ALT-003",
                equipment_id="COMP-001",
                timestamp=now - timedelta(days=1),
                severity=AlertSeverity.LOW,
                type="Efficiency Drop",
                message="Efficiency decreased by 3% over last 24 hours",
                resolved=True
            )
        ]
        
        # Generate sample maintenance logs
        self.maintenance_logs = [
            MaintenanceLog(
                id="MNT-001",
                equipment_id="TURB-003",
                timestamp=now - timedelta(days=45),
                type="Preventive",
                description="Routine turbine blade inspection and lubrication",
                technician="John Smith",
                cost=2500.00,
                duration_hours=4.5
            ),
            MaintenanceLog(
                id="MNT-002",
                equipment_id="PUMP-007",
                timestamp=now - timedelta(days=60),
                type="Corrective",
                description="Replaced worn bearing assembly",
                technician="Sarah Johnson",
                cost=1800.00,
                duration_hours=6.0
            )
        ]
        
        logger.info(f"Initialized {len(self.equipment)} equipment items")
    
    def get_all_equipment(self) -> List[Equipment]:
        """Get all equipment."""
        return list(self.equipment.values())
    
    def get_equipment(self, equipment_id: str) -> Optional[Equipment]:
        """Get specific equipment by ID."""
        return self.equipment.get(equipment_id)
    
    def get_equipment_by_status(self, status: EquipmentStatus) -> List[Equipment]:
        """Get equipment filtered by status."""
        return [eq for eq in self.equipment.values() if eq.status == status]
    
    def get_alerts(
        self, 
        equipment_id: Optional[str] = None,
        resolved: Optional[bool] = None
    ) -> List[Alert]:
        """Get alerts with optional filtering."""
        alerts = self.alerts
        
        if equipment_id:
            alerts = [a for a in alerts if a.equipment_id == equipment_id]
        
        if resolved is not None:
            alerts = [a for a in alerts if a.resolved == resolved]
        
        return sorted(alerts, key=lambda x: x.timestamp, reverse=True)
    
    def get_maintenance_logs(
        self,
        equipment_id: Optional[str] = None,
        limit: int = 10
    ) -> List[MaintenanceLog]:
        """Get maintenance logs."""
        logs = self.maintenance_logs
        
        if equipment_id:
            logs = [log for log in logs if log.equipment_id == equipment_id]
        
        return sorted(logs, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_dashboard_metrics(self) -> DashboardMetrics:
        """Get executive dashboard metrics."""
        equipment_list = list(self.equipment.values())
        alerts_list = self.alerts
        
        operational = len([e for e in equipment_list if e.status == EquipmentStatus.OPERATIONAL])
        warning = len([e for e in equipment_list if e.status == EquipmentStatus.WARNING])
        critical = len([e for e in equipment_list if e.status == EquipmentStatus.CRITICAL])
        
        avg_health = sum(e.health_score for e in equipment_list) / len(equipment_list) if equipment_list else 0
        
        unresolved_alerts = len([a for a in alerts_list if not a.resolved])
        
        # Calculate MTD maintenance cost
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        mtd_cost = sum(
            log.cost for log in self.maintenance_logs 
            if log.timestamp >= month_start
        )
        
        # Mock predicted failures (in production, this would use ML models)
        predicted_failures = [
            {
                "equipment_id": "PUMP-007",
                "equipment_name": "Hydraulic Pump 7",
                "failure_probability": 0.78,
                "estimated_days": 7,
                "reason": "High vibration and degraded bearing condition"
            },
            {
                "equipment_id": "TURB-003",
                "equipment_name": "Gas Turbine 3",
                "failure_probability": 0.45,
                "estimated_days": 21,
                "reason": "Elevated operating temperature"
            }
        ]
        
        return DashboardMetrics(
            total_equipment=len(equipment_list),
            operational_count=operational,
            warning_count=warning,
            critical_count=critical,
            average_health_score=round(avg_health, 1),
            total_alerts=len(alerts_list),
            unresolved_alerts=unresolved_alerts,
            maintenance_cost_mtd=mtd_cost,
            energy_efficiency=85.3,
            predicted_failures=predicted_failures
        )
    
    def get_operator_metrics(self) -> OperatorMetrics:
        """Get operator dashboard metrics."""
        recent_alerts = self.get_alerts(resolved=False)[:5]
        
        # Get pending maintenance
        now = datetime.now()
        pending_maintenance = []
        for eq in self.equipment.values():
            days_until = (eq.next_maintenance - now).days
            if days_until <= 14:
                pending_maintenance.append({
                    "equipment_id": eq.id,
                    "equipment_name": eq.name,
                    "due_date": eq.next_maintenance.isoformat(),
                    "days_until": days_until,
                    "type": "Scheduled Preventive Maintenance"
                })
        
        # Shift summary
        shift_summary = {
            "shift_start": (now - timedelta(hours=8)).isoformat(),
            "alerts_generated": 3,
            "alerts_resolved": 1,
            "equipment_interactions": 12,
            "average_response_time_minutes": 15.3
        }
        
        return OperatorMetrics(
            equipment=list(self.equipment.values()),
            recent_alerts=recent_alerts,
            pending_maintenance=pending_maintenance,
            shift_summary=shift_summary
        )
    
    def update_alert_status(self, alert_id: str, resolved: bool) -> bool:
        """Update alert resolved status."""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = resolved
                return True
        return False


# Global data service instance
data_service: Optional[DataService] = None


def get_data_service() -> DataService:
    """Get or create data service instance."""
    global data_service
    if data_service is None:
        data_service = DataService()
    return data_service
