import json
import operator

from flask import session, make_response, request, render_template
from requestbin import app, db

def _response(object, code=200):
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, json.dumps(object)), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        resp = make_response(json.dumps(object), code)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.endpoint('api.bins')
def bins():
    private = request.form.get('private') in ['true', 'on']
    bin = db.create_bin(private)
    if bin.private:
        session[bin.name] = bin.secret_key
    return _response(bin.to_dict())


@app.endpoint('api.bin')
def bin(name):
    try:
        bin = db.lookup_bin(name)
    except KeyError:
        return _response({'error': "Bin not found"}, 404)

    return _response(bin.to_dict())


@app.endpoint('api.requests')
def requests(bin):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Bin not found"}, 404)

    return _response([r.to_dict() for r in bin.requests])


@app.endpoint('api.request')
def request_(bin, name):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Bin not found"}, 404)

    for req in bin.requests:
        if req.id == name:
            return _response(req.to_dict())

    return _response({'error': "Request not found"}, 404)


@app.endpoint('api.stats')
def stats():
    stats = {
        'bin_count': db.count_bins(),
        'request_count': db.count_requests(),
        'avg_req_size_kb': db.avg_req_size(), }
    resp = make_response(json.dumps(stats), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.endpoint('api.config')
def config(bin):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'result': 1, 'error': "Bin not found"}, 404)

    db.set_response_text(bin, request.form.get('responseText', bin.responseText))
    db.set_bin_url(bin, request.form.get('url', bin.name))
    db.set_response_mime(bin, request.form.get('mimetype', bin.responseMIME))
    return _response({'result': 0}, 200)
