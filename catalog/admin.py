from django.contrib import admin
from .models import Category, Product, BlogPost, Version


# Настройка для модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Настройка для модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'is_published', 'views_count']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']


class VersionInline(admin.TabularInline):
    model = Version
    extra = 1  # Количество пустых форм для добавления новых версий (по умолчанию 1)


class ProductAdmin(admin.ModelAdmin):
    inlines = [VersionInline]
    list_display = (
        'name', 'price', 'category', 'get_active_version')

    def get_active_version(self, obj):
        active_version = obj.versions.filter(is_active=True).first()
        return active_version.version_name if active_version else 'No active version'

    get_active_version.short_description = 'Active Version'


class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'is_active')
    list_filter = ('is_active', 'product')


admin.site.register(Version, VersionAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
