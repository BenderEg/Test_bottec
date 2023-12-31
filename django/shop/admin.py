from django.contrib import admin
from .models import Item, Category, SubCategory, Messages, Client, \
    OrderItems, Order, Questions


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_filter = ('subcategory',)
    list_display = ('name', 'description', 'subcategory')
    list_display_links = ('name', 'description')
    ordering = ['name', 'subcategory']
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name', 'description')
    ordering = ['name']
    list_per_page = 20


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('name', 'description', 'category')
    list_display_links = ('name', 'description')
    ordering = ['name', 'category']
    list_per_page = 20


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    search_fields = ('header', 'description')
    list_display = ('header', 'description', 'status')
    list_display_links = ('header', 'description')
    ordering = ['status', 'modified']
    list_per_page = 20


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_filter = ('group_subscription', 'channel_subscription')
    list_display = ('name', 'group_subscription', 'channel_subscription')
    list_display_links = ('name',)
    ordering = ['group_subscription', 'channel_subscription']
    list_per_page = 20


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    fields = ['item', 'quantity']
    readonly_fields = ['item', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'status', 'created')
    ordering = ['created']
    list_per_page = 20

    inlines = (OrderItemsInline,)


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'created')
    ordering = ['created']
    list_per_page = 20


@admin.register(Questions)
class QustionsAdmin(admin.ModelAdmin):
    search_fields = ('question', 'answer')
    list_display = ('question', 'answer', 'status')
    list_display_links = ('question', 'answer')
    ordering = ['status', 'question']
    list_per_page = 20