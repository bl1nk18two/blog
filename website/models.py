from django.db import models


class Author(models.Model):
    author_first_name = models.CharField(max_length=50)
    author_last_name = models.CharField(max_length=50)
    activate_status = models.CharField(max_length=1, default="Y")

    def __str__(self):
        return f"{self.author_first_name} {self.author_last_name}"


class Categories(models.Model):
    name = models.CharField(max_length=50)
    activate_status = models.CharField(max_length=1, default='Y'
    )

    def __str__(self):
        return self.name    


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    thumb_image = models.URLField(default='https://coffective.com/wp-content/uploads/2018/06/default-featured-image.png.jpg')
    title = models.CharField(max_length=255)
    article = models.TextField()
    author_id = models.ForeignKey(Author, on_delete=models.PROTECT)
    subject_id = models.ForeignKey(Categories, on_delete=models.PROTECT)

    def __str__(self):
        return self.title    

