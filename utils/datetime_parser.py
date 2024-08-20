from datetime import datetime


def to_iso(date=datetime.now()):
    """Convert datetime object to ISO format"""
    return date.isoformat()


def from_iso(date):
    """Parse datetime object from ISO format"""
    return datetime.fromisoformat(date)
