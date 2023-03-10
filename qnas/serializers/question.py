from rest_framework import serializers
from qnas import models
from .tag import *
from .answer import *
from common import serializers as commonSerializers


class ForProfileAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = (
            "pk",
            "title",
        )


class ProfileQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = (
            "pk",
            "title",
            "created_at",
            "votes",
            "select_answer",
        )


class AskSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer(read_only=True)
    tag = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        fields = (
            "pk",
            "creator",
            "title",
            "content",
            "tag",
        )

    def get_tag(self, obj):
        return QnasSerializers.TagSerializer(
            obj.tag,
            many=True,
        ).data


class QuestionListSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    creator = commonSerializers.ProfileUserSerializer(read_only=True)
    editor = commonSerializers.ProfileUserSerializer(read_only=True)

    class Meta:
        model = models.Question
        fields = (
            "pk",
            "title",
            "content",
            "select_answer",
            "views",
            "updated_at",
            "answers_count",
            "tag",
            "votes",
            "creator",
            "editor",
        )

    def get_answers_count(self, question):
        self.answers_count()


class CommentByQuestionSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = models.QuestionComment
        fields = (
            "pk",
            "creator",
            "content",
            "created_at",
            "updated_at",
        )


class QuestionDetailSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer(read_only=True)
    editor = commonSerializers.ProfileUserSerializer(read_only=True)
    tag = TagListSerializer(read_only=True, many=True)
    question_comments = CommentByQuestionSerializer(
        read_only=True,
        many=True,
    )
    is_question_owner = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        fields = (
            "pk",
            "creator",
            "editor",
            "title",
            "content",
            "select_answer",
            "views",
            "updated_at",
            "tag",
            "votes",
            "question_comments",
            "is_question_owner",
        )

    def get_is_question_owner(self, model):
        request = self.context.get("request")
        return model.creator == request.user


class QuestionPostSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer(read_only=True)
    editor = commonSerializers.ProfileUserSerializer(read_only=True)
    tag = TagSerializer(read_only=True, many=True)
    question_comments = CommentByQuestionSerializer(
        read_only=True,
        many=True,
    )
    answers = AnswerListSerializer(
        read_only=True,
        many=True,
    )
    is_question_owner = serializers.SerializerMethodField()
    is_question_voted = serializers.SerializerMethodField()
    is_question_described = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        fields = (
            "pk",
            "creator",
            "editor",
            "title",
            "content",
            "select_answer",
            "views",
            "updated_at",
            "tag",
            "votes",
            "question_comments",
            "answers",
            "is_question_owner",
            "is_question_voted",
            "is_question_described",
        )

    def get_is_question_owner(self, model):
        request = self.context.get("request")
        return model.creator == request.user

    def get_is_question_voted(self, model):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return None

        try:
            return models.QuestionVote.objects.get(
                creator=request.user,
                target=model.pk,
            ).vote_type
        except:
            return None

    def get_is_question_described(self, model):
        request = self.context.get("request")

        return model.notification_user.filter(pk=request.user.pk).exists()


class QuestionVoteSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = models.QuestionVote
        fields = (
            "creator",
            "target",
            "vote_type",
            "updated_at",
        )


class QuestionCommentSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = models.QuestionComment
        fields = (
            "creator",
            "target",
            "content",
            "updated_at",
        )
