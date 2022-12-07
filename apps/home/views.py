from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.shortcuts import render, redirect
import pandas as pd
import plotly.express as px
import plotly.io as io
import requests
from sodapy import Socrata
from datetime import datetime
from . import models
from . import forms


#@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def recall_dash(request):
    #url = "https://datahub.transportation.gov/resource/6axg-epim.json"
    #r = requests.get(url)
    #data = pd.read_json(r.text)

    client = Socrata("datahub.transportation.gov", None)
    results = client.get("6axg-epim", limit=10000)
    recall_df = pd.DataFrame.from_records(results)
    recall_df = recall_df.filter(items=['report_received_date', 'manufacturer', 'subject', 'component', 'recall_type',
                                    'potentially_affected', 'corrective_action', 'mfr_campaign_number'])
    recall_df = recall_df.assign(corrective_action_in=lambda x: x.corrective_action is not None)
    recall_df = recall_df.drop(columns=['corrective_action'])
    recall_df['month_year'] = pd.to_datetime(recall_df['report_received_date']).dt.to_period('M')
    recall_df.drop(columns=['report_received_date'])

    timeseries = recall_df.groupby(['month_year'])['month_year'].count().reset_index(name='count')
    timeseries['month_year'] = timeseries['month_year'].astype(str)
    timeseries['month_year'] = pd.to_datetime(timeseries['month_year'])
    timeseries = timeseries.sort_values(by='month_year')
    time_fig = px.line(timeseries, x='month_year', y='count', title = "Total Number of Recalls per Month",
            labels={'count':'Number of Recalls', 'month_year': 'Date'})
    time_fig.update_layout(font=dict(size=18))
    time_fig_text = io.to_html(time_fig, include_plotlyjs='cdn', full_html=False)

    top_10 = recall_df.groupby(['manufacturer'])['manufacturer'].count().reset_index(name='count')
    top_10 = top_10.nlargest(10, 'count')
    manu_fig = px.bar(top_10, x = 'manufacturer', y = 'count', title="Top 10 Manufacturers by Number of Recalls",
            labels={'count':'Total Number of Recalls', 'manufacturer':'Manufacturer'}, color = 'manufacturer',
            color_discrete_sequence=px.colors.qualitative.Light24)
    manu_fig.update_layout(showlegend=False, font=dict(size=18))
    manu_fig.update_xaxes(tickfont=dict(size=12))
    manu_fig_text = io.to_html(manu_fig, include_plotlyjs='cdn', full_html=False)

    top_comp = recall_df.loc[:,['manufacturer', 'potentially_affected', 'component']]
    top_comp['potentially_affected'] = top_comp['potentially_affected'].fillna(0)
    top_comp['potentially_affected'] = top_comp['potentially_affected'].astype(int)
    top_comp['component'] = top_comp['component'].astype("category")
    top_comp = top_comp.groupby(["component"]).sum(["potentially_affected"]).reset_index()
    top_comp = top_comp.nlargest(5, 'potentially_affected')
    comp_fig = px.bar(top_comp, x = 'component', y = 'potentially_affected',
            title="Top Sum of Potentially Affected Components Globally",
            labels={'potentially_affected':'Potentially Affected Units', 'component':'Component'},
            color_discrete_sequence=px.colors.qualitative.Dark24_r)
    comp_fig.update_layout(font=dict(size=18))
    comp_fig.update_xaxes(tickfont=dict(size=12))
    comp_fig_text = io.to_html(comp_fig, include_plotlyjs='cdn', full_html=False)

    components = recall_df
    components = components.groupby('component').size().reset_index(name='counts')
    components = components.nlargest(10, 'counts')
    pie_fig = px.bar(components, y = 'counts', x = 'component', title = "Top Share of All Recalls by Component",
                        labels={'component':'Component','counts':'Number of Recalls'},
                        color='component', color_discrete_sequence=px.colors.qualitative.Pastel)
    pie_fig.update_layout(showlegend=False, font=dict(size=18))
    pie_fig.update_xaxes(tickfont=dict(size=12))
    pie_fig_text = io.to_html(pie_fig, include_plotlyjs='cdn', full_html=False)

    rec_type = recall_df.groupby("recall_type", as_index=False)["subject"].count()
    rec_type = rec_type.sort_values("subject", ascending=False)
    rec_type_fig = px.pie(rec_type, names = 'recall_type', values = 'subject', title="Share of Recall Types",
            color_discrete_sequence=px.colors.qualitative.Bold)
    rec_type_fig.update_traces(textposition='inside', textinfo='percent+label')
    rec_type_fig.update_layout(font=dict(size=18))
    rec_type_text = io.to_html(rec_type_fig, include_plotlyjs='cdn', full_html=False)

    return render(request, "home/dashboard.html", context={
                                                    'time_fig': time_fig_text,
                                                    'manu_fig': manu_fig_text,
                                                    'comp_fig': comp_fig_text,
                                                    'pie_fig': pie_fig_text,
                                                    'rec_type_fig':rec_type_text})


