from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from qnas.models import Tag
from qnas.serializers import TagSerializer


class Tags(APIView):
    def get(self, request):
        search = request.query_params.get("search")
        print(search)
        if search:
            tags = Tag.objects.filter(name__icontains=search)[:10]
        else:
            tags = Tag.objects.all()[:10]

        print(tags)

        serializer = TagSerializer(
            tags,
            many=True,
        )
        return Response(serializer.data)
