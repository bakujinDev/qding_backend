import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import Photo
from .serializers import PhotoSerializer


class GetUploadURL(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUD_FLARE_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CLOUD_FLARE_TOKEN}",
            },
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        return Response({"uploadURL": result.get("uploadURL")})
