from django.contrib import admin
from .models import Back_Test_Trade

@admin.register(Back_Test_Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('trade_type', 'ticker', 'quantity', 'price', 'timestamp')
    list_filter = ('trade_type', 'ticker')
    search_fields = ('ticker',)
    ordering = ('-timestamp',)

    # Optional: Add more customization as needed
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ('timestamp',)
        else:  # Adding a new object
            return ()
