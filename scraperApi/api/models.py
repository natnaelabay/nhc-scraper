from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Article(models.Model):
    SCRAPED_STATUS_CHOICES = (
        (0, 'Not Scraped'),
        (1, 'Scraped - Failed'),
        (2, 'Scraped - Successful'),
    )
    is_parsed = models.BooleanField(default=False)
    status = models.IntegerField(choices=SCRAPED_STATUS_CHOICES, default=0)
    published_date = models.DateField(null=True)
    url = models.URLField()
    title = models.CharField(max_length=500)
    content = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title} - {self.published_date}"
