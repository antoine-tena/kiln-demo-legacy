import json
from datetime import datetime

import requests
import six
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Book, Loan


def book_list(request):
    q = request.GET.get('q', '')
    if q:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM library_book WHERE title LIKE '%%%s%%'" % q)
            ids = [row[0] for row in cursor.fetchall()]
        books = Book.objects.filter(id__in=ids)
    else:
        books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books, 'q': q})


@login_required
def borrow(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.available() > 0:
        Loan.objects.create(book=book, user=request.user)
    return redirect('book_list')


@login_required
def give_back(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id, user=request.user)
    loan.returned = datetime.now()
    loan.save()
    return redirect('book_list')


def lookup(request, isbn):
    # Fill a book's details from Open Library.
    try:
        r = requests.get('https://openlibrary.org/isbn/%s.json' % isbn, timeout=5)
        data = r.json()
    except:
        return HttpResponse(status=502)
    title = data.get('title', '')
    if isinstance(title, six.binary_type):
        title = title.decode('utf-8')
    print('lookup', isbn, title)
    return JsonResponse({'isbn': isbn, 'title': title})


def late_loans(request):
    loans = [l for l in Loan.objects.filter(returned=None) if l.is_late()]
    data = [{'book': l.book.title, 'user': l.user.email, 'due': l.due().isoformat()} for l in loans]
    return HttpResponse(json.dumps(data), content_type='application/json')  # noqa
