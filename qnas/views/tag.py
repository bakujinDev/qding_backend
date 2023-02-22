from django.db.models import Q, Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from qnas import models
from qnas import serializers
from users import models as usersModels
from itertools import chain


class Tags(APIView):
    def get(self, request):
        search = request.query_params.get("search")

        if search:
            tags = models.Tag.objects.filter(name__icontains=search)[:10]
        else:
            tags = models.Tag.objects.all()[:10]

        serializer = serializers.TagSerializer(
            tags,
            many=True,
        )
        return Response(serializer.data)


class TagHistory(APIView):
    def get(self, request, user_pk):
        creator = usersModels.User.objects.get(pk=user_pk)

        history = (
            models.Tag.objects.annotate(
                count=Count(
                    "questions",
                    filter=Q(questions__creator=creator)
                    | Q(questions__answers__creator=creator),
                )
            )
            .filter(count__gt=0)
            .order_by("-count")
            .values("name", "count")[:5]
        )

        serializer = serializers.TagHistorySerializer(
            history,
            many=True,
        )

        return Response(serializer.data)
