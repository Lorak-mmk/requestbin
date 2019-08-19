import urllib
from flask import session, redirect, url_for, escape, request, render_template, make_response

from requestbin import app, db, config

def update_recent_bins(name):
    if 'recent' not in session:
        session['recent'] = []
    if name in session['recent']:
        session['recent'].remove(name)
    session['recent'].insert(0, name)
    if len(session['recent']) > 10:
        session['recent'] = session['recent'][:10]
    session.modified = True


def expand_recent_bins():
    if 'recent' not in session:
        session['recent'] = []
    recent = []
    for name in session['recent']:
        try:
            recent.append(db.lookup_bin(name))
        except KeyError:
            session['recent'].remove(name)
            session.modified = True
    return recent

@app.endpoint('views.home')
def home():
    return render_template('home.html', recent=expand_recent_bins())


@app.endpoint('views.bin')
def bin(name):
    if request.query_string == 'inspect':
        try:
            bin = db.lookup_bin(name)
        except KeyError:
            return "Not found\n", 404

        if bin.private and session.get(bin.name) != bin.secret_key:
            return "Private bin\n", 403

        update_recent_bins(name)
        return render_template('bin.html',
            responeText=bin.responseText,
            url=bin.url,
            bin=bin,
            base_url=request.scheme+'://'+request.host,
            max_requests=config.MAX_REQUESTS,
            bin_ttl=config.BIN_TTL // 3600,
            bin_max_size=config.MAX_RAW_SIZE // 1024)
    else:
        try:
            bin = db.lookup_bin_by_url(name)
        except KeyError:
            return "Not found\n", 404
        db.create_request(bin, request)
        resp = make_response(bin.responseText)
        return resp
