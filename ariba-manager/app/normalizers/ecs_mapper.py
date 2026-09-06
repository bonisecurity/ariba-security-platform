from typing import Any, Dict, Optional
from datetime import datetime


class ECSMapper:
    """Maps raw events to Elastic Common Schema (ECS)."""
    
    @staticmethod
    def map_event(raw_event: Dict[str, Any]) -> Dict[str, Any]:
        """Map a raw event to ECS format."""
        event: Dict[str, Any] = {
            "@timestamp": raw_event.get("@timestamp", datetime.utcnow().isoformat()),
            "event": {
                "category": raw_event.get("event", {}).get("category"),
                "type": raw_event.get("event", {}).get("type"),
                "action": raw_event.get("event", {}).get("action"),
                "outcome": raw_event.get("event", {}).get("outcome"),
            },
            "agent": {
                "id": raw_event.get("agent", {}).get("id"),
                "name": raw_event.get("agent", {}).get("name"),
                "ip": raw_event.get("agent", {}).get("ip"),
            },
            "source": {
                "ip": raw_event.get("source", {}).get("ip"),
            },
            "destination": {
                "ip": raw_event.get("destination", {}).get("ip"),
                "port": raw_event.get("destination", {}).get("port"),
            },
            "observer": {
                "product": raw_event.get("observer", {}).get("product"),
            },
            "tags": ["ariba", raw_event.get("event", {}).get("category", "unknown")],
        }
        
        # Add HTTP details if present
        if "http" in raw_event:
            event["http"] = {
                "method": raw_event["http"].get("method"),
                "url": raw_event["http"].get("url"),
                "response": {
                    "status_code": raw_event["http"].get("response", {}).get("status_code"),
                }
            }
        
        return event


mapper = ECSMapper()