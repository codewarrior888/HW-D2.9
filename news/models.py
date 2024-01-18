from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    userAuthor = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.IntegerField(default=0)

    def update_rating(self):
        post_ratings = self.post_set.aggregate(post_rating_sum=models.Sum('post_rating'))['post_rating_sum'] or 0

        comment_ratings = self.userAuthor.comment_set.\
                                   aggregate(comment_rating_sum=models.Sum('comment_rating'))['comment_rating_sum'] or 0

        self.authorRating = post_ratings * 3 + comment_ratings
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    POST_GENRE = [
        (article, 'Article'),
        (news, 'News')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_genre = models.CharField(max_length=2, choices=POST_GENRE)
    post_title = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)
    post_time = models.DateTimeField(auto_now_add=True)

    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return f"{self.post_text[:124]}..."

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
