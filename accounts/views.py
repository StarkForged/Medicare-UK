from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, RegisterForm


def login_view(request):
    """
    Show login form on GET.
    On POST: validate credentials, log the user in, redirect to dashboard
    (or the `next` URL if Django redirected them here from a protected page).

    BUG FIX: The original used `LoginForm(request, data=request.POST or None)`.
    AuthenticationForm requires `request` as its first argument always —
    passing `data=None` on a GET request is correct, but the `or None` trick
    causes issues because AuthenticationForm doesn't handle data=None cleanly
    in all Django versions. Explicit branching is clearer and always correct.
    """
    # Already logged in — no need to show the login page
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Redirect to the page the user originally tried to visit,
            # or fall back to the main dashboard.
            next_url = request.GET.get('next', 'core:dashboard')
            return redirect(next_url)
    else:
        form = LoginForm(request)   # empty form for GET

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Log the user out and send them to the login page."""
    logout(request)
    return redirect('accounts:login')


def register_view(request):
    """
    Show registration form on GET.
    On POST: create account, log the new user in immediately, redirect to dashboard.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
