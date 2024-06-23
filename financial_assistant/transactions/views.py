from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, FormView)
from .models import Transaction, Category, Currency, Card
from .forms import TransactionForm, PDFUploadForm
from .utils import parse_pdf
from . import dash_app


class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/list.html'
    context_object_name = 'transactions'
    paginate_by = 10


class TransactionFormMixin:
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/form.html'
    success_url = reverse_lazy('transactions:list')


class TransactionCreateView(TransactionFormMixin, CreateView):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(TransactionFormMixin, UpdateView):
    pass


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transactions/delete.html'
    success_url = reverse_lazy('transactions:list')


def dash(request):
    return render(request, 'transactions/dash.html')


class UploadPDFView(FormView):
    template_name = 'transactions/upload.html'
    form_class = PDFUploadForm
    success_url = reverse_lazy('transactions:list')

    def form_valid(self, form):
        pdf_file = self.request.FILES['pdf_file']
        transactions_list = parse_pdf(pdf_file)
        user = self.request.user

        for trans in transactions_list:
            card_number = trans['card_number']
            card, created = Card.objects.get_or_create(
                user=user,
                number=card_number,
                defaults={'expiry_date': '2024-12-31', 'name_on_card': 'Default Name'}
            )

            Transaction.objects.create(
                user=user,
                date=trans['date_time_operation'].date(),
                description=trans['description'],
                category=Category.objects.get(name="Продукты"),  # Replace with appropriate category
                type='income' if trans['amount'] > 0 else 'expense',
                amount=trans['amount'],
                currency=Currency.objects.get(code='RUB'),  # Replace with appropriate currency
                notes=trans.get('additional_info', ''),
                status='completed',
                payment_method='other',
                card=card
            )

        return super().form_valid(form)

