from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, 'homepage.html')

def about(request):
	return render(request, 'signup.html')

def resources(request):
	return render(request, 'signup.html')

def docs(request):
	return render(request, 'signup.html')


def signup(request):
	return render(request, 'signup.html')


def login(request):
	if request.method == 'GET':
		return render(request, 'login.html')

	elif request.method == 'POST':
		return render(request, 'dashboard.html')