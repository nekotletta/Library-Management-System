from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.
@csrf_protect
def login_user(request):
    title = 'Login'
    extra_context = {
        'title': title,
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # tenemos que verificar que el usuario haya activado la cuenta de antemano. Si no es el caso,
        # se notifica que verifique el correo y la active 
        # user_active = CustomUser.objects.filter(email=email).values_list('is_active', flat=True).first()
        # if not user_active:
        #     messages.error(request, "Cuenta inactiva. Revise su correo electrónico para activar su cuenta.")
        #     return redirect('authentication:login')
        
        # else:
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            # Check if the user is an admin
            if user.is_superuser or  user.is_staff:
                return redirect('/administration/')  # Redirect to the admin page

            else:
                return redirect('/dashboard/')
                # else:
                #     return redirect('user_info:create_profile', id=request.user.id)  # Redirect to the user page

        else:
            messages.error(request, "Correo electrónico o contraseña incorrecta.")
            return redirect('authentication:login')

    return render(request, 'login.html', extra_context)