from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm


class HomePageView(TemplateView):
    template_name = 'home.html'


class UserLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                messages.success(request, 'Login successful')
                return HttpResponseRedirect(reverse('products'))
            else:

                messages.error(request, 'Invalid username or password')
                return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request, 'Invalid username or password')
            return HttpResponseRedirect(reverse('login'))


class SignupView(TemplateView):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/signup.html')


class ProductsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'products.html'

    def get(self, request, *args, **kwargs):
        context = {
            'products': Product.objects.all(),
            'form': ProductForm()
        }

        return render(request, 'products.html', context)

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        product_id = request.POST['id']

        if form.is_valid():
            stock = request.POST['stock']

            product = Product.objects.get(pk=product_id)
            product.stock = stock
            product.save()

            messages.success(request, 'Stock updated successfully')
            return HttpResponseRedirect(reverse('products'))
        else:
            messages.error(request, 'Invalid form')
            return HttpResponseRedirect(reverse('products'))
