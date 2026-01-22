from fastapi import APIRouter
from typing import List

from app.models.schemas import DashboardMetrics, OperatorMetrics, Alert
from app.services.data_service import get_data_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/executive", response_model=DashboardMetrics)
async def get_executive_dashboard():
    """
    Get executive dashboard metrics.
    
    Returns high-level KPIs including:
    - Equipment health overview
    - Alert statistics
    - Maintenance costs
    - Predicted failures
    """
    data_service = get_data_service()
    return data_service.get_dashboard_metrics()


@router.get("/operator", response_model=OperatorMetrics)
async def get_operator_dashboard():
    """
    Get operator dashboard metrics.
    
    Returns operational data including:
    - Equipment list with current status
    - Recent alerts
    - Pending maintenance tasks
    - Shift summary
    """
    data_service = get_data_service()
    return data_service.get_operator_metrics()


@router.get("/alerts", response_model=List[Alert])
async def get_all_alerts(resolved: bool = None):
    """Get all system alerts with optional filtering."""
    data_service = get_data_service()
    return data_service.get_alerts(resolved=resolved)


@router.patch("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    """Mark an alert as resolved."""
    data_service = get_data_service()
    success = data_service.update_alert_status(alert_id, resolved=True)
    
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {"message": "Alert resolved successfully", "alert_id": alert_id}
