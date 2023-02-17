from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from common.views import get_page
from qnas import models, serializers
from common.views import check_owner


def add_tags(tags, question):
    for tag_name in tags:
        tag = models.Tag.objects.get(name=tag_name)
        question.tag.add(tag)


class Questions(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        page = get_page(request)
        start = (page - 1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE

        total = models.Question.objects.all().count()

        page_qeustions = models.Question.objects.all().order_by("-pk")[start:end]
        serializer = serializers.QuestionListSerializer(
            page_qeustions,
            many=True,
        )

        return Response(
            {
                "total": total,
                "list": serializer.data,
            }
        )

    def post(self, request):
        serializer = serializers.AskSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    question = serializer.save(creator=request.user)

                    tags = request.data.get("tag")

                    add_tags(tags, question)

                    serializer = serializers.AskSerializer(question)

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
        question = models.Question.objects.get(pk=question_id)

        viewLocalItem = request.query_params.get("viewLocalItem")
        if not viewLocalItem:
            question.views = question.views + 1
            question.save(update_fields=["views"])

        serializer = serializers.QuestionSerializer(
            question,
            context={"request": request},
        )

        return Response(serializer.data)


class QuestionVotes(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, question_id):
        question = models.Question.objects.get(pk=question_id)

        vote = models.QuestionVote.objects.get(target=question, creator=request.user)
        print(vote)
        return Response({"hi": "hi"})


class QuestionComments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, question_id):
        question = models.Question.objects.get(pk=question_id)
        serializer = serializers.QuestionCommentSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            comment = serializer.save(
                creator=request.user,
                target=question,
            )
            serializer = serializers.QuestionCommentSerializer(comment)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class QuestionCommentDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, comment_id):
        comment = models.QuestionComment.objects.get(pk=comment_id)
        now = timezone.localtime()
        limit = comment.created_at.astimezone() + timezone.timedelta(minutes=5)

        if limit >= now:
            check_owner(request, comment.creator)

            serializer = serializers.QuestionCommentSerializer(
                comment,
                data=request.data,
                partial=True,
            )

            if serializer.is_valid():
                updated_comment = serializer.save()
                serializer = serializers.QuestionCommentSerializer(updated_comment)
                return Response(serializer.data)

            else:
                return Response(serializer.errors)

        else:
            raise ParseError("수정 가능한 시간이 지났습니다")

    def delete(swlf, request, comment_id):
        comment = models.QuestionComment.objects.get(pk=comment_id)

        now = timezone.localtime()
        limit = comment.created_at.astimezone() + timezone.timedelta(minutes=5)

        if limit >= now:
            check_owner(request, comment.creator)
            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise ParseError("수정 가능한 시간이 지났습니다")
