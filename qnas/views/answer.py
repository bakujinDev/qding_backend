from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from qnas import models
from qnas import serializers
from common.views import check_owner, get_page
from users import models as usersModels


class AnswerPost(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, question_id):
        question = models.Question.objects.get(pk=question_id)
        serializer = serializers.AnswerSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            comment = serializer.save(
                creator=request.user,
                question=question,
            )
            serializer = serializers.AnswerSerializer(comment)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class AnswerVotes(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, answer_id):
        answer = models.Answer.objects.get(pk=answer_id)

        vote = models.AnswerVote.objects.filter(target=answer, creator=request.user)

        if vote.exists():
            raise ParseError("이미 투표한 질문이에요.")

        else:
            serializer = serializers.AnswerVoteSerializer(data=request.data)

            if serializer.is_valid():
                vote = serializer.save(
                    creator=request.user,
                    target=answer,
                )
                serializer = serializers.AnswerVoteSerializer(vote)
                return Response(serializer.data)

            else:
                return Response(serializer.errors)


class AnswerComments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, answer_id):
        answer = models.Answer.objects.get(pk=answer_id)
        serializer = serializers.AnswerCommentSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            comment = serializer.save(
                creator=request.user,
                target=answer,
            )
            serializer = serializers.AnswerCommentSerializer(comment)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class AnswerCommentDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, comment_id):
        comment = models.AnswerComment.objects.get(pk=comment_id)
        now = timezone.localtime()
        limit = comment.created_at.astimezone() + timezone.timedelta(minutes=5)

        if limit >= now:
            check_owner(request, comment.creator)

            serializer = serializers.AnswerCommentSerializer(
                comment,
                data=request.data,
                partial=True,
            )

            if serializer.is_valid():
                updated_comment = serializer.save()
                serializer = serializers.AnswerCommentSerializer(updated_comment)
                return Response(serializer.data)

            else:
                return Response(serializer.errors)

        else:
            raise ParseError("수정 가능한 시간이 지났습니다")

    def delete(swlf, request, comment_id):
        comment = models.AnswerComment.objects.get(pk=comment_id)

        now = timezone.localtime()
        limit = comment.created_at.astimezone() + timezone.timedelta(minutes=5)

        if limit >= now:
            check_owner(request, comment.creator)
            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise ParseError("수정 가능한 시간이 지났습니다")


class AnswerByCreator(APIView):
    def get(self, request, user_pk):
        order_opt = request.query_params.get("order_opt", "-pk")

        page = get_page(request)
        start = (page - 1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE

        creator = usersModels.User.objects.get(pk=user_pk)
        total = models.Answer.objects.filter(creator=creator).count()

        if order_opt == "-votes":
            page_answers = sorted(
                models.Answer.objects.filter(creator=creator),
                key=lambda a: -a.votes(),
            )[start:end]
        else:
            page_answers = models.Answer.objects.filter(creator=creator).order_by(
                "-pk"
            )[start:end]

        serializer = serializers.ProfileAnswerSerializer(
            page_answers,
            many=True,
        )

        return Response(
            {
                "total": total,
                "list": serializer.data,
            }
        )
