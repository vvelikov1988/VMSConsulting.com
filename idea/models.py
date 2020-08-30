from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import FileExtensionValidator

from stdimage.models import StdImageField
from stdimage.validators import MinSizeValidator, MaxSizeValidator

from account.model_addon import UploadToPathAndRename
from account.models import Account

IDEA_TOPIC_CHOICES = (
    (1, 'Computer Science'),
    (2, 'Medical'),
    (3, 'Marketing'),
    (4, 'Business'),
    (5, 'Sport'),
    (6, 'Places'),
    (7, 'Development'),
    (8, 'Other'),
)


class Idea(models.Model):
    user = models.ForeignKey(Account, related_name='ideas', on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255
    )
    topic = models.IntegerField(
        verbose_name=_('Topic'),
        choices=IDEA_TOPIC_CHOICES,
    )
    description = models.TextField()
    image = StdImageField(
        verbose_name=_('Image'),
        default='default/img/idea.png',
        upload_to=UploadToPathAndRename('upload/img/idea'),
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg']),
            MinSizeValidator(200, 200),
            MaxSizeValidator(1200, 1200)
        ],
        variations={
            'thumbnail': (40, 40, True),
            'medium': (200, 200, True),
            'large': (525, 525, True),
        },
        blank=True,
        null=True
    )
    file = models.FileField(
        verbose_name=_('Resume'),
        upload_to=UploadToPathAndRename('upload/file/resume'),
        validators=[
            FileExtensionValidator(['pdf', 'doc', 'docx']),
        ],
        blank=True,
        null=True
    )
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('idea')
        verbose_name_plural = _('ideas')
        ordering = ['-created_at']

    def __str__(self):
        return ('%s add by %s' % (self.title, self.user.get_full_name())).strip()

    def get_topic_str(self):
        return IDEA_TOPIC_CHOICES[self.topic - 1][1]


class Comment(models.Model):
    user = models.ForeignKey(Account, related_name='comments', on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return ('%s commented by %s' % (self.text, self.user.get_full_name())).strip()
