from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.text import slugify


class MenuItem(models.Model):
    choice = [('main_menu', 'main_menu')]
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=False)
    menu_name = models.CharField(max_length=50, choices=choice, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    url = models.CharField(max_length=255, blank=True, editable=False)
    named_url = models.CharField(max_length=255, blank=True)

    def generate_url(self):
        parts = [slugify(self.name) or self.slug]
        parent = self.parent
        while parent:
            parts.append(slugify(parent.name) or parent.slug)
            parent = parent.parent
        return '/' + '/'.join(reversed(parts)) + '/'

    def save(self, *args, **kwargs):
        self.url = self.generate_url()
        super().save(*args, **kwargs)
        for child in self.children.all():
            child.save( c )

    def get_absolute_url(self):
        try:
            if self.named_url:
                return reverse(self.named_url)
        except NoReverseMatch:
            pass
        return self.url or "#"

    def __str__(self):
        return self.name
