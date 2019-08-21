import feedparser
import time
import re
from requestbin import config

bin_ttl = config.BIN_TTL
storage_backend = config.STORAGE_BACKEND

storage_module, storage_class = storage_backend.rsplit('.', 1)

try:
    klass = getattr(__import__(storage_module, fromlist=[storage_class]), storage_class)
except ImportError, e:
    raise ImportError("Unable to load storage backend '{}': {}".format(storage_backend, e))

db = klass(bin_ttl)

def create_bin(private=False):
    return db.create_bin(private)

def create_request(bin, request):
    return db.create_request(bin, request)

def set_response_text(bin, respTxt):
    return db.set_response_text(bin, respTxt)

def set_response_mime(bin, mime):
    return db.set_response_mime(bin, mime)

def set_bin_url(bin, url):
    return db.set_bin_url(bin, url)

def lookup_bin(name):
    name=re.split(r"[/.]", name)[0]
    return db.lookup_bin(name)

def lookup_bin_by_url(url):
    return db.lookup_bin_by_url(url)

def count_bins():
    return db.count_bins()

def count_requests():
    return db.count_requests()

def avg_req_size():
    return db.avg_req_size()
