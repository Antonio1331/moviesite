from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Genre, Movie, UserProfile
from .forms import MovieForm, GenreForm


class MainView(ListView):
    model = Movie
    template_name = "moviesite/main.html"
    context_object_name = "movies"

    def get_queryset(self):
        return Movie.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["title"] = "main"
        messages.info(self.request, "Xush kelibsiz! Asosiy sahifasidasiz.")
        return context


class AboutView(TemplateView):
    template_name = "moviesite/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "about"
        return context


class MoviesByGenre(ListView):
    model = Movie
    template_name = "moviesite/main.html"
    context_object_name = "movies"

    def get_queryset(self):
        return Movie.objects.filter(genre_id=self.kwargs["genre_id"], published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = get_object_or_404(Genre, pk=self.kwargs["genre_id"])
        context["genres"] = Genre.objects.all()
        context["title"] = genre.type
        return context


class MovieDetail(DetailView):
    model = Movie
    template_name = "moviesite/movie.html"
    context_object_name = "movie"
    pk_url_kwarg = "movie_id"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context


class MovieCreate(UserPassesTestMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "moviesite/add_movie.html"
    success_url = reverse_lazy("main")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Film muvaffaqiyatli qo'shildi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Film qo'shishda xatolik yuz berdi!")
        return super().form_invalid(form)


class MovieUpdate(UserPassesTestMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = "moviesite/update_movie.html"
    pk_url_kwarg = "movie_id"
    success_url = reverse_lazy("main")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Film muvaffaqiyatli yangilandi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Film yangilashda xatolik yuz berdi!")
        return super().form_invalid(form)


class MovieDelete(UserPassesTestMixin, DeleteView):
    model = Movie
    template_name = "moviesite/delete_movie.html"
    pk_url_kwarg = "movie_id"
    success_url = reverse_lazy("main")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Film muvaffaqiyatli o'chirildi!")
        return super().delete(request, *args, **kwargs)


class GenreCreate(UserPassesTestMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = "moviesite/add_genre.html"
    success_url = reverse_lazy("main")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Janr muvaffaqiyatli qo'shildi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Janr qo'shishda xatolik yuz berdi!")
        return super().form_invalid(form)


class GenreUpdate(UserPassesTestMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = "moviesite/update_genre.html"
    pk_url_kwarg = "genre_id"
    success_url = reverse_lazy("main")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Janr muvaffaqiyatli yangilandi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Janr yangilashda xatolik yuz berdi!")
        return super().form_invalid(form)


class GenreDelete(UserPassesTestMixin, DeleteView):
    model = Genre
    template_name = "moviesite/delete_genre.html"
    pk_url_kwarg = "genre_id"
    success_url = reverse_lazy("main")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Janr muvaffaqiyatli o'chirildi!")
        return super().delete(request, *args, **kwargs)


class ProfileDetail(DetailView):
    model = UserProfile
    template_name = "moviesite/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        user = get_object_or_404(User, username=self.kwargs["username"])
        return get_object_or_404(UserProfile, user=user)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "moviesite/profile_detail.html"
    login_url = "/login/"


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Parollar mos emas!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bunday foydalanuvchi allaqachon mavjud!")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Ro‘yxatdan o‘tdingiz, endi login qiling!")
        return redirect("login")

    return render(request, "moviesite/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {username}!")
            return redirect("main")
        else:
            messages.error(request, "Login yoki parol noto‘g‘ri!")
            return redirect("login")

    return render(request, "moviesite/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Siz tizimdan chiqdingiz.")
    return redirect("main")

def movie_list(request):
    movies = Movie.objects.all().order_by('-id')
    paginator = Paginator(movies, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'moviesite/main.html', {'page_obj': page_obj})
