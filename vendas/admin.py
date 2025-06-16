from django.contrib import admin
from .models import Produto
from .models import Produto, Orcamento, ItemOrcamento

admin.site.register(Produto)
admin.site.register(Orcamento)
admin.site.register(ItemOrcamento)

# Register your models here.
