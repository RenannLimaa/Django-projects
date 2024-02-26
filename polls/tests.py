import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
# Create your tests here.


class QuestionModelsTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        # create date set to 30 days in the future with current time
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
