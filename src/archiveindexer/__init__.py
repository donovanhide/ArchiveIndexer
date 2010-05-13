import os, glob, datetime,sys ,csv
from jarray import zeros, array
from optparse import OptionParser

from org.archive.io.warc import WARCReaderFactory
from org.apache.commons.httpclient import Header,HttpParser,StatusLine
from org.apache.commons.httpclient.util import EncodingUtil, DateUtil

def main():
    usage = "usage: %prog WARCFile"
    parser = OptionParser(usage)
    (options, args) = parser.parse_args(sys.argv)
    if len(args) != 1:
        parser.print_usage()
        sys.exit(0)
    process(args[0])

def process(warc):
    file = os.path.basename(warc)
    csvWriter = csv.writer(sys.stdout, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    reader = WARCReaderFactory.get(warc)
    for record in reader:
        header = record.getHeader()
        if header.getHeaderValue('WARC-Type') == 'response':
            statusBytes =  HttpParser.readRawLine(record)
            statusString = ''.join(chr(c) for c in statusBytes)
            if (statusString and StatusLine.startsWithHTTP(statusString)):
                statusLine = StatusLine(statusString)
                httpHeaders = HttpParser.parseHeaders(record).tolist()
                code = int(statusLine.getStatusCode())
                date = parseDate(getHeader(httpHeaders,'Date'))
                etag = getHeader(httpHeaders,'ETag')
                last_modified = parseDate(getHeader(httpHeaders,'Last-Modified'))
                content_length = header.getHeaderValue('Content-Length')
                offset = header.getHeaderValue('Content-Length')
                hash = header.getHeaderValue('WARC-Payload-Digest')
                content_type = getHeader(httpHeaders,'Content-Type')
                url = header.getUrl()
                csvWriter.writerow([file,url,date,code,etag,last_modified,content_type,content_length,offset,hash])

def getHeader(headers,key):
    values = [h for h in headers if h.getName() == key]
    if len(values)>0:
        return values[0].getValue()
    return None;

def parseDate(date):
    if date:
        return datetime.datetime.fromtimestamp(DateUtil.parseDate(date).getTime()//1000)
    return None
