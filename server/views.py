from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from server import models
from server import mqtt_server
from django.template.context_processors import csrf
# Create your views here.
import datetime
def hello(request):
    return HttpResponse('Hello,world')

#下面的代码是新增加的，这个函数主要是把查询的内容渲染到 index.html页面去
def index(request):
    print(request.GET.get('name'))
    blog_index = models.Article.objects.all().order_by('-id')
    device = models.Device.objects.get(deviceID='154266')
    context = {
        'blog_index':blog_index,
        'device':device,
    }
    return render(request, 'index.html',context)


def orm_create(deviceId,message):
    try:
        print(deviceId + str(message['a']))
        # device = models.Device.objects.get(deviceID=deviceId)
        # time_now = datetime.datetime.strptime(datetime.datetime.now(), "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
        # time_now = time.strftime('%Y-%m-%d %H:%M[:%S[.%f]][%Z]', time.localtime(time.time()))
        dic = {'device_id':deviceId,'power':message['a']}
        models.Device_Data.objects.create(**dic)
    except Exception as e:
        print(e)

def orm_get(request):
    deviceID = request.GET.get('deviceId')
    data = models.Device_Data.objects.filter(device_id=deviceID).order_by('-created_time')[:10]
    data = list(data.values())
    # 生成 csrf 数据，发送给前端
    x = csrf(request)
    csrf_token = x['csrf_token']
    data = {'status': 'true','list': data,'csrf_token':str(csrf_token)}
    response = JsonResponse(data,safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def biubiu(request):
    deviceId = request.POST.get('deviceId')
    mqtt_server.server_to_device_send(deviceId,'biubiu')
    data = {'status': 'true'}
    response = JsonResponse(data, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "Content-Type,X-Requested-With,X-CSRFToken"
    return response

mqtt_server.server_main()