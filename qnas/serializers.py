from rest_framework import serializers
from .models import Question
from common import serializers as commonSerializers


class QuestionListSerializer(serializers.ModelSerializer):
    creator = commonSerializers.MinimumUserSerializer()
    editor = commonSerializers.MinimumUserSerializer()

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
            "answers_count",
        )

    def get_answers_count(self, question):
        self.answers_count()
