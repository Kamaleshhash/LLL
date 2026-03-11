import hashlib
import json
import re
from datetime import datetime
from difflib import SequenceMatcher


def normalize_village_name(name: str) -> str:
    return re.sub(r'\s+', ' ', (name or '').strip().lower())


def normalize_survey_number(value: str) -> str:
    return (value or '').strip().upper().replace(' ', '')


def fuzzy_score(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_village_name(a), normalize_village_name(b)).ratio()


def make_verification_hash(payload: dict) -> str:
    blob = json.dumps(payload, sort_keys=True, default=str).encode('utf-8')
    return hashlib.sha256(blob).hexdigest()


def parse_date(value: str):
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d').date()
