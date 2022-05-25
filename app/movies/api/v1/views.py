from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from movies.models import Filmwork, PersonFilmwork, Role  # noqa
from django.contrib.postgres.aggregates import ArrayAgg


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]  # Список методов, которые реализует обработчик

    @staticmethod
    def get_queryset():
        # Переделал, но не уверен, что правильно понял. По крайне мере если будут добавляться
        # роли, здесь менять ни чего не нужно будет
        roles = {
            role: ArrayAgg(
                "person__full_name", filter=Q(personfilmwork__role=role), distinct=True
            )
            for role in Role.all_roles
        }
        qs = Filmwork.objects.annotate(
            **roles, genr=ArrayAgg("genres__name", distinct=True)
        )
        return qs.order_by("id")

    @staticmethod
    def render_to_response(
        context,
    ):
        return JsonResponse(context)

    @staticmethod
    def get_film_data(film: Filmwork):
        return {
            "id": film.id,
            "title": film.title,
            "description": film.title,
            "creation_date": film.created,
            "rating": film.rating,
            "type": film.type,
            "genres": film.genr,
            "actors": film.actor,
            "directors": film.director,
            "writers": film.writer,
        }


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        qs = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            qs, self.paginate_by
        )
        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": [self.get_film_data(film) for film in queryset],
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        film: Filmwork = self.get_queryset().filter(id=self.kwargs.get("pk"))[0]
        return self.get_film_data(film)


# разобрался с кавычками, остановился на двойных
