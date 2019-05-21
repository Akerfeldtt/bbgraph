from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect,render_to_response
from django.contrib import messages
from django.core.cache import cache
from celery import task
from celery.result import AsyncResult
from celery.task.control import inspect
from .forms import ParamForm
from .tasks import plotgraph
from scipy import constants
import numpy as np
import io
import time
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import savefig,close

ID = []
PROGRESS = []
IMAGE = []

def redirect_root(request):


    return redirect('/grapher/')

def BBmodel(kt,R,z=0.0316):
    E = np.linspace(1e-3, 2, 1000)
    Y = []
    D10 = 13950
    #kt = 0.11703
    sig=constants.Stefan_Boltzmann
    T = kt*(1.16e7)
    L39 = ( R**2 *4*np.pi * (T**4) *sig )/1e32
    N = L39/( (D10*(1+z))**2)

    for i in range(len(E)):
        Y.append((N * (8.0525) * (E[i] ** 2) * (E[i] * (1 + z)) ** 2 )/ ((1 + z) * (kt ** 4) * (np.exp((E[i] * (1 + z)) / kt) - 1)))
    return E,Y,N


def FormPost(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ParamForm(request.POST)
        #import pdb
        #pdb.set_trace()
        # check whether it's valid:
        if form.is_valid():
            return HttpResponseRedirect('interactive_results/')
        else:
            print(form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ParamForm()
    return render(request, 'grapher/index.html', {'form': form})

def FormGet(request):
    form = ParamForm(request.POST)

    # check whether it's valid:
    if request.method == 'POST' and 'btnform1' in request.POST:
        if form.is_valid():

            Temperature = float(form.cleaned_data['temperature'])
            Radius = float(form.cleaned_data['radius'])
            Redshift = float(form.cleaned_data['redshift'])
            from decimal import Decimal
            Xaxis, Yaxis, N = BBmodel(Temperature, Radius,Redshift)
            Xaxis = Xaxis.tolist()
            Radius = '%.2E' % Decimal(str(Radius))
            return render(request, 'grapher/results.html',{'temp':Temperature,'rad':Radius, 'redshift':Redshift,'Xaxis':Xaxis, 'Yaxis':Yaxis})
    if request.method == 'POST' and 'btnform2' in request.POST:
        
        if form.is_valid():

            Temperature = float(form.cleaned_data['temperature'])
            Radius = float(form.cleaned_data['radius'])
            Redshift = float(form.cleaned_data['redshift'])
            from decimal import Decimal
            Xaxis, Yaxis, N = BBmodel(Temperature, Radius,Redshift)
            Xaxis = Xaxis.tolist()
            Radius = '%.2E' % Decimal(str(Radius))
            buf_getvalue = plotgraph.delay(Xaxis,Yaxis)
            FormGet.task_id = buf_getvalue.id
            task = AsyncResult(FormGet.task_id )
            ID.append(FormGet.task_id)
            progress = task.state
            PROGRESS.append(progress)

            #
            # )
            # import pdb
            # pdb.set_trace(

            #time.sleep(1)
            # if task.ready():
            #     getval = task.get()
            #     getval = getval.encode('utf-8')
            #     getval = base64.b64decode(getval)
            #     response = HttpResponse(getval, content_type='image/png')
            #     #response['Content-Length'] = str(len(response.content))
            #     return response

            """
            return render_to_response('grapher/check_completion.html', {})
            #getval=buf_getvalue.get()
            #getval=getval.encode('utf-8')
            #getval =base64.b64decode(getval)
            #response = HttpResponse(getval, content_type='image/png')
            #response['Content-Length'] = str(len(response.content))
            """

            return render(request, 'grapher/check_completion.html',{'form': form, 'tasky': progress,'ID' : ID})
    return render(request, 'grapher/completion_status.html', {'form': form})


def newView(request):
    form = ParamForm(request.POST)

    # check whether it's valid:
    if request.method == 'POST' and 'btnform3' in request.POST:
        for i in range(len(ID)):
            task_id = ID[i]
            task = AsyncResult(task_id)
            progress = task.state
            PROGRESS[i] = progress

        task_id = FormGet.task_id
        task = AsyncResult(FormGet.task_id)
        progress = task.state
        # time.sleep(1)

        if task.ready():
            getval = task.get()
            ID_ind=ID.index(task_id)
            PROGRESS[ID_ind]=task.state





            #getval = getval.encode('utf-8')
            #getval = base64.b64decode(getval)
            #response = HttpResponse(getval, content_type='image/png')
            #response['Content-Length'] = str(len(response.content))
            return render_to_response('grapher/status_complete.html', {'form': form,'image': getval,'progress':PROGRESS,'ID' : ID})
    return render(request, 'grapher/completion_status.html', {'form': form, 'progress': PROGRESS,'ID' : ID})

def imagedisplay(request):
    task_id = FormGet.task_id
    task = AsyncResult(FormGet.task_id)

    for i in range(len(ID)):
        task_id = ID[i]
        task = AsyncResult(task_id)
        progress = task.state
        PROGRESS[i] = progress
        getval = task.get()
        IMAGE.append(getval)
    if task.ready():
        # getval = task.get()
        # progress = task.state
        i = inspect()
        a=1
        return render_to_response('grapher/png_template.html', { 'image': IMAGE,'apple':a})
