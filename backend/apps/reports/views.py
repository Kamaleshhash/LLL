from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

from apps.records.models import CaseRecord


class CaseSummaryPDFView(APIView):
    def get(self, request, cnr_number):
        case = CaseRecord.objects.filter(cnr_number=cnr_number).first()
        if not case:
            return Response({'detail': 'Case not found'}, status=404)

        buf = BytesIO()
        pdf = canvas.Canvas(buf, pagesize=A4)
        pdf.setFont('Helvetica-Bold', 14)
        pdf.drawString(40, 800, 'Land Litigation Case Summary')
        pdf.setFont('Helvetica', 11)
        rows = [
            f'CNR: {case.cnr_number}',
            f'Court: {case.court_name}',
            f'Case Type: {case.case_type}',
            f'Parties: {case.petitioner} vs {case.respondent}',
            f'Status: {case.status} | Stage: {case.stage}',
            f'Filing Date: {case.filing_date}',
            f'Last Hearing: {case.last_hearing_date}',
            f'Next Hearing: {case.next_hearing_date}',
            f'Risk Score: {case.risk_score}',
        ]
        y = 770
        for row in rows:
            pdf.drawString(40, y, row)
            y -= 22
        pdf.showPage()
        pdf.save()

        content = buf.getvalue()
        buf.close()
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={cnr_number}_summary.pdf'
        return response
