from __future__ import annotations

try:
    from .pipeline import run_pipeline
except ImportError:  # fallback when running as script
    from pipeline import run_pipeline


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
