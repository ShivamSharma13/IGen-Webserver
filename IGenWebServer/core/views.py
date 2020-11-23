from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
import os
from .models import PRS, PUBLIC_DNA_CHOICES, SELF_IDENTIFIED_CHOICES
from IGenWebServer.settings import BASE_DIR

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
	if request.method == 'GET':
		return render(request, 'signup.html')
	elif request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		reenter_password = request.POST['reenter-password']
		username = email.split('@')[0]
		if password != reenter_password:
			return render(request, 'signup.html', {'error': "Passwords do not match."})

		#Check if the username already exists.
		if_usernames = User.objects.filter(email = email).count()
		if if_usernames != 0:
			return render(request, 'signup.html', {'error': "Please choose a different email. This email exists."})

		#Create User object and authenticate.
		user = User.objects.create_user(email = email, username = username, password = password)
		user = authenticate(request, username=username, password=password)

		#Log in the user.
		if user is not None:
			auth_login(request, user)
			return redirect('dashboard', permanent = True)


def login(request):
	if request.method == 'GET':
		return render(request, 'login.html')

	elif request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		username = email.split('@')[0]
		user = authenticate(request, username=username, password=password)

		#Log in the user.
		if user is not None:
			auth_login(request, user)
			return redirect('dashboard', permanent = True)
		else:
			return render(request, 'login.html', {'error': 'Password does not match'})

def logout(request):
	auth_logout(request)
	return render(request, 'homepage.html')


@login_required(login_url='/login/')
def dashboard(request, redirect_kwargs = None):
	if request.method == 'GET':
		if redirect_kwargs == None:
			return render(request, 'dashboard.html')
		else:
			if "error" in redirect_kwargs:
				user = request.user
				prs_files = user.prs.all()
				redirect_kwargs['prs'] = prs
				return render(request, 'dashboard.html', redirect_kwargs)


@login_required(login_url='/login/')
def upload_dna(request):
	if request.method == 'POST':
		user = request.user
		dna_source = request.POST['source']
		internal_usage_permission = request.POST['auth']
		file = request.FILES['dna-file']
		self_identified_ancestry = request.POST['self-identified-ancestry']
		eng_to_bool = {'Yes': True, 'No': False}
		if internal_usage_permission not in eng_to_bool or dna_source not in [i[0] for i in PUBLIC_DNA_CHOICES] or self_identified_ancestry not in [i[0] for i in SELF_IDENTIFIED_CHOICES]: 
			return redirect('dashboard', {'error': 'Form fields are incorrect.'} , permanent = True)
		home_dir = os.path.join(BASE_DIR, "data", user.username)

		model_object_prs = PRS(user = user, 
								home_dir = home_dir, 
								dna_source = dna_source, 
								internal_usage_permission = eng_to_bool[internal_usage_permission], 
								self_identified_ancestry = self_identified_ancestry)

		#Save the file.
		file_dir = os.path.join(home_dir, str(model_object_prs.uuid))
		os.makedirs(file_dir)

		with open(os.path.join(file_dir, 'input-file.txt'), "wb") as f:
			f.write(file.read())

		model_object_prs.save()
		return redirect('dashboard')
	elif request.method == 'GET':
		return redirect('dashboard',  permanent = True)


@login_required(login_url='/login/')
def check_status(request):
	user = request.user
	return None


@login_required(login_url='/login/')
def show_results(request):
	user = request.user
	return render(request, 'results.html')


def run_pipeline(*args):
	pass
	'''
	1. Raw file comes in.
	2. Convert to VCF file. [Sara]
	3. Imputation and Phasing. [Sara]
	4. One Time - PCA [Saving]
	5. PRS []
	6. Percentile Calculations.
		Output Expectation:
			 HIV - 45%
			 Hep-B - 55%
			 Chicken Pox - 65%
	7. Generate Graphs.
	'''