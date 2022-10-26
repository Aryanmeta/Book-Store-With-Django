from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Book
from .forms import CommentForm


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    template_name = 'books/book_list.html'
    context_object_name = 'books'


# class BookDetailView(generic.DetailView):
#     model = Book
#     template_name = 'books/book_detail.html'
@login_required
def BookDetailView(request, pk):
    # get book object
    book = get_object_or_404(Book, pk=pk)
    # get book comments
    book_comment = book.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    return render(request, 'books/book_detail.html', {'book': book,
                                                      'comments': book_comment,
                                                      'comment_form': comment_form,
                                                      })


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ('title', 'author', 'description', 'price', 'cover', )
    template_name = 'books/book_create.html'


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    fields = ('title', 'author', 'description', 'price', 'cover', )
    template_name = 'books/book_update.html'


class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('book_list')
