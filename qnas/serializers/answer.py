from rest_framework import serializers
from qnas import models
from .question import *
from common import serializers as commonSerializers


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
            # "votes",
            "content",
            "updated_at",
            "answer_comments",
        )


class AskSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer(read_only=True)
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = models.Question
        fields = (
            "creator",
            "title",
            "content",
            "tag",
        )


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
