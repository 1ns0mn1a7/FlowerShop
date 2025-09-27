from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Consultation

@api_view(['POST'])
def create_consultation(request):
    name = request.data.get('client_name', '').strip()
    phone = request.data.get('client_phone', '').strip()

    existing_consultation = Consultation.objects.filter(client_name=name, status__in=['accepted', 'rejected'],
                                                        client_phone=phone).exists()
    if existing_consultation:
        return Response({'error': 'У вас уже есть активная или отклоненная заявка'}, status=status.HTTP_400_BAD_REQUEST)

    consultation = Consultation.objects.create(
        client_name=name,
        client_phone=phone
    )

    return Response({'success': 'Заявка создана', 'id': consultation.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_order(request):
    name = request.data.get('client_name', '').strip()
