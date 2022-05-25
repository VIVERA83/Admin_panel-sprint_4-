from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    prefetch_related = ("items",)
    # К сожалению не понял как, сделать что бы запросов было меньше
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    # Отображение полей в списке
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "created",
        "modified",
    )
    # Фильтрация в списке
    list_filter = ("type", "rating", "person")
    # Поиск по полям
    search_fields = ("title", "description", "id")
    # Сортировка
    ordering = ("title",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
