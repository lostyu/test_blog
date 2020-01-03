from django import template
from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num]
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    dates = Post.objects.dates('created_time', 'month', order='DESC')
    results = []

    for d in dates:
        count = Post.objects.all().filter(created_time__year=d.year, created_time__month=d.month).count()
        results.append({'date': d, 'count': count})

    return {
        'date_list': results
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.all()
    results = []
    for c in category_list:
        count = c.post_set.all().count()
        results.append({'cate': c, 'count': count})
    return {
        'category_list': results
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all()
    }
