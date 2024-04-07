from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.template.defaultfilters import truncatewords_html
from .models import Post


class LatestPostFeed(Feed):
    title = 'My blog'
    description = 'New posts'
    link = reverse_lazy('post_list')

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords_html(item.body, 30)
    
    def item_pubdate(self, item):
        return item.publish