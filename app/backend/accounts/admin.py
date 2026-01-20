from django.contrib import admin
from .models import User    

# Registrar o modelo de usuário personalizado no admin do Django
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'escola', 'is_active')
    list_filter = ('user_type', 'escola')
    search_fields = ('username', 'email')
    
