from django.contrib import admin

from .models import Category, Transaction, Tag, Currency

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'date',
        'amount',
        'currency',
    )
    list_editable = (
        'amount',
        'currency',
    )    
    search_fields = ('description',) 
    list_filter = ('category',)
    list_display_links = ('description',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Tag)
admin.site.register(Currency)
admin.site.register(Category)
