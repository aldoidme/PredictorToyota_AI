from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_dashboard(
    context: Mapping[str, Any],
    template_path: str | Path,
    output_path: str | Path,
) -> Path:
    """Renderiza el dashboard HTML con Jinja2."""

    template_path = Path(template_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_path.name)

    html = template.render(**context)
    output_path.write_text(html, encoding="utf-8")
    return output_path
