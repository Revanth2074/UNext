"""Pydantic models for ticket requests and responses."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    """Schema for creating a new ticket."""

    ticket_id: str = Field(..., description="Unique ticket identifier (e.g. T-1001)")
    customer_name: str = Field(..., description="Name of the customer")
    category: str = Field(..., description="Category of the ticket")
    priority_raw: str = Field(..., description="Raw priority (low, medium, high, critical)")
    created_at: str = Field(..., description="Creation date in format YYYY-MM-DD HH:MM:SS")
    sla_hours: int = Field(..., gt=0, description="Allowed SLA resolution time in hours")
    status: str = Field(..., description="Current status of the ticket (e.g. open, closed)")


class TicketUpdate(BaseModel):
    """Schema for updating an existing ticket's status and/or priority_raw."""

    priority_raw: Optional[str] = Field(None, description="Updated raw priority (low, medium, high, critical)")
    status: Optional[str] = Field(None, description="Updated ticket status (e.g. open, closed)")


class TicketResponse(BaseModel):
    """Schema representing a processed ticket response."""

    ticket_id: str
    customer_name: str
    category: str
    priority_raw: str
    priority_score: int
    created_at: str
    sla_hours: int
    status: str
    sla_breached: bool

    class Config:
        """Pydantic config configuration."""
        from_attributes = True
