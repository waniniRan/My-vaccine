from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from HealthcareW.models.GrowthRecord import GrowthRecord
from HealthcareW.models.Child import Child
from HealthcareW.models.Guardian import Guardian
from datetime import datetime

class GrowthCurveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            guardian = Guardian.objects.get(user=request.user)
            child = Child.objects.get(child_id=child_id, guardian=guardian)
        except (Guardian.DoesNotExist, Child.DoesNotExist):
            return Response({'detail': 'Child not found or not owned by guardian.'}, status=status.HTTP_404_NOT_FOUND)
        growth_records = GrowthRecord.objects.filter(child=child).order_by('date_recorded')
        if not growth_records.exists():
            return Response({'labels': [], 'datasets': []})
        labels = [gr.date_recorded.strftime('%Y-%m-%d') for gr in growth_records]
        weights = [gr.weight for gr in growth_records]
        heights = [gr.height for gr in growth_records]
        # Optionally, add WHO reference data here if available
        datasets = [
            {'label': 'Weight (kg)', 'data': weights},
            {'label': 'Height (cm)', 'data': heights},
        ]
        return Response({'labels': labels, 'datasets': datasets}) 