def recallsearch_1(request):
    makes = False
    models = False
    results = False
    url = "https://api.nhtsa.gov/products/vehicle/modelYears?issueType=r"
    r = requests.get(url)
    yearList = pd.read_json(r.text)
    yearList = yearList.results.apply(pd.Series)
    yearList = yearList[yearList.modelYear != '9999']
    return render(request, 'home/recallsearch.html', context={'yearList':yearList.squeeze(),
                                                        'makes':makes,
                                                        'models':models,
                                                        'results':results})

def recallsearch_2(request):
    try:
        if request.method == "GET":
            year = request.GET["yearSel"]
            makes = True
            models = False
            results = False
            url = "https://api.nhtsa.gov/products/vehicle/makes?modelYear=" + year + "&issueType=r"
            r = requests.get(url)
            makeList = pd.read_json(r.text)
            makeList = makeList.results.apply(pd.Series)
            makeList = makeList["make"]
            return render(request, 'home/recallsearch.html', context={'yearSel':year,
                                                            'makes':makes,
                                                            'models':models,
                                                            'makeList':makeList,
                                                            'results':results})
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

def recallsearch_3(request):
    try:
        if request.method == "GET":
            year = request.GET["yearSel"]
            make = request.GET["makeSel"]
            makes = True
            models = True
            results = False
            url = "https://api.nhtsa.gov/products/vehicle/models?modelYear=" + year + "&make=" + make + "&issueType=r"
            r = requests.get(url)
            modelList = pd.read_json(r.text)
            modelList = modelList.results.apply(pd.Series)
            modelList = modelList["model"]
            return render(request, 'home/recallsearch.html', context={'yearSel':year,
                                                            'makeSel':make,
                                                            'makes':makes,
                                                            'models':models,
                                                            'modelList':modelList,
                                                            'results':results})
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

def recallsearch_results(request):
    try:
        if request.method == "GET":
            year = request.GET["yearSel"]
            make = request.GET["makeSel"]
            model = request.GET["modelSel"]
            makes = True
            models = True
            results = True
            url = "https://api.nhtsa.gov/recalls/recallsByVehicle?make=" + make + "&model=" + model + "&modelYear=" + year
            r = requests.get(url)
            recallList = pd.read_json(r.text)
            count = int(recallList.Count[0])
            recallList = recallList.results.to_dict()
            recallList = sorted(recallList.values(), key=lambda x:datetime.strptime(x["ReportReceivedDate"],'%d/%m/%Y'))
            empty = False
            if len(recallList) == 0:
                empty = True
            return render(request, 'home/recallsearch.html', context={'yearSel':year,
                                                            'makeSel':make,
                                                            'modelSel':model,
                                                            'count':count,
                                                            'makes':makes,
                                                            'models':models,
                                                            'recallList':recallList,
                                                            'results':results,
                                                            'empty':empty})
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

