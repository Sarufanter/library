from django.db import models

# Create your models here.

from django.urls import reverse, reverse_lazy  # To generate URLS by reversing URL patterns


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
        , verbose_name='Жанри')

    class Meta:
        verbose_name='жанр'
        verbose_name_plural = 'Жанри'

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    class Meta:
        verbose_name='мову оригіналу'
        verbose_name_plural = 'Мови оригіналу'

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200, verbose_name='Назви книг')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book", verbose_name='Коротко про книгу')
    isbn = models.CharField(max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, verbose_name='Мова оригіналу')
    is_anonsed = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    year_of_creation = models.IntegerField()
    
    class Meta:
        ordering = ['title', 'author']
        verbose_name='книгу'
        verbose_name_plural = 'Книги'

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Жанри'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


import uuid  # Required for unique book instances
from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a borrower


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('book',on_delete=models.RESTRICT, null=True, verbose_name='Назва книги')
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True, verbose_name='Дата повернення')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ким повернуто')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('d', 'На обслуговуванні'),
        ('o', 'Зайнято'),
        ('a', 'Доступно'),
        ('r', 'Зарезервовано'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability',
        verbose_name='Статус')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)
        verbose_name='статус книги'
        verbose_name_plural = 'Статус книги'

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name='Фамілія')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата народження')
    date_of_death = models.DateField(null=True, blank=True, verbose_name='Дата смерті')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    summary_author = models.TextField(max_length=1000, null=True, help_text="Enter a brief description of the book",
                               verbose_name='Коротко про книгу')

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'автора'
        verbose_name_plural = 'Автори'

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0} {1}'.format(self.first_name, self.last_name)


from django.db import models
from django.urls import reverse


from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('admin_event_edit', args=(self.id,))
        #url = reverse('event_edit', args=(self.id,))
        return f'<a href="{ url }"> {self.title} </a>'

    class Meta:
        verbose_name = 'події'
        verbose_name_plural = 'Події'

    def __str__(self):
        """String for representing the Model object."""
        return '{0}'.format(self.title)