from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def my_reviews_view(request):
    reviews = [
        {"product": "Galaxy Buds Pro", "text": "Отличные наушники!", "rating": 4},
        {
            "product": "Samsung S24 Ultra",
            "text": "Камера 🔥, экран шикарный!",
            "rating": 5,
        },
    ]
    return render(request, "reviews/my_reviews.html", {"reviews": reviews})
