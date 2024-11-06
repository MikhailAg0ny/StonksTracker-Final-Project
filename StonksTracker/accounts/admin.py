from django.contrib import admin
from .models import Watchlist, PriceHistory

admin.site.register(Watchlist)
admin.site.register(PriceHistory)
