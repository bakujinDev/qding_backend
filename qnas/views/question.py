from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from qnas.models import Question, Tag
from qnas.serializers import QuestionListSerializer, AskSerializer, QuestionSerializer


def add_tags(tags, question):
    for tag_name in tags:
        tag = Tag.objects.get(name=tag_name)
        question.tag.add(tag)


class Questions(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_qeustions = Question.objects.all()
        serializer = QuestionListSerializer(
            all_qeustions,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AskSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    question = serializer.save(creator=request.user)

                    tags = request.data.get("tag")

                    add_tags(tags, question)

                    serializer = AskSerializer(question)

                    return Response(serializer.data)

            except Exception as exception:
                raise ParseError(exception)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class QuestionPost(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        question = Question.objects.get(pk=id)
        serializer = QuestionSerializer(question)

        return Response(serializer.data)
