from django.contrib import messages
from django.db.models import F
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Article, Member, Comment
from .forms import ArticleForm

def index(request : HttpRequest) -> HttpResponse:
    articles = Article.objects.filter(is_published = True)
    return render(request, "blog/index.html", {"articles" : articles})

def article_detail(request : HttpRequest, pk : int) -> HttpResponse:
    article = get_object_or_404(Article, pk = pk)
    Article.objects.filter(pk=pk).update(views=F("views")+1)
    return render(request, "blog.detail.html", {"article": article})

def add_comment(request: HttpRequest, pk : int) -> HttpResponse:
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        content = request.POST.get("content", "")
        commenter = Member.objects.first() # TODO implement login
        if commenter is None:
            raise Http404("Failed to find commenter")
        Comment.objects.create(article=article, commenter=commenter, content=content)
    return redirect("blog:article_detail", pk=article.pk)

def author_articles(request: HttpRequest, username: str) -> HttpResponse:
    author : Member = get_object_or_404(Member, username=username)
    articles = Article.objects.filter(author=author).annotate(comment_count=Count("comments"))
    return render(request, "blog/author.html", {"author" : author, "articles" : articles})

def article_create(request: HttpRequest) -> HttpResponse:
    if (request.method == "POST"):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            messages.success(request, f"\"{article.title}\" 创建成功");
            return redirect("blog:article_detail", pk = article.pk)
    else:
        form = ArticleForm()

    return render(request, "blog/article_form.html", {"form": form})

# 浏览量+1，实际上是先读（原来的浏览量）后写（加1后的浏览量），需要保证原子性。a的方法，两次请求可能发生：1读到原浏览量->2读到原浏览量->1增加浏览量后保存->2增加浏览量后保存
# b的方法实际把读写操作放到了一次数据库请求里，因此没有问题。
