from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def available(self):
        return self.copies - self.loan_set.filter(returned=None).count()


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed = models.DateTimeField(default=datetime.now)
    returned = models.DateTimeField(null=True, blank=True)

    def due(self):
        return self.borrowed + timedelta(days=settings.LOAN_DAYS)

    def is_late(self):
        return self.returned is None and datetime.now() > self.due()
