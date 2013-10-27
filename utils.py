import re
from subprocess import Popen, PIPE, STDOUT


def stream_response(url, depth, search):
    cmd = 'python ../python-web-crawler/crawl.py {} {} {}'.format(url, depth, search)
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)

    yield "<html><body>\n"
    while True:
        line = p.stdout.readline()

        m = re.findall(' at (.*)', line)
        if len(m) > 0:
            for href in m:
                yield '<div>Found {} at <a href="{}">{}</a></div>\n'.format(search, href, href)
        else:
            yield "<div>%s</div>\n" % line

        if not line: break
    yield "</body></html>\n"
