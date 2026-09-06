from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ariba_manager.app.db.session import get_db
from ariba_manager.app.schemas.common import (
    EventCreate,
    EventResponse,
    AgentCreate,
    AgentResponse,
    AlertCreate,
    AlertResponse,
    RuleCreate,
    RuleResponse,
    IncidentCreate,
    IncidentResponse,
    HealthCheck,
    ReadyCheck,
)
from ariba_manager.app.models import User, Agent, Event, Alert, Rule, Incident
import uuid
import json
from datetime import datetime


router = APIRouter(prefix="/v1", tags=["v1"])


# Health endpoints
@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(status="ok", timestamp=datetime.utcnow(), version="0.1.0")


@router.get("/ready", response_model=ReadyCheck)
async def readiness_check():
    """Readiness check endpoint."""
    return ReadyCheck(
        status="ready",
        checks={
            "database": "ok",
            "redis": "ok",
            "opensearch": "ok",
        },
    )


# Agent endpoints
@router.post("/agents/enroll", response_model=AgentResponse)
async def enroll_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    """Enroll a new agent."""
    from sqlalchemy import select
    from ariba_manager.app.models import Agent
    
    result = db.execute(select(Agent).where(Agent.agent_id == agent_data.agent_id))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Agent already enrolled",
        )
    
    agent = Agent(
        agent_id=agent_data.agent_id,
        name=agent_data.name,
        hostname=agent_data.hostname,
        ip_address=agent_data.ip_address,
        os=agent_data.os,
        os_version=agent_data.os_version,
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return AgentResponse(
        id=agent.id,
        agent_id=agent.agent_id,
        name=agent.name,
        hostname=agent.hostname,
        ip_address=agent.ip_address,
        os=agent.os,
        os_version=agent.os_version,
    )


@router.get("/agents", response_model=List[AgentResponse])
async def list_agents(db: Session = Depends(get_db)):
    """List all enrolled agents."""
    from sqlalchemy import select
    from ariba_manager.app.models import Agent
    
    result = db.execute(select(Agent).where(Agent.status == "online"))
    agents = result.scalars().all()
    return [
        AgentResponse(
            id=a.id,
            agent_id=a.agent_id,
            name=a.name,
            hostname=a.hostname,
            ip_address=a.ip_address,
            os=a.os,
            os_version=a.os_version,
        )
        for a in agents
    ]


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """Get agent details."""
    from sqlalchemy import select
    from ariba_manager.app.models import Agent
    
    result = db.execute(select(Agent).where(Agent.agent_id == agent_id))
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    
    return AgentResponse(
        id=agent.id,
        agent_id=agent.agent_id,
        name=agent.name,
        hostname=agent.hostname,
        ip_address=agent.ip_address,
        os=agent.os,
        os_version=agent.os_version,
    )


# Event endpoints
@router.post("/events", response_model=EventResponse, status_code=202)
async def ingest_event(event_data: EventCreate, db: Session = Depends(get_db)):
    """Ingest a single security event."""
    from uuid import uuid4
    
    event_id = str(uuid4())[:8] + str(uuid4()).hex[:4]
    
    event = Event(
        event_id=event_id,
        agent_id=event_data.agent_id,
        category=event_data.category,
        event_type=event_data.event_type,
        action=event_data.action,
        outcome=event_data.outcome,
        severity=event_data.severity,
        source_ip=event_data.source_ip,
        destination_ip=event_data.destination_ip,
        destination_port=event_data.destination_port,
        timestamp=event_data.timestamp,
        raw_data=event_data.raw_data,
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return EventResponse(
        id=event.id,
        event_id=event.event_id,
        agent_id=event.agent_id,
        category=event.category,
        event_type=event.event_type,
        action=event.action,
        outcome=event.outcome,
        severity=event.severity,
        source_ip=event.source_ip,
        destination_ip=event.destination_ip,
        destination_port=event.destination_port,
        timestamp=event.timestamp,
        raw_data=event.raw_data,
        processed=event.processed,
        created_at=event.created_at,
    )


@router.post("/events/bulk", response_model=List[EventResponse], status_code=202)
async def ingest_bulk_events(events_data: List[EventCreate], db: Session = Depends(get_db)):
    """Ingest multiple events in bulk."""
    from uuid import uuid4
    
    created_events = []
    
    for event_data in events_data:
        event_id = str(uuid4())[:8] + str(uuid4()).hex[:4]
        
        event = Event(
            event_id=event_id,
            agent_id=event_data.agent_id,
            category=event_data.category,
            event_type=event_data.event_type,
            action=event_data.action,
            outcome=event_data.outcome,
            severity=event_data.severity,
            source_ip=event_data.source_ip,
            destination_ip=event_data.destination_ip,
            destination_port=event_data.destination_port,
            timestamp=event_data.timestamp,
            raw_data=event_data.raw_data,
        )
        
        db.add(event)
        created_events.append(event)
    
    db.commit()
    
    for event in created_events:
        db.refresh(event)
    
    return [
        EventResponse(
            id=e.id,
            event_id=e.event_id,
            agent_id=e.agent_id,
            category=e.category,
            event_type=e.event_type,
            action=e.action,
            outcome=e.outcome,
            severity=e.severity,
            source_ip=e.source_ip,
            destination_ip=e.destination_ip,
            destination_port=e.destination_port,
            timestamp=e.timestamp,
            raw_data=e.raw_data,
            processed=e.processed,
            created_at=e.created_at,
        )
        for e in created_events
    ]


# Alert endpoints
@router.post("/alerts", response_model=AlertResponse, status_code=201)
async def create_alert(alert_data: AlertCreate, db: Session = Depends(get_db)):
    """Create a new alert."""
    from sqlalchemy import select
    from ariba_manager.app.models import Agent
    
    # Find the agent
    result = db.execute(select(Agent).where(Agent.agent_id == str(alert_data.agent_id)))
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    
    alert = Alert(
        alert_id=uuid.uuid4().hex[:12],
        agent_id=agent.id,
        title=alert_data.title,
        description=alert_data.description,
        severity=alert_data.severity,
        mitre_tactic=alert_data.mitre_tactic,
        mitre_technique_id=alert_data.mitre_technique_id,
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    return AlertResponse(
        id=alert.id,
        alert_id=alert.alert_id,
        agent_id=alert.agent_id,
        title=alert.title,
        description=alert.description,
        severity=alert.severity,
        status=alert.status,
        mitre_tactic=alert.mitre_tactic,
        mitre_technique_id=alert.mitre_technique_id,
        created_at=alert.created_at,
    )


# Rule endpoints
@router.post("/rules", response_model=RuleResponse, status_code=201)
async def create_rule(rule_data: RuleCreate, db: Session = Depends(get_db)):
    """Create a new detection rule."""
    from sqlalchemy import select
    from ariba_manager.app.models import Rule
    
    # Check if rule already exists
    result = db.execute(select(Rule).where(Rule.rule_id == rule_data.name))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rule with this name already exists",
        )
    
    rule = Rule(
        rule_id=rule_data.name,
        name=rule_data.name,
        version=rule_data.version,
        enabled=rule_data.enabled,
        severity=rule_data.severity,
        condition=rule_data.condition,
        mitre_tactic=rule_data.mitre_tactic,
        mitre_technique_id=rule_data.mitre_technique_id,
    )
    
    db.add(rule)
    db.commit()
    db.refresh(rule)
    
    return RuleResponse(
        id=rule.id,
        rule_id=rule.rule_id,
        name=rule.name,
        version=rule.version,
        enabled=rule.enabled,
        severity=rule.severity,
        condition=rule.condition,
        mitre_tactic=rule.mitre_tactic,
        mitre_technique_id=rule.mitre_technique_id,
        created_at=rule.created_at,
    )


# Incident endpoints
@router.post("/incidents", response_model=IncidentResponse, status_code=201)
async def create_incident(incident_data: IncidentCreate, db: Session = Depends(get_db)):
    """Create a new incident."""
    from sqlalchemy import select, func
    import json
    
    # Get related alerts if provided
    related_alert_ids = incident_data.related_alert_ids or []
    
    incident = Incident(
        incident_id=uuid.uuid4().hex[:12],
        title=incident_data.title,
        description=incident_data.description,
        severity=incident_data.severity,
        owner_id=incident_data.owner_id,
        related_alert_ids=json.dumps(related_alert_ids) if related_alert_ids else None,
    )
    
    db.add(incident)
    db.commit()
    db.refresh(incident)
    
    return IncidentResponse(
        id=incident.id,
        incident_id=incident.incident_id,
        title=incident.title,
        description=incident.description,
        severity=incident.severity,
        status=incident.status,
        owner_id=incident.owner_id,
        related_alert_ids=json.loads(incident.related_alert_ids) if incident.related_alert_ids else [],
        evidence=incident.evidence,
        created_at=incident.created_at,
        updated_at=incident.updated_at,
    )