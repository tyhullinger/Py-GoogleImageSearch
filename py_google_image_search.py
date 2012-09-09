import urllib2
import simplejson

GOOGLE_IMAGE_SEARCH_URL = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0'

class GoogleImage(object):
    def __init__(self, width, height, title, titleNoFormatting, url, unescapedUrl):
        self.width = width
        self.height = height
        self.title = title
        self.titleNoFormatting = titleNoFormatting
        self.url = url
        self.unescapedUrl = unescapedUrl

class GoogleImageSearch(object):
    
    def __init__(self):
        self.search = {}

    def referer(self, value):
        self.referer = value

    def search_term(self, value):
        self.add_param('q', value)

    def add_param(self, key, value):
        if not key in self.search:
            self.search[key] = value
        else:
            self.search.update({key: value})

    def list_params(self):
        if len(self.search) > 0:
            for key, value in self.search.iteritems():
                print '{0} : {1}'.format(key, str(value))
        else:
            print 'No values have been set'

    def query(self):
        request = urllib2.Request(
            self.__build_url(), None, {'Referer': self.referer}
        )
        return self.__objectify_results(
                simplejson.load(
                    urllib2.urlopen(request)
                )
            )

    def __build_url(self):
        temp = ''
        for key, value in self.search.iteritems():
            temp = temp + '&{0}={1}'.format(key, str(value))
        return (GOOGLE_IMAGE_SEARCH_URL + temp)

    def __objectify_results(self, values):
        results = []
        if values['responseStatus'] == 200:
            for value in values['responseData']['results']:
                results.append(GoogleImage(
                    value['width'],
                    value['height'],
                    value['title'],
                    value['titleNoFormatting'],
                    value['url'],
                    value['unescapedUrl']
                    )
                )
        return results


def store_image(url):
    try:
        u = urllib2.urlopen(url)
    except IOError:
        print '{0} - can not be read'.format(url)
    else:
        tmp = url.split('/')
        file_name = tmp[len(tmp) - 1]
        local_file = open(file_name, 'wb')
        local_file.write(u.read())
        local_file.close()

'''
g = GoogleImageSearch()
g.referer('tyhullinger.com')
g.search_term('9780764569593')
g.list_params()
results = g.query()

x = 1
for result in results:
    print '-------------------------------------------------------'
    print 'Result {0}'.format(x)
    print '-------------------------------------------------------'
    print 'Title: {0}'.format(result.title)
    print 'Unformatted Title: {0}'.format(result.titleNoFormatting)
    print 'Dimensions: {0}x{1}'.format(result.width, result.height)
    print 'Url: {0}'.format(result.url)
    print 'Unescaped Url: {0}'.format(result.unescapedUrl)
    x = x + 1

print
store = input('Enter the result number of the image you want to keep (0 for none): ')

if not store == 0:
    print 'Storing...'
    store_image(results[store - 1].unescapedUrl)
'''
