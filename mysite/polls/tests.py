import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice
# Create your tests here.


class QuestionModelsTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        # create date set to 30 days in the future with current time
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def createQuestion(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    Choice.objects.create(question=question, choice_text="Choice")
    return question


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        question = createQuestion(question_text="Past Question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        createQuestion(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(
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


class QuestionDetailView(TestCase):
    def test_future_question(self):
        future_question = createQuestion(question_text="Future question", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = createQuestion(question_text="Past question", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_without_choices(self):
        question = Question.objects.create(question_text="Question without choices", pub_date=timezone.now())
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_question_with_choices(self):
        question = createQuestion(question_text="Question with choices", days=0)
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class QuestionResultsView(TestCase):
    def test_future_question(self):
        future_question = createQuestion(question_text="Future question", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
