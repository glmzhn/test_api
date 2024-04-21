from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, generate_verification_code
from datetime import timedelta
from django.utils import timezone


@api_view(['POST'])
def check_phone_number(request):
    phone_number = request.data.get('phone_number')
    if phone_number:
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if not created:
            if user.code_created_at is None or timezone.now() - user.code_created_at > timedelta(minutes=5):
                user.verif_code = generate_verification_code()
                user.code_created_at = timezone.now()
                user.save()
        return Response({"code_verification": user.verif_code})
    else:
        return Response({"error": "Phone number is required."}, status=400)


@api_view(['POST'])
def verify_code(request):
    code = request.data.get('code')
    user = User.objects.filter(verif_code=code).first()
    if user:
        user.is_authenticated = True
        user.save()
        return Response({"unique_id": user.unique_id})
    else:
        return Response({"error": "Invalid verification code."}, status=400)


@api_view(['POST'])
def invite_user(request):
    code = request.data.get('code')
    invite_code = request.data.get('invite_code')
    user = User.objects.filter(verif_code=code, is_authenticated=True).first()
    if user:
        if invite_code and not user.has_invited:
            inviter = User.objects.filter(unique_id=invite_code, has_invited=False).first()
            if inviter:
                user.invited_by = inviter
                inviter.has_invited = True
                inviter.save()
                user.has_invited = True
                user.save()
                return Response({"message": "User successfully invited."})
            else:
                return Response({"error": "You have already invited a user"})
        else:
            return Response({"error": "You have already invited a user or no invite code provided."})
    else:
        return Response({"error": "Invalid verification code or user is not authenticated."}, status=400)


@api_view(['GET'])
def get_invited_users(request, unique_id):
    user = User.objects.filter(unique_id=unique_id).first()
    if user:
        invited_users = User.objects.filter(invited_by=user)
        return Response({"invited_users": [str(u.phone_number) for u in invited_users]})
    else:
        return Response({"error": "User does not exist."}, status=404)
