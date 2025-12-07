from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q

from .models import Product, ProductImage, Review, Profile
from .forms import ReviewForm, ProfileForm, ProductForm
# Updated profile and product editing functionality


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
    owner_profile = Profile.objects.filter(user=product.owner).first()
    return render(request, 'market/product_detail.html', {
        'product': product,
        'images': images,
        'owner_profile': owner_profile,
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
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'market/profile.html', {
        'profile': profile,
    })

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён.')
            return redirect('market:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'market/profile_edit.html', {
        'profile': profile,
        'form': form,
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()

            image = form.cleaned_data.get('image')
            if image:
                ProductImage.objects.create(product=product, image=image)

            messages.success(request, 'Товар успешно добавлен.')
            return redirect('market:product_detail', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, 'market/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            image = form.cleaned_data.get('image')
            if image:
                ProductImage.objects.create(product=product, image=image)
            messages.success(request, 'Товар успешно обновлён.')
            return redirect('market:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'market/edit_product.html', {
        'form': form,
        'product': product,
    })


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар был удалён.')
        return redirect('market:profile')

    return render(request, 'market/confirm_delete_product.html', {
        'product': product,
    })
