from django.contrib import admin
from .models import Item, Category, SubCategory, Messages, Client


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