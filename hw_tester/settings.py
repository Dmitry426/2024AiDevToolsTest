import os
from dataclasses import dataclass, field

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

@dataclass
class UvicornURL :
    host: str = field(default="127.0.0.1")
    port: str = field(default="8000")

    @classmethod
    def from_env(cls) -> "UvicornURL":
        """Create an instance of UvicornURL using environment variables."""
        host = os.getenv("UVICORN_HOST", cls.__dataclass_fields__["host"].default)
        port = os.getenv("UVICORN_PORT", cls.__dataclass_fields__["port"].default)
        return cls(host=host, port=port)

