from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from qnas.models import Question
from qnas.serializers import QuestionListSerializer


class Questions(APIView):
    def get(self, request):
        all_qeustions = Question.objects.all()
        serializer = QuestionListSerializer(
            all_qeustions,
            many=True,
        )
        return Response(serializer.data)
