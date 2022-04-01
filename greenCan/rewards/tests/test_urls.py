from django.test import TestCase
from django.urls import reverse, resolve
from rewards.views import index, earn_rewards


class TestUrls(TestCase):
    def test_index_url(self):
        url = reverse("rewards:index")
        self.assertEquals(resolve(url).func, index)
        self.assertEquals(resolve(url).namespace, "rewards")
        self.assertEquals(url, "/rewards/")

    def test_earn_rewards_url(self):
        url = reverse("rewards:earn-rewards")
        self.assertEquals(resolve(url).func, earn_rewards)
        self.assertEquals(resolve(url).namespace, "rewards")
        self.assertEquals(url, "/rewards/earn/")
