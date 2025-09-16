from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Genre, Movie
from .forms import MovieForm
from .models import UserProfile

# Create your views here.

def main(request: HttpRequest):
    messages.info(request, "Xush kelibsiz! Asosiy sahifasidasiz.")
    genres = Genre.objects.all()
    movies = Movie.objects.filter(published=True)

    context = {
        'genres': genres,
        'movies': movies,
        'title': 'main',
    }

    return render(request, 'moviesite/main.html', context)

def about(request: HttpRequest):
    context = {
        'title': 'about',
    }

    return render(request, 'moviesite/about.html', context)

def by_genre(request: HttpRequest, genre_id):
    movies = Movie.objects.filter(genre_id=genre_id, published=True)
    genres = Genre.objects.all()
    genre = get_object_or_404(Genre, pk=genre_id)

    context = {
        'movies': movies,
        'genres': genres,
        'title': genre.type,
    }

    return render(request, 'moviesite/main.html', context)

def by_movie(request: HttpRequest, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, published=True)

    movie.views += 1
    movie.save()

    context = {
        'movie': movie,
        'title': movie.title,
    }

    return render(request, 'moviesite/movie.html', context)

# POST
def add_movie(request: HttpRequest):
    if request.user.is_staff:
        if request.method == 'POST':
            form = MovieForm(request.POST, files=request.FILES)
            if form.is_valid():
                movie = form.save()
                messages.success(request, "Maqola muvaffaqiyatli qo'shildi!")
                return redirect("by_movie", movie_id=movie.pk)
            else:
                messages.error(request, "Ma'lumotlar qo'shishda xatolik yuz berdi!")
        else:
            form = MovieForm()

        context = {
            "form": form,
            "title": "Film qo'shish"
        }
        return render(request, 'moviesite/add_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')
    
# UPDATE
def update_movie(request: HttpRequest, movie_id: int):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)

        if request.method == 'POST':
            form = MovieForm(request.POST, files=request.FILES, instance=movie)
            if form.is_valid():
                movie = form.save()
                messages.success(request, "Film muvaffaqiyatli yangilandi!")
                return redirect("by_movie", movie_id=movie.pk)
            else:
                messages.error(request, "Ma'lumotlar qo'shishda xatolik yuz berdi!.")
        else:
            form = MovieForm(instance=movie)

        context = {
            "form": form,
            "title": "Filmni yangilash"
        }
        return render(request, 'moviesite/update_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')
    
# DELETE
def delete_movie(request: HttpRequest, movie_id):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)
        messages.warning(request, "Filmni o'chirmoqchimisiz?")
        if request.method == 'POST':
            movie.delete()
            messages.success(request, "Film muvaffaqiyatli o'chirildi!")
            return redirect("main")
        context = {
            'movie': movie,
            'title': "Filmni o'chirish"
        }
        return render(request, 'moviesite/delete_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')

def profile_detail(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Bunday foydalanuvchi topilmadi")

    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        raise Http404("Profil topilmadi")

    return render(request, "moviesite/profile_detail.html", {"profile": profile})

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