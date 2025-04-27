import json
from django.db import models
from django.urls import reverse

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    order = models.PositiveSmallIntegerField(default=0)
    url = models.CharField(max_length=500, blank=True)
    named_url = models.CharField(max_length=200, blank=True)
    named_args = models.CharField(max_length=300, blank=True)
    class Meta:
        ordering = ['menu', 'order', 'id']
    def __str__(self):
        return f"{self.menu.name} → {self.title}"
    def get_url(self):
        if self.named_url:
            try:
                args = json.loads(self.named_args) if self.named_args else []
                return reverse(self.named_url, args=args)
            except:
                return '#'
        return self.url or '#'
