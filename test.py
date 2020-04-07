from itertools import count

from flask import Flask, render_template, jsonify, views, request

app = Flask(__name__)

@app.route('/htbin/counts')
def htbin_counts(request):
    # print(request.POST.dict().get('count'))
    num = request.POST.dict().get('count') or 'p001'
    print(num)
    jason = count.main(num)
    return jsonify(jason,safe=False)


@app.route('/htbin/counts')
def htbin_counts():
    return render_template('index2.html')

@app.route('/video/', methods=['GET', 'POST'])
def htbin_counts():
    if request.method == 'POST':
        jason=count.main(dict().get('count'))
        print(jason)
        src = "rtmp://server.blackant.org:1935/live/hello"
    if jason == 'p001':
        src = "rtmp://server.blackant.org:1935/live_2710/hello"
    if jason == 'p002':
        src = "rtmp://server.blackant.org:1935/live_2711/hello"
    if jason == 'p003':
        src = "rtmp://server.blackant.org:1935/live_2712/hello"
    return render_template( 'video.html', locals())

if __name__ == '__main__':
    app.run()
