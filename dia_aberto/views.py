from django.shortcuts import redirect

def error404(request, exception):
    return redirect('utilizadores:mensagem', 5)