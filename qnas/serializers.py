from rest_framework import serializers
from .models import Question, QuestionComment, Answer, AnswerComment, Tag
from common import serializers as commonSerializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "pk",
            "name",
            "description",
        )


class QuestionListSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Question
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
        )

    def get_answers_count(self, question):
        self.answers_count()


class CommentByAnswerSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = AnswerComment
        fields = (
            "creator",
            "content",
            "updated_at",
        )


class AnswerListSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer(read_only=True)
    answer_comments = CommentByAnswerSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Answer
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
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = (
            "creator",
            "title",
            "content",
            "tag",
        )


class AnswerSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = (
            "creator",
            "question",
            "content",
            "updated_at",
        )


class CommentByQuestionSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = QuestionComment
        fields = (
            "creator",
            "content",
            "updated_at",
        )


class QuestionSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Question
        fields = (
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
        )


class QuestionCommentSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = QuestionComment
        fields = (
            "creator",
            "target",
            "content",
            "updated_at",
        )


class AnswerCommentSerializer(serializers.ModelSerializer):
    creator = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = AnswerComment
        fields = (
            "creator",
            "target",
            "content",
            "updated_at",
        )
