
































































#GUARDIANS VIEW ON THE MOBILE APP ONLY
class CustomTokenObtainPairView(TokenObtainPairView):
    # Custom login logic if needed
    pass
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def guardian_children(request):
    children = request.user.children.all()
    serializer = ChildSerializer(children, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def child_detail(request, child_id):
    child = get_object_or_404(Child, id=child_id, guardian=request.user)
    serializer = ChildSerializer(child)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def child_vaccinations(request, child_id):
    child = get_object_or_404(Child, id=child_id, guardian=request.user)
    vaccinations = child.vaccinations.all().order_by('-date_administered')
    serializer = VaccinationSerializer(vaccinations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def child_growth_data(request, child_id):
    child = get_object_or_404(Child, id=child_id, guardian=request.user)
    growth_records = child.growth_records.all().order_by('recorded_date')
    serializer = GrowthRecordSerializer(growth_records, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications(request):
    notifications = request.user.notification_set.all().order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, guardian=request.user)
    notification.is_read = True
    notification.save()
    return Response({'status': 'marked as read'})
#END