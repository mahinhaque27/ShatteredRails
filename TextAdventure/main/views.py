from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import UserForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from .models import Game
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .forms import TerminalSettingsForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from functools import wraps

# Display home page (first page)
def index(request):
    return render(request, 'index.html')

# enforces that you are authenticated before accessing a page
def logout_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index_2')
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view

@logout_required

# Display register page and process registration data
@logout_required
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create instance of user but don't save it yet
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = True  # Deactivate account till it is confirmed
            user.save()

            # Create instance of game
            game = Game.objects.create(user=user, game_name='akira', health=50, verification='unverified', completion=0, save_state=0)

            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'shatteredrails@gmail.com', [to_email])
            return render(request, 'confirmation_prompt.html')
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'register.html', context)

# Used for email verification
User = get_user_model()
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        return render(request, 'verification_complete.html')
    else:
        return HttpResponse('Activation link is invalid!')

# process login form data and authenticate
@logout_required
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)    
                return redirect('index_2')
        else:
            messages.error(request, "Username and/or Password is Incorrect")
    return render(request, 'login.html')

# display game selection page
def index_2(request):
    return render(request, 'index-2.html')

# display second game
def game_2(request):
    return render(request, 'game-2.html')

# call function to log user out and set status as logged out
def user_logout(request):
    logout(request)
    return redirect('login')

def success(request):
    return render(request, 'success.html')

# display game page, return game state data for user to page
def game(request):
    if request.user.is_authenticated:
        game = Game.objects.get(user=request.user)
        return render(request, 'game.html', {'game': game})
    else:
        return render(request, 'game.html')

# display profile page
def profile(request):
    return render(request, 'profile.html')

# display edit password page
def profilePassword(request):
    return render(request, 'profile-password.html')

# function that process profile form when user updates profile
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['full_name']
        user.email = request.POST['email']
        user.username = request.POST['username']
        user.save()
        
        success_message = "Profile was sucessfully updated."
        return render(request, 'profile.html', {'success_message': success_message})
    else:
        error_message = "Profile failed to update, please try again later"
        return render(request, 'profile.html', {'error_message': error_message})
    
# function that processes edit password form
def edit_password(request):
    if request.method == 'POST':
        user = request.user
        if 'current_password' in request.POST and 'new_password' in request.POST:
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            
            
            authenticated_user = authenticate(username=user.username, password=current_password)
            
            if authenticated_user is not None:
                user.set_password(new_password)
                user.save()
                
                login(request, user)

                success_message = "Password was sucessfully updated."
                return render(request, 'profile-password.html', {'success_message': success_message})
            else:
                error_message = "Invalid current password. Please try again."
                return render(request, 'profile-password.html', {'error_message': error_message})
    return render(request, 'profile.html')

# Save the location of where the user is in game 1 to db
@csrf_exempt
@login_required
def save_game_state(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        save_state = data.get('save_state')

        game = Game.objects.get(user=request.user)
        game.save_state = save_state
        game.add_state(save_state)  

        return JsonResponse({'status': 'success', 'message': 'Game state saved successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# display start page for game 1
def start(request):
    return render(request, 'start.html')
# display start page for game 2
def start1(request):
    return render(request, 'start1.html')

# display help page
def help(request):
    return render(request, 'help.html')

# display home page
def index(request):
    is_authenticated = request.user.is_authenticated
    context = {'is_authenticated': is_authenticated}
    return render(request, 'index.html', context)

# get game 1 completion value from db for the user and send to front end
def get_progress(request):
    try:
        game = Game.objects.get(user=request.user)
        completion = game.completion
        return JsonResponse({'completion': completion})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Game object not found for the current user'}, status=404)

# Processes the settings popup
def game_settings(request):
    if request.method == 'POST':
        form = TerminalSettingsForm(request.POST)
        if form.is_valid():
            return redirect('game-settings')  
    else:
        form = TerminalSettingsForm(initial={
            'background_color': request.session.get('background_color', '#121212'),
            'font_color': request.session.get('font_color', '#FFFFFF'),
        })

    context = {'form': form}
    return render(request, 'game-2.html', context)


# delete account from db on the profile page
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user

        user.delete()

        logout(request)
  
        return redirect('login') 
    else:
        pass

# process the forgot username form
def forgot_username(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            username = user.username
            
            
            send_mail(
                'Your Username',
                f'Your username is: {username}',
                'shatteredrails@gmail.com',  
                [email],            
                fail_silently=False,
            )
            
       
            return JsonResponse({'success': True, 'message': 'Username sent successfully. Check your email.'})
        except User.DoesNotExist:
           
            return JsonResponse({'success': False, 'message': 'Email address not found.'})

    
    return render(request, 'forgot_username.html')

# send email associated with user account
def send_reset_password_email(request, user):
   
    token = default_token_generator.make_token(user)

  
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    
    reset_link = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')

    
    subject = 'Reset your password'
    message = render_to_string('reset_password_email.html', {'reset_link': reset_link})


    send_mail(subject, message, 'shatteredrails@gmail.com', [user.email])

# process the forgot password form
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_link = reverse('reset_password', kwargs={'user_id': user.id})
            reset_link = request.build_absolute_uri(reset_link)
            send_mail(
                'Reset Password',
                f'Click the following link to reset your password: {reset_link}',
                'shatteredrails@gmail.com',
                [email],
                fail_silently=False,
            )
            success_message = 'Password reset link sent successfully. Check your email.'
            return render(request, 'forgot_password.html', {'success_message': success_message})
        except User.DoesNotExist:
            error_message = 'Email address not found.'
            return render(request, 'forgot_password.html', {'error_message': error_message})

 
    return render(request, 'forgot_password.html')

# send email 
def send_reset_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_link = reverse('reset_password', kwargs={'user_id': user.id})
            reset_link = request.build_absolute_uri(reset_link)
            send_mail(
                'Reset Password',
                f'Click the following link to reset your password: {reset_link}',
                'shatteredrails@gmail.com',
                [email],
                fail_silently=False,
            )
            success_message = 'Password reset link sent successfully. Check your email.'
            return render(request, 'forgot_password.html', {'success_message': success_message})
        except User.DoesNotExist:
            error_message = 'Email address not found.'
            return render(request, 'forgot_password.html', {'error_message': error_message})


    return render(request, 'forgot_password.html')

# display reset password page
def reset_password(request, user_id):
    return render(request, 'reset_password.html', {'user_id': user_id})

# process forgot password form and update in db
def update_password(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user = User.objects.get(pk=user_id)
            user.set_password(new_password)
            user.save()
            return redirect('login')  
        else:
            return render(request, 'reset_password.html', {'error_message': 'Passwords do not match.'})


