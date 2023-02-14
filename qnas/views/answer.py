from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from qnas.models import Question, Answer
from qnas.serializers import AnswerSerializer


class AnswerPost(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        serializer = AnswerSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            comment = serializer.save(
                creator=request.user,
                question=question,
            )
            serializer = AnswerSerializer(comment)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)
