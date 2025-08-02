from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

@login_required
def my_reviews_view(request):
    reviews = Review.objects.filter(user=request.user).select_related("product")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews:my_reviews')
    else:
        form = ReviewForm()

    return render(request, 'reviews/my_reviews.html', {
        'reviews': reviews,
        'form': form
    })
