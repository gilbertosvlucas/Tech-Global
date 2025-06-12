from django.contrib.auth.views import LoginView, LogoutView

class LoginUsuario(LoginView):
    template_name = 'clientes/login.html'

class LogoutUsuario(LogoutView):
    pass
