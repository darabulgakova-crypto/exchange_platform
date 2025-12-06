from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg


from .models import Product, Review, Profile
from .forms import ReviewForm

def product_list(request):
    products = (
        Product.objects
        .filter(is_active=True)
        .select_related('owner')
        .prefetch_related('images', 'reviews')
        .annotate(
            review_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        )
    )
    return render(request, 'market/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    images = product.images.all()
    return render(request, 'market/product_detail.html', {
        'product': product,
        'images': images,
    })


def product_reviews(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    reviews = product.reviews.select_related('author').all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Можно сделать редирект на логин, но для простоты пока просто рендерим с ошибкой
            form = ReviewForm(request.POST)
            error = 'Чтобы оставить отзыв, войдите в систему.'
        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.author = request.user
                review.save()
                return redirect('market:product_reviews', pk=product.pk)
            error = None
    else:
        form = ReviewForm()
        error = None

    return render(request, 'market/product_reviews.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'error': error,
    })


@login_required
def profile_view(request):
    # Попробуем взять профиль, если его нет — можно создать "по месту"
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'market/profile.html', {'profile': profile})
