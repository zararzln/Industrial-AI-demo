from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models.schemas import Equipment, Alert, MaintenanceLog, EquipmentStatus
from app.services.data_service import get_data_service

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("/", response_model=List[Equipment])
async def get_all_equipment():
    """Get all equipment."""
    data_service = get_data_service()
    return data_service.get_all_equipment()


@router.get("/{equipment_id}", response_model=Equipment)
async def get_equipment(equipment_id: str):
    """Get specific equipment by ID."""
    data_service = get_data_service()
    equipment = data_service.get_equipment(equipment_id)
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return equipment


@router.get("/status/{status}", response_model=List[Equipment])
async def get_equipment_by_status(status: EquipmentStatus):
    """Get equipment filtered by status."""
    data_service = get_data_service()
    return data_service.get_equipment_by_status(status)


@router.get("/{equipment_id}/alerts", response_model=List[Alert])
async def get_equipment_alerts(
    equipment_id: str,
    resolved: Optional[bool] = Query(None, description="Filter by resolved status")
):
    """Get alerts for specific equipment."""
    data_service = get_data_service()
    
    # Verify equipment exists
    if not data_service.get_equipment(equipment_id):
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return data_service.get_alerts(equipment_id=equipment_id, resolved=resolved)


@router.get("/{equipment_id}/maintenance", response_model=List[MaintenanceLog])
async def get_equipment_maintenance(
    equipment_id: str,
    limit: int = Query(10, ge=1, le=100)
):
    """Get maintenance history for specific equipment."""
    data_service = get_data_service()
    
    # Verify equipment exists
    if not data_service.get_equipment(equipment_id):
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return data_service.get_maintenance_logs(equipment_id=equipment_id, limit=limit)
