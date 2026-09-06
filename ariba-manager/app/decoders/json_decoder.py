from ..decoders import BaseDecoder, registry
from typing import Any, Dict, Optional
import json


class JsonDecoder(BaseDecoder):
    """Decoder for JSON-formatted log data."""
    
    @property
    def name(self) -> str:
        return "json"
    
    @property
    def supported_formats(self) -> list:
        return ["json", "application/json"]
    
    def decode(self, raw_data: str) -> Optional[Dict[str, Any]]:
        """Decode a JSON-formatted string into a normalized event."""
        try:
            data = json.loads(raw_data.strip())
            # Normalize to Ariba event format
            event: Dict[str, Any] = {
                "@timestamp": data.get("@timestamp", ""),
                "event": {
                    "id": data.get("event", {}).get("id", ""),
                    "category": data.get("event", {}).get("category", ""),
                    "type": data.get("event", {}).get("type", ""),
                    "action": data.get("event", {}).get("action", ""),
                    "outcome": data.get("event", {}).get("outcome", ""),
                },
                "agent": {
                    "id": data.get("agent", {}).get("id", ""),
                    "name": data.get("agent", {}).get("name", ""),
                    "ip": data.get("agent", {}).get("ip", ""),
                },
                "source": {
                    "ip": data.get("source", {}).get("ip", ""),
                },
                "destination": {
                    "ip": data.get("destination", {}).get("ip", ""),
                    "port": data.get("destination", {}).get("port"),
                },
                "observer": {
                    "product": data.get("observer", {}).get("product", ""),
                },
            }
            return event
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            # Log error but return None for malformed data
            return None


# Register the decoder
registry.register(JsonDecoder(), name="json")