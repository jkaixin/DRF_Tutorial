from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted((item[1][0], item[0]) for item in LEXERS)
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField('修改时间', auto_now_add=True)
    title = models.CharField('标题', max_length=100, blank=True, default='')
    code = models.TextField('代码')
    linehos = models.BooleanField(default=False)
    language = models.CharField('代码语言', max_length=100, choices=LANGUAGE_CHOICES, default='python')
    style = models.CharField('风格', max_length=100, choices=STYLE_CHOICES, default='friendly')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='snippets')
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linehos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created']
