from typing import override

from django.db.models import CASCADE, BooleanField, Model, CharField, EmailField, DateTimeField, PositiveIntegerField, TextField, ForeignKey

class Member(Model):
    # 此处将 username 和 display_name 分离，username设为 unique 以便于题目二的author_articles按username查找作者
    username : CharField = CharField(max_length = 50, unique = True, default = "user")
    display_name : CharField = CharField(max_length = 100, default = "User")
    email : EmailField = EmailField(unique = True)
    joined_at : DateTimeField = DateTimeField(auto_now_add = True)
    bio : TextField = TextField(blank = True, default = "")

    class Meta:
        ordering = ["joined_at"]

    @override
    def __str__(self):
        return str(self.username)

class Article(Model):
    title : CharField = CharField(max_length = 200)
    content : TextField = TextField()
    author : ForeignKey = ForeignKey(Member, on_delete = CASCADE, related_name = "articles")
    is_published : BooleanField = BooleanField(default = False)
    created_at : DateTimeField = DateTimeField(auto_now_add = True)
    views : PositiveIntegerField = PositiveIntegerField(default = 0)

    class Meta:
        ordering = ["-created_at"]

class Comment(Model):
    content : TextField = TextField()
    article : ForeignKey = ForeignKey(Article, on_delete = CASCADE, related_name = "comments")
    commenter : ForeignKey = ForeignKey(Member, on_delete = CASCADE, related_name = "comments")

    class Meta:
        ordering = ["id"]

    def truncated_content(self) -> str:
        full_content = str(self.content)
        return full_content[:20] + ("..." if len(full_content) > 20 else "")

    @override
    def __str__(self):
        return f"{self.commenter}: {self.truncated_content}"

# Q1: CASCADE实现连带删除，比如删除作者的同时需要删除他的所有文章。SET_NULL 则是把相应字段置为 NULL，例如，如果想在删除用户时保留评论，可以把 Comment.commenter 的 on_delete 改为 SET_NULL，但相应地需要把 commenter 字段设置 null=True 并在业务代码中正确处理空值
# Q2: `related_name="comments"` 表示反向查询的名字，例如 Comment 类里的 article 是正向查询，related_name 则是指定反向查询的访问器名字。`article.comments.all()` 返回所有的article字段指向这个 Comment 的对象。
