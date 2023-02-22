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

    class Meta:
        model = models.Answer
        fields = (
            "pk",
            "creator",
            "votes",
            "content",
            "updated_at",
            "answer_comments",
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
