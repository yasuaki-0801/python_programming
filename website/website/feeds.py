from django.contrib.syndication.views import Feed
from django.urls import reverse
from cms.models import Post
from django.utils.feedgenerator import Atom1Feed

class LatestPostsFeed(Feed):

    title = "MySite 最新ブログ記事"
    link = "/cms/"
    description = "MySite のブログ記事に関する最新情報。"

    def items(self):
        return Post.objects.order_by('-published_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    # モデルに get_absolute_url() が定義されている場合は不要
    def item_link(self, item):
        return reverse('cms:post_detail', args=[item.pk])

class RssLatestPostsFeed(Feed):
    title = "MySite 最新ブログ記事"
    link = "/cms/"
    description = "MySite のブログ記事に関する最新情報。"
    def items(self):
        return Post.objects.order_by('-published_at')[:5]

class AtomLatestPostsFeed(RssLatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = RssLatestPostsFeed.description