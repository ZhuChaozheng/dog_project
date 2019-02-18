from django.shortcuts import render
from django.http import JsonResponse
from .htbin import count
# Create your views here.


def counts(request):
    # print(request.POST.dict().get('count'))
    num = request.POST.dict().get('count') or 'p001'
    print(num)
    jason = count.main(num)
    return JsonResponse(jason, safe=False)


def index(request):
    return render(request, 'index2.html')


def video(request):
    jason = count.main(request.POST.dict().get('count'))
    print(jason)
    src = "rtmp://server.blackant.org:1935/live/hello"
    if jason == 'p001':
        src = "rtmp://server.blackant.org:1935/live_2710/hello"
    if jason == 'p002':
        src = "rtmp://server.blackant.org:1935/live_2711/hello"
    if jason == 'p003':
        src = "rtmp://server.blackant.org:1935/live_2712/hello"
    return render(request, 'video.html', locals())
