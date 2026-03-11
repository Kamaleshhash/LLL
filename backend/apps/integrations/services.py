"""Production integration placeholders.

Replace stubs with signed API clients for:
- State RoR systems (e.g., TNREGINET / E-Sevai / Bhulekh variants)
- eCourts and NJDG metadata feeds
- webhook listeners for case status updates
"""


def fetch_land_record(*_args, **_kwargs):
    return {'status': 'stub'}


def fetch_case_record(*_args, **_kwargs):
    return {'status': 'stub'}
