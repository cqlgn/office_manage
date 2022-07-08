from django.shortcuts import render, get_object_or_404
from .models import cmdb
import time
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
import requests
import json
today = time.strftime("%Y-%m-%d", time.localtime())

def home(request):
    objs = cmdb.objects.all()
    summary=3000
    use = 0
    for money in objs:
        use+=money.金额
    remain = summary-use
    for date in objs:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'home.html',context={
        'objs': objs,
        'summary':summary,
        'use':use,
        'remain':remain
    }
                  )

def office(request):
    objs = cmdb.objects.filter(小类别='日常办公')
    for date in objs:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'office.html',context={
        'objs': objs,
    }
                  )
def card(request):
    objs = cmdb.objects.filter(小类别='名片印制')
    for date in objs:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'card.html',context={
        'objs': objs,
    }
                  )

def benefit(request):
    objs = cmdb.objects.filter(小类别='员工福利')
    for date in objs:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'benefit.html',context={
        'objs': objs,
    }
                  )



