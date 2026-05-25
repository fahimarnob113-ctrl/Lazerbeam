from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


CONFIG_PATH = Path("lazerbeam_config.json")


@dataclass(slots=True)
class AppConfig:
    vault_path: str = ""
    organization_mode: str = "auto"
    manual_folder: str = "lazerbeam-inbox"
    duplicate_strategy: str = "append"
    debug: bool = False
    features: dict[str, bool] = field(
        default_factory=lambda: {
            "browser_server": False,
            "tray": False,
            "ai_summary": False,
        }
    )


def load_config(path: Path = CONFIG_PATH) -> AppConfig:
    if not path.exists():
        return AppConfig()
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return AppConfig(**{**asdict(AppConfig()), **data})


def save_config(config: AppConfig, path: Path = CONFIG_PATH) -> None:
    path.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")
