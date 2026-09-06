from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


# Event schemas
class EventCreate(BaseModel):
    """Schema for creating an event."""
    agent_id: int
    category: str
    event_type: str  # using type instead of reserved word
    action: str
    outcome: str
    severity: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    destination_port: Optional[int] = None
    timestamp: datetime
    raw_data: Optional[Dict[str, Any]] = None


class EventResponse(BaseModel):
    """Schema for event response."""
    id: int
    event_id: str
    agent_id: int
    category: str
    event_type: str
    action: str
    outcome: str
    severity: Optional[str]
    source_ip: Optional[str]
    destination_ip: Optional[str]
    destination_port: Optional[int]
    timestamp: datetime
    raw_data: Optional[Dict[str, Any]]
    processed: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Agent schemas
class AgentCreate(BaseModel):
    """Schema for creating an agent."""
    agent_id: str
    name: str
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    os: str
    os_version: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None


class AgentResponse(BaseModel):
    """Schema for agent response."""
    id: int
    agent_id: str
    name: str
    hostname: Optional[str]
    ip_address: Optional[str]
    os: str
    os_version: Optional[str]
    status: str
    last_heartbeat: Optional[datetime]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Alert schemas
class AlertCreate(BaseModel):
    """Schema for creating an alert."""
    agent_id: int
    title: str
    description: Optional[str] = None
    severity: str
    mitre_tactic: Optional[str] = None
    mitre_technique_id: Optional[str] = None


class AlertResponse(BaseModel):
    """Schema for alert response."""
    id: int
    alert_id: str
    agent_id: int
    title: str
    description: Optional[str]
    severity: str
    status: str
    mitre_tactic: Optional[str]
    mitre_technique_id: Optional[str]
    created_at: datetime
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


# Rule schemas
class RuleCreate(BaseModel):
    """Schema for creating a detection rule."""
    name: str
    version: str = "1.0.0"
    enabled: bool = True
    severity: str
    condition: Dict[str, Any]
    mitre_tactic: Optional[str] = None
    mitre_technique_id: Optional[str] = None


class RuleResponse(BaseModel):
    """Schema for rule response."""
    id: int
    rule_id: str
    name: str
    version: str
    enabled: bool
    severity: str
    condition: Dict[str, Any]
    mitre_tactic: Optional[str]
    mitre_technique_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


# Incident schemas
class IncidentCreate(BaseModel):
    """Schema for creating an incident."""
    title: str
    description: Optional[str] = None
    severity: str
    owner_id: Optional[int] = None


class IncidentResponse(BaseModel):
    """Schema for incident response."""
    id: int
    incident_id: str
    title: str
    description: Optional[str]
    severity: str
    status: str
    owner_id: Optional[int]
    related_alert_ids: List[str]
    evidence: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Health check schemas
class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    timestamp: datetime
    version: str = "0.1.0"


class ReadyCheck(BaseModel):
    """Schema for readiness check."""
    status: str
    checks: Dict[str, str]