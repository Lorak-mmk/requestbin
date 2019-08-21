import time
import operator

from ..models import Bin

from requestbin import config

class MemoryStorage():
    cleanup_interval = config.CLEANUP_INTERVAL

    def __init__(self, bin_ttl):
        self.bin_ttl = bin_ttl
        self.bins = {}
        self.urls = {}
        self.request_count = 0

    def do_start(self):
        self.spawn(self._cleanup_loop)

    def _cleanup_loop(self):
        while True:
            self.async.sleep(self.cleanup_interval)
            self._expire_bins()

    def _expire_bins(self):
        expiry = time.time() - self.bin_ttl
        for name, bin in self.bins.items():
            if bin.created < expiry:
                self.bins.pop(name)

    def create_bin(self, private=False):
        bin = Bin(private)
        self.bins[bin.name] = bin
        self.urls[config.URL_DB_PREFIX + bin.url] = bin.name
        return self.bins[bin.name]

    def create_request(self, bin, request):
        bin.add(request)
        self.request_count += 1

    def set_response_text(self, bin, respTxt):
        bin.responseText = respTxt
    
    def set_response_mime(self, bin, mime):
        bin.responseMIME = mime

    def set_bin_url(self, bin, url):
        del self.urls[config.URL_DB_PREFIX + bin.url] # This might be expected behaviour
        bin.url = url
        self.urls[config.URL_DB_PREFIX + url] = bin.name

    def count_bins(self):
        return len(self.bins)

    def count_requests(self):
        return self.request_count

    def avg_req_size(self):
        return None

    def lookup_bin(self, name):
        return self.bins[name]

    def lookup_bin_by_url(self, url):
        url = config.URL_DB_PREFIX + url
        binKey = self.urls[url]
        return self.bins[binKey]
