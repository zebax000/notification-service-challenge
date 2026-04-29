import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable

from app.services.util import generate_unique_id
