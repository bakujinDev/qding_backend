from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from qnas.models import Question, Answer, AnswerComment
from qnas.serializers import AnswerSerializer, AnswerCommentSerializer
from common.views import check_owner


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


class AnswerComments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, answer_id):
        answer = Answer.objects.get(pk=answer_id)
        serializer = AnswerCommentSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            comment = serializer.save(
                creator=request.user,
                target=answer,
            )
            serializer = AnswerCommentSerializer(comment)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class AnswerCommentDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, comment_id):
        comment = AnswerComment.objects.get(pk=comment_id)
        now = timezone.localtime()
        limit = comment.created_at.astimezone() + timezone.timedelta(minutes=5)

        if limit >= now:
            check_owner(request, comment.creator)

            serializer = AnswerCommentSerializer(
                comment,
                data=request.data,
                partial=True,
            )

            if serializer.is_valid():
                updated_comment = serializer.save()
                serializer = AnswerCommentSerializer(updated_comment)
                return Response(serializer.data)

            else:
                return Response(serializer.errors)

        else:
            raise ParseError("수정 가능한 시간이 지났습니다")
