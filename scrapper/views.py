from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.views.decorators.cache import never_cache
from .models import UserLinks
import requests
import bs4

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
REQUEST_HEADER = {
    "User-Agent" : USER_AGENT,
    "Accept-Language" : "en-US, en;q=0.5"
}

def url_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    
def get_page_html(url):
    res = requests.get(url=url, headers=REQUEST_HEADER)
    return res.content

def get_profile_username(soup):
    username = soup.find('span', attrs={
        'class' : 'p-nickname vcard-username d-block'
    })
    return username.text.strip()

def get_profile_repositories(soup):
    a_tag = soup.find('a', id='repositories-tab')
    span_counter = a_tag.find('span', attrs={
        'class' : 'Counter'
    })
    return span_counter.text.strip()

def get_profile_titles_and_descriptions_and_urls(soup, url):
    titles_and_descriptions_and_urls = {}
    main_div = soup.find_all('div', class_='col-10 col-lg-9 d-inline-block')
    for div in main_div:
        a_tag = div.find('a', attrs={
            'itemprop' : 'name codeRepository'
        })
        div_in_div = div.find_all('div')
        second_div = div_in_div[1]
        if second_div.find('p'):
            titles_and_descriptions_and_urls[a_tag.text.strip()] = {
                'description' : second_div.find('p').text.strip(),
                'url_for_repo' : url + '/' + a_tag.text.strip()
            }
        else:
            titles_and_descriptions_and_urls[a_tag.text.strip()] = {
                'description' : None,
                'url_for_repo' : url + '/' + a_tag.text.strip()
            }
    return titles_and_descriptions_and_urls

def get_profile_languages_used(soup):
    languages = []
    details_tag = soup.find('details', id='language-options')
    label_tags = details_tag.find_all('label', class_='SelectMenu-item')
    for label in label_tags:
        languages.append(label.find('span').text.strip())
    return languages[1:]


def scrape_github_profile(url):
    if not url_exists(url):
        return {"error": "URL does not exist"}
    
    new_url = url + "?tab=repositories"
    
    profile_info = {}
    html = get_page_html(url=new_url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    titles_and_descriptions_and_urls = get_profile_titles_and_descriptions_and_urls(soup, url)
    repositories = 0
    for key in titles_and_descriptions_and_urls.keys():
        repositories += 1
    profile_info['username'] = get_profile_username(soup)
    profile_info['total_repositories'] = repositories
    profile_info['titles_and_descriptions'] = titles_and_descriptions_and_urls
    profile_info['languages_used'] = get_profile_languages_used(soup)
    return JsonResponse(profile_info)

@never_cache
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('user_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        phone_no = request.POST.get('phone_no', '').strip()

        if not username or not email or not password or not phone_no:
            return JsonResponse({"error": "All fields are required."})  # make a template for this
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email is already registered. Use another email to register"})
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username is already taken. Use another username to register"})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.profile.phone_no = phone_no
        user.save()
        return redirect('login')
    return render(request, 'signin.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            user = None
        
        if user:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session["login"] = True
                auth_login(request, user)
                return redirect('index')
            else:
                return render(request, 'login.html', {'emailPasswordError': True})
        else:
            return render(request, 'login.html', {'error': True})
    return render(request, 'login.html')

@login_required(login_url="/login/")
@never_cache
def index(request):
    if request.method == 'POST':
        link = request.POST.get('link', '')
        user_link = UserLinks(url=link, user=request.user)
        user_link.save()
        result = scrape_github_profile(link)
        return result
        
    return render(request, 'index.html')

@never_cache
def custom_logout(request):
    Session.objects.filter(session_key=request.session.session_key).delete()
    logout(request)
    return redirect(reverse('login'))


def custom_page_not_found(request, path):
    return render(request, '404.html', {'path': path}, status=404)
