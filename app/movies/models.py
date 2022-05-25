import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    full_name = models.TextField(
        _("full name"),
        blank=True,
    )

    def __str__(self):
        return self.full_name


class Gender(models.TextChoices):
    MALE = "male", _("male")
    FEMALE = "female", _("female")


class Types(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv_show", _("tv_show")


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("film_work")
        verbose_name_plural = _("film_work")
        indexes = [models.Index(fields=["creation_date"])]

    title = models.TextField(_("title"))
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation date"))
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.TextField(_("type"), choices=Types.choices, default=Types.MOVIE)
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    person = models.ManyToManyField(Person, through="PersonFilmwork")

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    class Meta:
        db_table = 'content"."genre_film_work'

    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    created = models.DateTimeField(_("created"), auto_now_add=True)


class Role(models.TextChoices):
    ACTOR = "actor", _("actor")
    DIRECTORS = "director", _("director")
    WRITERS = "writer", _("writer")

    @classmethod
    @property
    # данный метод используется в api.v1.views, для получения списка актуальных ролей.
    def all_roles(cls) -> dict[str]:  # noqa
        return cls._value2label_map_.keys()


class PersonFilmwork(UUIDMixin):
    class Meta:
        db_table = 'content"."person_film_work'
        unique_together = [["id", "film_work", "person"]]

    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    # Учел, пожелание на ограничение поля РОЛИ, но для себя не понял пока как сделать так
    # что бы роли можно было бы добавлять из панели
    role = models.CharField(choices=Role.choices, default=Role.ACTOR, max_length=120)
    created = models.DateTimeField(auto_now_add=True)
