from django.db import models

class Research(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Source(models.Model):
    research = models.ForeignKey(Research, related_name='sources', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Pics(models.Model):
    research = models.ForeignKey(Research, related_name='pics', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='research_pics/')
    caption = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.research.name} - {self.caption}"