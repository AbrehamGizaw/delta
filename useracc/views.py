
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.crypto import get_random_string
from django.views import View
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

class UserProfile(LoginRequiredMixin, View):
    template_name = 'user_profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {'user': user}
        return render(request, self.template_name, context)


class Register(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Generate email verification token
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Build the email verification link
            current_site = get_current_site(request)
            verification_url = reverse('useracc:email_verify', kwargs={'uidb64': uidb64, 'token': token})
            verification_link = f'http://{current_site.domain}{verification_url}'

            # Send email with verification link
            subject = 'Email Verification Link'
            message = f'Click the following link to verify your email: {verification_link}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.username]

            send_mail(subject, message, from_email, to_email, fail_silently=False)

            # Set initial status to 'pending' since email verification is pending
            user.status = 'pending'
            user.save()

            messages.success(request, 'Account created successfully. Check your email for the verification link.')
            return redirect('useracc:login')
        

        return render(request, self.template_name, {'form': form})
    
class EmailVerify(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.status = 'email_verified'  # Updated status value
                user.save()
                messages.success(request, 'Email verification successful. Your account is now email verified.')
            else:
                messages.error(request, 'Invalid email verification token.')

        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            messages.error(request, 'Invalid email verification token.')

        return redirect('useracc:login')
    
class Activate(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        if user.status =='email_verified':
            user.status = 'activated'
            user.save()
            messages.success(request, 'Account activation successful.')
        elif user.is_superuser==True:
            user.status='activated'
            user.save()
            messages.success(request, 'Account activation successful.')
        elif user.status=='activated':
            messages.success(request, 'the account is already activated.')

        else:
            messages.warning(request, 'User must verify their email')

        
        return redirect('useracc:staff_page')




class UserLogin(View):
    template_name = 'login.html'

    def get(self, request, ):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, ):
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.status == 'pending' and user.is_superuser==False:
                messages.warning(request, 'Your account is pending approval. Please check your email for verification.')
                
            elif user.status == 'email_verified':
                messages.info(request, 'Your email is verified. Your account is not yet active.')
                
            elif user.status == 'activated' or user.is_superuser==True:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect(reverse('staff:index'))
            
            
        else:
            messages.error(request, 'Invalid login credentials.')

        return render(request, self.template_name, {'form': form})
    
@method_decorator(login_required, name='dispatch')
class UserLogout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('useracc:login')

class StaffPage(LoginRequiredMixin, View):
    template_name = 'user_list.html'

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        context = {'users': users}
        return render(request, self.template_name, context)

class DeleteUser(View):
    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
