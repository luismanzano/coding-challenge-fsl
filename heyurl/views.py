from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateNewShortUrl
from heyurl.models import Url, Click
from datetime import datetime
import random
import string
from .helpers import validate_url
from django.shortcuts import redirect as django_redirect

def index(request):
    urls = Url.objects.order_by('-created_at')
    context = {'urls': urls}
    return render(request, 'heyurl/index.html', context)

def store(request): #create the short url
    # FIXME: Insert a new URL object into storage



    if request.method == 'POST':
        form = CreateNewShortUrl(request.POST)


        if validate_url(request.POST["original_url"]) == False:
            return HttpResponse("The URL is not Valid, please try with a different one")

        if Url.objects.filter(original_url=request.POST["original_url"]):
            return HttpResponse("There is already a short url for this website, please try with a different one")

        if form.is_valid():
            print("VALID FORM")
            original_website = form.cleaned_data["original_url"]
            random_chars_list = list(string.ascii_letters)
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            random_chars_list += numbers
            random_chars = ''
            for i in range(5):
                random_chars += random.choice(random_chars_list)
            while len(Url.objects.filter(short_url=random_chars)) != 0:
                for i in range(5):
                    random_chars += random.choice(random_chars_list)
            new_date = datetime.now()
            new_url = Url(original_url=original_website, short_url=random_chars, clicks=0, created_at=new_date,
                          updated_at=new_date)
            new_url.save()
            form = CreateNewShortUrl()
            context = {'form': form}
            return django_redirect('/')

        else:
            print("INVALID FORM")
            form = CreateNewShortUrl()
            context = {'form': form}
            return render(request, 'heyurl/index.html', context)

    return HttpResponse("Storing a new URL object into storage")

#THE VIEW THAT RETRIEVES THE DATA FOR THE DATA INFO PANEL
def data_panel(request, url):
    today = datetime.now()
    print("DATA PANEL URL")
    ident = Url.objects.filter(short_url=url)
    ident = ident[0].id
    clicks_this_month = Click.objects.filter(url=ident, created_at__year=today.year, created_at__month=today.month)
    safari = Click.objects.filter(url=ident, browser__contains='safari')
    chrome = Click.objects.filter(url=ident, browser__contains='chrome')
    firefox = Click.objects.filter(url=ident, browser__contains='firefox')
    mobile = Click.objects.filter(url=ident, platform='Mobile')
    pc = Click.objects.filter(url=ident, platform='PC')
    print("PC", pc)
    context = {
        'url': url,
        'clicks': len(clicks_this_month),
        'safari': len(safari),
        'chrome': len(chrome),
        'firefox': len(firefox),
        'mobile': len(mobile),
        'pc': len(pc),
    }

    return render(request, 'heyurl/data_panel.html', context)

#Log to db with user agent, browser and redirect to the website the customer wants to go
def redirect(request, url):
    current_obj = Url.objects.filter(short_url=url)
    #CREATING DATE
    now_date = datetime.now()
    #GETTING THE DEVICE
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        device = "Mobile"
    else:
        device = "PC"
    #GETTING THE BROWSER
    browser = request.user_agent.browser.family
    #SAVING THE CLICK
    new_click = Click(url=current_obj[0], created_at=now_date, browser=browser, platform=device, updated_at=now_date)
    new_click.save()
    Url.objects.filter(short_url=url).update(clicks=current_obj[0].clicks + 1)

    if not validate_url(current_obj[0].original_url):
        return render(request, '404.html')

    context = {
        'obj': current_obj[0]
    }

    return django_redirect(current_obj[0].original_url)
