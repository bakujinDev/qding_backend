from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from qnas.models import Question, QuestionComment, Tag
from qnas.serializers import (
    QuestionListSerializer,
    AskSerializer,
    QuestionSerializer,
    QuestionCommentSerializer,
)
from common.views import check_owner


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


class QuestionDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)

        cookie = request.query_params.get("cookie")
        if not cookie:
            question.views = question.views + 1
            question.save(update_fields=["views"])

        serializer = QuestionSerializer(
            question,
            context={"request": request},
        )

        return Response(serializer.data)


class QuestionVote(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def post():


class QuestionComments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        serializer = QuestionCommentSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            comment = serializer.save(
                creator=request.user,
                target=question,
            )
            serializer = QuestionCommentSerializer(comment)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class QuestionCommentDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, comment_id):
        comment = QuestionComment.objects.get(pk=comment_id)
        now = timezone.localtime()
        limit = comment.created_at.astimezone() + timezone.timedelta(minutes=5)

        if limit >= now:
            check_owner(request, comment.creator)

            serializer = QuestionCommentSerializer(
                comment,
                data=request.data,
                partial=True,
            )

            if serializer.is_valid():
                updated_comment = serializer.save()
                serializer = QuestionCommentSerializer(updated_comment)
                return Response(serializer.data)

            else:
                return Response(serializer.errors)

        else:
            raise ParseError("수정 가능한 시간이 지났습니다")

    def delete(swlf, request, comment_id):
        comment = QuestionComment.objects.get(pk=comment_id)

        now = timezone.localtime()
        limit = comment.created_at.astimezone() + timezone.timedelta(minutes=5)

        if limit >= now:
            check_owner(request, comment.creator)
            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise ParseError("수정 가능한 시간이 지났습니다")
