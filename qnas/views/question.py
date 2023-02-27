from django.conf import settings
from django.db import transaction, connection
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from common.views import check_owner, get_page
from qnas import models, serializers
from users import models as usersModels
from users import function
from users.serializers import NotificationSerializer
from users.function import add_notifications_to_user_list, add_notification


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

        page_questions = models.Question.objects.all().order_by("-pk")[start:end]
        serializer = serializers.QuestionListSerializer(
            page_questions,
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

                    function.subscribe_notification(
                        model=question,
                        request_user=request.user,
                    )

                    serializer = serializers.AskSerializer(question)
                    return Response(serializer.data)

            except Exception as exception:
                raise ParseError(exception)

        else:
            print(request.data.get("tag"))
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class QuestionDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, question_id):
        question = models.Question.objects.get(pk=question_id)

        serializer = serializers.AskSerializer(question)

        return Response(serializer.data)

    def put(self, request, question_id):
        # 추후 수정요청 -> 동의 2명시 수정 으로 패치예정
        question = models.Question.objects.get(pk=question_id)

        check_owner(request, question.creator)

        serializer = serializers.AskSerializer(
            question,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    question = serializer.save()

                    tags = request.data.get("tag")

                    if tags != None:
                        question.tag.clear()

                        if tags:
                            add_tags(tags, question)

                    serializer = serializers.AskSerializer(question)
                    return Response(serializer.data)

            except Exception as exception:
                raise ParseError(exception)
        else:
            return Response(serializer.errors)


class QuestionPost(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, question_id):
        question = models.Question.objects.get(pk=question_id)

        viewLocalItem = request.query_params.get("viewLocalItem")
        if not viewLocalItem:
            question.views = question.views + 1
            question.save(update_fields=["views"])

        serializer = serializers.QuestionPostSerializer(
            question,
            context={"request": request},
        )

        return Response(serializer.data)


class ChoiceAnswer(APIView):
    def post(self, request, question_id):
        question = models.Question.objects.select_related("select_answer").get(
            pk=question_id
        )
        answer_id = request.data.get("answerId")

        if question.select_answer:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="이미 답변을 선택한 질문이에요")

        try:
            answer = models.Answer.objects.select_related("creator").get(pk=answer_id)
            question.select_answer = answer
            question.save(update_fields=["select_answer"])

            add_notification(
                answer.creator,
                content="답변이 선택되었어요",
                push_url=f"/qna/{question_id}?answerId={answer_id}",
            )

            return Response({"ok": "ok"})

        except models.Answer.DoesNotExist:
            raise NotFound


class QuestionVotes(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, question_id):
        question = models.Question.objects.get(pk=question_id)

        vote = models.QuestionVote.objects.filter(target=question, creator=request.user)

        if vote.exists():
            raise ParseError("이미 투표한 질문이에요.")

        else:
            serializer = serializers.QuestionVoteSerializer(data=request.data)

            if serializer.is_valid():
                vote = serializer.save(
                    creator=request.user,
                    target=question,
                )
                serializer = serializers.QuestionVoteSerializer(vote)
                return Response(serializer.data)

            else:
                return Response(serializer.errors)


class QuestionComments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, question_id):
        serializer = serializers.QuestionCommentSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            question = models.Question.objects.prefetch_related(
                "notification_user"
            ).get(pk=question_id)

            comment = serializer.save(
                creator=request.user,
                target=question,
            )
            serializer = serializers.QuestionCommentSerializer(comment)

            add_notifications_to_user_list(
                question,
                request.user,
                content="새로운 댓글이 추가되었어요",
                push_url=f"/qna/{question_id}",
            )

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
        try:
            comment = models.QuestionComment.objects.get(pk=comment_id)
        except models.QuestionComment.DoesNotExist:
            raise NotFound

        now = timezone.localtime()
        limit = comment.created_at.astimezone() + timezone.timedelta(minutes=5)

        if limit >= now:
            check_owner(request, comment.creator)
            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise ParseError("수정 가능한 시간이 지났습니다")


class QuestionByCreator(APIView):
    def get(self, request, user_pk):
        order_opt = request.query_params.get("order_opt", "-pk")

        page = get_page(request)
        start = (page - 1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE

        creator = usersModels.User.objects.get(pk=user_pk)
        total = models.Question.objects.filter(creator=creator).count()

        if order_opt == "-votes":
            page_questions = sorted(
                models.Question.objects.filter(creator=creator),
                key=lambda a: -a.votes(),
            )[start:end]
        else:
            page_questions = models.Question.objects.filter(creator=creator).order_by(
                "-pk"
            )[start:end]

        serializer = serializers.ProfileQuestionSerializer(
            page_questions,
            many=True,
        )
        return Response(
            {
                "total": total,
                "list": serializer.data,
            }
        )
