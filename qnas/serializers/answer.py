from rest_framework import serializers
from qnas import models
from django.apps import apps
from qnas import serializers as QnasSerializers
from common import serializers as commonSerializers


class ProfileAnswerSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = models.Answer
        fields = (
            "pk",
            "question",
            "votes",
            "is_selected",
            "created_at",
        )

    def get_question(self, obj):
        return QnasSerializers.ForProfileAnswerSerializer(obj.question).data


class CommentByAnswerSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = models.AnswerComment
        fields = (
            "pk",
            "creator",
            "content",
            "created_at",
            "updated_at",
        )


class AnswerListSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer(read_only=True)
    answer_comments = CommentByAnswerSerializer(
        read_only=True,
        many=True,
    )
    is_answer_selected = serializers.SerializerMethodField()
    is_answer_voted = serializers.SerializerMethodField()

    class Meta:
        model = models.Answer
        fields = (
            "pk",
            "creator",
            "votes",
            "content",
            "updated_at",
            "answer_comments",
            "is_answer_selected",
            "is_answer_voted",
        )

    def get_is_answer_selected(self, model):
        return model == model.question.select_answer

    def get_is_answer_voted(self, model):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return None

        try:
            return models.AnswerVote.objects.get(
                creator=request.user,
                target=model.pk,
            ).vote_type
        except:
            return None


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


class AnswerSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer(read_only=True)

    class Meta:
        model = models.Answer
        fields = (
            "creator",
            "question",
            "content",
            "updated_at",
        )


class AnswerVoteSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = models.AnswerVote
        fields = (
            "creator",
            "target",
            "vote_type",
            "updated_at",
        )


class AnswerCommentSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = models.AnswerComment
        fields = (
            "creator",
            "target",
            "content",
            "updated_at",
        )
