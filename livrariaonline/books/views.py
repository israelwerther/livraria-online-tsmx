from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, View, CreateView
from django.urls import reverse, reverse_lazy
from .forms import CustomUserCreationForm
from .models import Book, Cart, CartItem, Order
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.db.models import Q



class MyBooksListView(ListView):
    template_name = 'books/books.html'
    context_object_name = 'books'
    queryset = Book.objects.all()
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('books_list')

    def get_queryset(self):
        queryset = Book.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        books = paginator.get_page(page)
        context['books'] = books
        return context

class CartListView(ListView):
    model = CartItem
    template_name = 'books/cart.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        
        if user.is_authenticated and user.my_cart():
            queryset.filter(cart__user=user)
        
        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class CartItemRemoveView(View):
    template_name = 'books/cart.html'

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        cart = get_object_or_404(Cart, session_key=request.session.session_key)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return redirect('cart')


class CheckoutTemplateView(TemplateView):
    template_name = 'books/checkout.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            redirect('/login')
        
        return super().dispatch(request, *args, **kwargs)
    



class OrderSuccessRedirectView(View):
    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id', None)
        if order_id:
            request.session['order_id'] = None
            return redirect(reverse('books:order_success', kwargs={'order_id': order_id}))
        else:
            return redirect(reverse('books:books_list'))


class OrderSuccessView(View):
    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'books/order_success.html', {'order': order})


class MyOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'books/my_orders.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
        
            redirect(reverse_lazy('books:my_orders'))
            
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        
        next_url = self.request.GET.get('next')
        
        if next_url:
        
            return next_url
        
        return reverse_lazy('books:my_orders')
        

    def form_valid(self, form):

        response = super().form_valid(form)

        next_url = self.request.GET.get('next')

        data = self.request.POST

        user = self.request.user

        cart = user.my_cart()

        if next_url == reverse_lazy('books:checkout'):
            cart.clean_cart()
        
        for index, book_id in enumerate(data.getlist('book')):    
            cart.add_book(book_id=book_id, quantity=data.getlist('quantity')[index] if data.getlist('quantity')[index] else 1)
        
        return response
    
class CustomSignUpView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
