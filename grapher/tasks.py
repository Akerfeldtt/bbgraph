# Create your tasks here
from __future__ import absolute_import, unicode_literals
from bbgraph.celery import app
import io
#import django
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import savefig,close,get_current_fig_manager
from django.http import HttpResponseRedirect,HttpResponse
import PIL
import base64
import time
@app.task(soft_time_limits=5,time_limit=20)
def plotgraph(x, y):
    f = Figure()
    buf = io.BytesIO()
    ax = f.add_subplot(111)
    ax.plot(x, y, '-')
    ax.set_ylabel(r"$\mathrm{EF_{E}\,(erg\,cm^{-2}\,s^{-1})}$")
    ax.set_xlabel(r"$\mathrm{Energy\,(keV)}$")
    # Code that sets up figure goes here; in the question, that's ...
    canvas = FigureCanvas(f)
    canvas.print_png(buf)
    buf_getval=buf.getvalue()
    buf.close()
    graphic = base64.b64encode(buf_getval)
    graphic = graphic.decode('utf-8')
    time.sleep(1)
    return graphic



