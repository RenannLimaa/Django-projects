import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
# Create your tests here.


class QuestionModelsTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        # create date set to 30 days in the future with current time
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.delta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, min=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def createQuestion(question_text, days):
    time = timezone.now() + datetime.delta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["lastest_question_list"], [])

    def test_past_question(self):
        question = createQuestion(question_text="Past Question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        createQuestion(question_text="Future question", days=30)
        response = self.client.get(reverse("polls.index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEquals(
            response.context["latest_question_list"],
            [],
        )

    def test_future_question_and_past_question(self):
        question = createQuestion(question_text="Past Question", days=-30)
        createQuestion(question_text="Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def two_past_questions(self):
        question1 = createQuestion(question_text="Past Question 1", days=-30)
        question2 = createQuestion(question_text="Past Question 2", days=-5)
        response = self.client.get(reverse("polls:index"))
        response.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
