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
    is_answer_voted = serializers.SerializerMethodField()
    is_answer_described = serializers.SerializerMethodField()

    class Meta:
        model = models.Answer
        fields = (
            "pk",
            "creator",
            "votes",
            "content",
            "updated_at",
            "answer_comments",
            "is_selected",
            "is_answer_voted",
            "is_answer_described",
        )

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

    def get_is_answer_described(self, model):
        request = self.context.get("request")

        return model.notification_user.filter(pk=request.user.pk).exists()


class AnswerSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer(read_only=True)

    class Meta:
        model = models.Answer
        fields = (
            'pk',
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
