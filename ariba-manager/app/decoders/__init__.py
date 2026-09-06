from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class BaseDecoder(ABC):
    """Base class for all log decoders."""
    
    @abstractmethod
    def decode(self, raw_data: str) -> Dict[str, Any]:
        """Decode raw log data into a normalized event dict.
        
        Args:
            raw_data: The raw log line or payload to decode
            
        Returns:
            A dict representing the normalized event, or None if decoding fails
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable decoder name."""
        pass
    
    @property
    @abstractmethod
    def supported_formats(self) -> list:
        """List of supported log formats/file types."""
        pass


class DecoderRegistry:
    """Registry for managing registered decoders."""
    
    def __init__(self):
        self._decoders: Dict[str, BaseDecoder] = {}
    
    def register(self, decoder: BaseDecoder, name: str = None) -> None:
        """Register a decoder.
        
        Args:
            decoder: The decoder instance to register
            name: Optional name to register under (defaults to decoder.name)
        """
        decoder_name = name or decoder.name
        self._decoders[decoder_name] = decoder
    
    def get(self, name: str) -> Optional[BaseDecoder]:
        """Get a decoder by name.
        
        Args:
            name: The decoder name to look up
            
        Returns:
            The decoder instance, or None if not found
        """
        return self._decoders.get(name)
    
    def get_all(self) -> Dict[str, BaseDecoder]:
        """Get all registered decoders."""
        return self._decoders.copy()
    
    def unregister(self, name: str) -> None:
        """Unregister a decoder."""
        self._decoders.pop(name, None)


# Global registry instance
registry = DecoderRegistry()