import json
from pathlib import Path

from django.db.models import Q

from landlitigation.utils import fuzzy_score, make_verification_hash, normalize_survey_number, normalize_village_name, parse_date
from apps.records.models import CaseEvent, CaseRecord, LandParcel, ParcelCaseLink, VerificationLog

DATA_DIR = Path(__file__).resolve().parents[2] / 'data'


def load_mock_data():
    land_path = DATA_DIR / 'mock_land_records.json'
    case_path = DATA_DIR / 'mock_case_records.json'

    if not land_path.exists() or not case_path.exists():
        return

    lands = json.loads(land_path.read_text(encoding='utf-8'))
    cases = json.loads(case_path.read_text(encoding='utf-8'))

    case_map = {}
    for case_data in cases:
        case_obj, _ = CaseRecord.objects.update_or_create(
            cnr_number=case_data['cnr_number'],
            defaults={
                'case_type': case_data['case_type'],
                'court_name': case_data['court_name'],
                'petitioner': case_data['petitioner'],
                'respondent': case_data['respondent'],
                'filing_date': parse_date(case_data.get('filing_date')),
                'last_hearing_date': parse_date(case_data.get('last_hearing_date')),
                'next_hearing_date': parse_date(case_data.get('next_hearing_date')),
                'status': case_data['status'],
                'stage': case_data.get('stage', ''),
                'order_pdf_url': case_data.get('order_pdf_url', ''),
                'summary': case_data.get('summary', ''),
                'risk_score': case_data.get('risk_score', 0.0),
            },
        )
        CaseEvent.objects.filter(case=case_obj).delete()
        for event in case_data.get('events', []):
            CaseEvent.objects.create(
                case=case_obj,
                event_date=parse_date(event['event_date']),
                title=event['title'],
                description=event.get('description', ''),
            )
        case_map[case_obj.cnr_number] = case_obj

    for land in lands:
        payload_hash = make_verification_hash(land)
        parcel, _ = LandParcel.objects.update_or_create(
            state=land['state'],
            district=land['district'],
            village_name=land['village_name'],
            survey_number=land['survey_number'],
            owner_name=land['owner_name'],
            defaults={
                'taluk': land.get('taluk', ''),
                'area_hectare': land['area_hectare'],
                'land_type': land['land_type'],
                'geojson_boundary': land.get('geojson_boundary', {}),
                'ror_reference': land.get('ror_reference', ''),
                'verification_hash': payload_hash,
            },
        )
        VerificationLog.objects.get_or_create(
            source_system='Mock-RoR',
            source_reference=land.get('ror_reference', parcel.survey_number),
            payload_hash=payload_hash,
            defaults={'signature': f'mock-signature-{payload_hash[:12]}'},
        )
        for cnr in land.get('linked_cases', []):
            case_obj = case_map.get(cnr)
            if case_obj:
                ParcelCaseLink.objects.update_or_create(parcel=parcel, case=case_obj, defaults={'is_primary': True})


def filter_case_links(parcel, case_type='', status='', from_date=None, to_date=None):
    links = parcel.case_links.select_related('case').all()
    if case_type:
        links = links.filter(case__case_type__icontains=case_type)
    if status:
        links = links.filter(case__status=status)
    if from_date:
        links = links.filter(case__filing_date__gte=from_date)
    if to_date:
        links = links.filter(case__filing_date__lte=to_date)
    return links


def search_parcels(state, district, village_name, survey_number):
    village_normalized = normalize_village_name(village_name)
    survey_normalized = normalize_survey_number(survey_number)

    candidates = LandParcel.objects.filter(state__iexact=state, district__iexact=district)
    exact = candidates.filter(survey_number__iexact=survey_normalized, village_name__iexact=village_name)
    if exact.exists():
        return exact, []

    ranked = []
    for parcel in candidates.filter(survey_number__iexact=survey_normalized):
        score = fuzzy_score(parcel.village_name, village_normalized)
        if score >= 0.55:
            ranked.append((score, parcel.id))

    ranked.sort(reverse=True)
    ids = [item[1] for item in ranked]
    return LandParcel.objects.filter(id__in=ids), ranked


def autocomplete_village(state, district, query):
    query = normalize_village_name(query)
    villages = LandParcel.objects.filter(state__iexact=state, district__iexact=district).values_list('village_name', flat=True).distinct()
    scored = sorted(((fuzzy_score(v, query), v) for v in villages), reverse=True)
    return [v for score, v in scored if score >= 0.45][:10]


def semantic_search(query):
    q = query.lower()
    case_filter = Q()
    if 'encroachment' in q:
        case_filter |= Q(case_type__icontains='encroachment')
    if 'title' in q:
        case_filter |= Q(case_type__icontains='title')
    if 'pending' in q:
        case_filter |= Q(status='pending')
    if 'veerapandi' in q:
        case_filter |= Q(parcel_links__parcel__village_name__icontains='veerapandi')

    if not case_filter:
        case_filter = Q(status='pending')

    return CaseRecord.objects.filter(case_filter).distinct()[:30]
