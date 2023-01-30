from django.test import TestCase
from django.utils import timezone
from .models import Post
from django.urls.base import reverse
# Create your tests here.

class NewsAggregatorTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="My News Post",
            description="Woah it is news",
            pub_date=timezone.now(),
            link="https://www.jonahfoster.net/",
            image="https://image.myawesomeshow.com",
            website_name="The Website Name",
            guid="de194720-7b4c-49e2-a05f-432436d3fetr",
        )
    
    def test_post_content(self):
        self.assertEqual(self.post.description, "Woah it is news")
        self.assertEqual(self.post.link, "https://www.jonahfoster.net/")
        self.assertEqual(self.post.guid, "de194720-7b4c-49e2-a05f-432436d3fetr")
    
    def test_post_str_representation(self):
            self.assertEqual(
                str(self.post), "The Website Name: My News Post"
            )

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "homepage.html")

    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "My News Post")