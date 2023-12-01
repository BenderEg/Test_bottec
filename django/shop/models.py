from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True

class UUIDMixin(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:

        abstract = True


class Category(UUIDMixin, TimeStampedMixin):

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:

        db_table = "content\".\"category"
        verbose_name = _('сategory')
        verbose_name_plural = _('сategory')
        indexes = [
            models.Index(fields=['name'], name='category_name_idx')
            ]

    def __str__(self) -> str:
        return self.name


class SubCategory(UUIDMixin, TimeStampedMixin):

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:

        db_table = "content\".\"subcategory"
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategory')
        indexes = [
            models.Index(fields=['name', 'category'], name='subcategory_name_idx')
            ]

    def __str__(self) -> str:
        return f'Подкатегория: {self.name} (категория {self.category.name})'


class Item(UUIDMixin, TimeStampedMixin):

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    image_path = models.ImageField(_('image'), max_length=255,
                                   blank=True, null=True,
                                   upload_to=f'images/%Y/%m/%d/%H/%M/%S')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    class Meta:

        db_table = "content\".\"item"
        verbose_name = _('item')
        verbose_name_plural = _('item')
        indexes = [
            models.Index(fields=['name', 'subcategory'], name='item_name_idx')
            ]

    def __str__(self) -> str:
        return self.name


class Messages(UUIDMixin, TimeStampedMixin):

    class Status(models.IntegerChoices):
        DRAFT = 0, _('draft')
        PUBLISHED = 1, _('published')

    class Target(models.TextChoices):

        GROUP = 'group', _('group')
        CHANNEL = 'channel', _('channel')

    header = models.CharField(_('header'), max_length=255)
    description = models.TextField(_('description'))
    target = models.CharField(_('target'), max_length=10,
                              choices=Target.choices,
                              default=Target.GROUP)
    status = models.BooleanField(_('status'), choices=Status.choices,
                                 blank=False, default=Status.DRAFT)

    class Meta:

        db_table = "content\".\"messages"
        verbose_name = _('messages')
        verbose_name_plural = _('messages')

    def __str__(self) -> str:
        return self.header


class Client(TimeStampedMixin):

    class Subscription(models.IntegerChoices):
        SUBSCRIBED = 0, _('subscribed')
        NOT_SUBSCRIBED = 1, _('not subscribed')

    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(_('name'), max_length=255)
    group_subscription = models.BooleanField(_('group_subscription'),
                                             choices=Subscription.choices,
                                             blank=False, default=Subscription.NOT_SUBSCRIBED)
    channel_subscription = models.BooleanField(_('channel_subscription'),
                                             choices=Subscription.choices,
                                             blank=False, default=Subscription.NOT_SUBSCRIBED)

    class Meta:

        db_table = "content\".\"client"
        verbose_name = _('client')
        verbose_name_plural = _('client')

    def __str__(self) -> str:
        return f'{self.name}_{self.id}'


class Order(UUIDMixin):

    class Status(models.IntegerChoices):
        OPEN = 0, _('open')
        CLOSED = 1, _('closed')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, editable=False)
    items = models.ManyToManyField(Item, through='OrderItems', editable=False)
    address = models.TextField(_('description'))
    status = models.BooleanField(_('status'), choices=Status.choices,
                                 blank=False, default=Status.OPEN)

    class Meta:

        db_table = "content\".\"order"
        verbose_name = _('order')
        verbose_name_plural = _('order')

    def __str__(self) -> str:
        return str(self.id)


class OrderItems(UUIDMixin, TimeStampedMixin):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField(_('quantity'),
                                   validators=[MinValueValidator(1)],
                                   editable=False)

    class Meta:

        db_table = "content\".\"order_item"
        verbose_name = _('order_item')
        verbose_name_plural = _('order_item')

    def __str__(self) -> str:
        return str(self.id)
