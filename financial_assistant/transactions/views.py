from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Transaction
from .forms import TransactionForm



class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/list.html'
    context_object_name = 'transactions'
    paginate_by = 10 


class TransactionFormMixin:
    model=Transaction
    form_class = TransactionForm
    template_name = 'transactions/form.html'
    success_url = reverse_lazy('transactions:list')


class TransactionCreateView(TransactionFormMixin, CreateView):
    pass


class TransactionUpdateView(TransactionFormMixin, UpdateView):
    pass


class TransactionDeleteView(DeleteView):
    model=Transaction
    template_name = 'transactions/delete.html'
    success_url = reverse_lazy('transactions:list')
