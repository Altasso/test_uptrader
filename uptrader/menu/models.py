from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.text import slugify


class MenuItem(models.Model):
    choice_menu = [('main_menu', 'main_menu')]
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=False, blank=True, null=True)
    menu_name = models.CharField(max_length=50, choices=choice_menu, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    url = models.CharField(max_length=200, blank=True, null=True, help_text="Явный URL, например /about/")
    named_url = models.CharField(max_length=100, blank=True, null=True, help_text="Имя URL из urls.py, например home")


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
            child.save()


    def get_absolute_url(self):
        if self.named_url:
            try:
                if self.slug:
                    url = reverse(self.named_url, kwargs={'slug': self.slug})
                    if not url.startswith('/'):
                        url = '/' + url
                    return url
                else:
                    return '#'
            except NoReverseMatch:
                return '#'
        elif self.url:
            if not self.url.startswith('/'):
                return '/' + self.url
            return self.url
        else:
            return '#'

    def __str__(self):
        return self.name
