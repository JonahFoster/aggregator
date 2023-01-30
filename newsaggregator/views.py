from django.views.generic import ListView
from .models import Post
# Create your views here.

class HomePageView(ListView):
    template_name = "homepage.html"
    model = Post


    # Filter Posts, limit to 10 most recent ones
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter().order_by("-pub_date")[:10]
        return context