def ratingsearch_1(request):
    makes = False
    models = False
    trim = False
    results = False
    url = "https://api.nhtsa.gov/SafetyRatings"
    r = requests.get(url)
    yearList = pd.read_json(r.text)
    yearList = yearList.Results.apply(pd.Series).ModelYear
    return render(request, 'home/ratingsearch.html', context={'yearList':yearList,
                                                        'makes':makes,
                                                        'models':models,
                                                        'trim':trim,
                                                        'results':results})

def ratingsearch_2(request):
    try:
        if request.method == "GET":
            year = request.GET["yearSel"]
            makes = True
            models = False
            results = False
            trim = False
            url = "https://api.nhtsa.gov/SafetyRatings/modelyear/" + year
            r = requests.get(url)
            makeList = pd.read_json(r.text)
            makeList = makeList.Results.apply(pd.Series).Make
            return render(request, 'home/ratingsearch.html', context={'yearSel':year,
                                                            'makes':makes,
                                                            'models':models,
                                                            'trim':trim,
                                                            'makeList':makeList,
                                                            'results':results})
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

def ratingsearch_3(request):
    try:
        if request.method == "GET":
            year = request.GET["yearSel"]
            make = request.GET["makeSel"]
            makes = True
            models = True
            trim = False
            results = False
            url = "https://api.nhtsa.gov/SafetyRatings/modelyear/" + year + "/make/" + make
            r = requests.get(url)
            modelList = pd.read_json(r.text)
            modelList = modelList.Results.apply(pd.Series).Model
            return render(request, 'home/ratingsearch.html', context={'yearSel':year,
                                                            'makeSel':make,
                                                            'makes':makes,
                                                            'models':models,
                                                            'trim':trim,
                                                            'modelList':modelList,
                                                            'results':results})
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

def ratingsearch_4(request):
    try:
        if request.method == "GET":
            year = request.GET["yearSel"]
            make = request.GET["makeSel"]
            model = request.GET["modelSel"]
            makes = True
            models = True
            trim = True
            results = False
            url = "https://api.nhtsa.gov/SafetyRatings/modelyear/" + year + "/make/" + make + "/model/" + model
            r = requests.get(url)
            trimList = pd.read_json(r.text)
            trimList = trimList.Results
            return render(request, 'home/ratingsearch.html', context={'yearSel':year,
                                                            'makeSel':make,
                                                            'modelSel':model,
                                                            'makes':makes,
                                                            'models':models,
                                                            'trim':trim,
                                                            'trimList':trimList,
                                                            'results':results})
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

def ratingsearch_results(request):
    try:
        if request.method == "GET":
            year = request.GET["yearSel"]
            make = request.GET["makeSel"]
            model = request.GET["modelSel"]
            trimSel = request.GET["trimSel"]
            makes = True
            models = True
            trim = True
            results = True
            url = "https://api.nhtsa.gov/SafetyRatings/VehicleId/" + trimSel
            r = requests.get(url)
            ratingList = pd.read_json(r.text)
            ratingList = ratingList.Results[0]
            return render(request, 'home/ratingsearch.html', context={'yearSel':year,
                                                            'makeSel':make,
                                                            'modelSel':model,
                                                            'trimSel':trimSel,
                                                            'makes':makes,
                                                            'models':models,
                                                            'trim':trim,
                                                            'ratingList':ratingList,
                                                            'results':results})
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render({}, request))

def addcar(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form_instance = forms.CarForm(request.POST)
        if form_instance.is_valid():
            form_instance.save(request)
            return redirect(settings)
    else:
        return redirect("/")

def settings(request):
    user = request.user
    car_objects = models.CarModel.objects.filter(user=user)
    return render(request, 'home/settings.html', context={'cars':car_objects})