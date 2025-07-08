from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from HealthcareW.models.Guardian import Guardian
from HealthcareW.models.Child import Child
from HealthcareW.models.GrowthRecord import GrowthRecord
from HealthcareW.models.VaccinationRecord import VaccinationRecord
from api.myserializers.guardian_serializer import GuardianProfileSerializer, GuardianChildrenSerializer
from api.myserializers.child_serializer import GuardianChildSerializer
from api.myserializers.growthrecord_serializer import GuardianGrowthRecordSerializer
from api.myserializers.vaccinationrecord_serializer import GuardianVaccinationRecordSerializer
from rest_framework.permissions import IsAuthenticated

class GuardianProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            guardian = Guardian.objects.get(user=request.user)
        except Guardian.DoesNotExist:
            return Response({'detail': 'Guardian not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GuardianProfileSerializer(guardian)
        return Response(serializer.data)

class GuardianChildrenView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            guardian = Guardian.objects.get(user=request.user)
        except Guardian.DoesNotExist:
            return Response({'detail': 'Guardian not found.'}, status=status.HTTP_404_NOT_FOUND)
        children = Child.objects.filter(guardian=guardian)
        serializer = GuardianChildrenSerializer(children, many=True)
        return Response(serializer.data)

class GuardianChildDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, child_id):
        try:
            guardian = Guardian.objects.get(user=request.user)
            child = Child.objects.get(child_id=child_id, guardian=guardian)
        except (Guardian.DoesNotExist, Child.DoesNotExist):
            return Response({'detail': 'Child not found or not owned by guardian.'}, status=status.HTTP_404_NOT_FOUND)
        child_serializer = GuardianChildSerializer(child)
        growth_records = GrowthRecord.objects.filter(child=child).order_by('-date_recorded')[:5]
        growth_serializer = GuardianGrowthRecordSerializer(growth_records, many=True)
        vaccines = VaccinationRecord.objects.filter(child=child).order_by('-administration_date')[:5]
        vaccine_serializer = GuardianVaccinationRecordSerializer(vaccines, many=True)
        return Response({
            'child': child_serializer.data,
            'recent_growth_records': growth_serializer.data,
            'recent_vaccinations': vaccine_serializer.data
        })

class GuardianChildGrowthView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, child_id):
        try:
            guardian = Guardian.objects.get(user=request.user)
            child = Child.objects.get(child_id=child_id, guardian=guardian)
        except (Guardian.DoesNotExist, Child.DoesNotExist):
            return Response({'detail': 'Child not found or not owned by guardian.'}, status=status.HTTP_404_NOT_FOUND)
        growth_records = GrowthRecord.objects.filter(child=child).order_by('date_recorded')
        serializer = GuardianGrowthRecordSerializer(growth_records, many=True)
        return Response(serializer.data)

class GuardianChildVaccinesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, child_id):
        try:
            guardian = Guardian.objects.get(user=request.user)
            child = Child.objects.get(child_id=child_id, guardian=guardian)
        except (Guardian.DoesNotExist, Child.DoesNotExist):
            return Response({'detail': 'Child not found or not owned by guardian.'}, status=status.HTTP_404_NOT_FOUND)
        vaccines = VaccinationRecord.objects.filter(child=child).order_by('administration_date')
        serializer = GuardianVaccinationRecordSerializer(vaccines, many=True)
        return Response(serializer.data) 