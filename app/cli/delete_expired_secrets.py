import argparse
import sys

from app.database import SessionLocal
from app.service.secrets import delete_expired_secrets


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Doesn't delete expired secrets. Just counts them.")
    
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        with SessionLocal() as session:
            amount = delete_expired_secrets(session, args.dry_run)

        if args.dry_run:
            print(f"Expired secrets: {amount}")
        else:
            print(f"Deleted expired secrets: {amount}")

    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
