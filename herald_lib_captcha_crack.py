import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse
from library_captcha_cnn import LibraryCaptchaCrack
from tornado.options import options, define
from PIL import Image
import io

CAPTCHA_URL = 'http://www.libopac.seu.edu.cn:8080/reader/captcha.php'

define("port", default=16554, help="本地监听端口", type=int)
http_client = AsyncHTTPClient()
cnn = LibraryCaptchaCrack()
print('[+]教务处验证码攻击模型加载完毕')

class LibHandler(tornado.web.RequestHandler):
    async def get(self):
        cookies = self.get_argument('cookie', None)
        if cookies is not None:
            request = HTTPRequest(url=CAPTCHA_URL, headers={'cookie': cookies})
        else:
            request = HTTPRequest(url=CAPTCHA_URL)
        response = await http_client.fetch(request)
        if 'Set-Cookie' in response.headers:
            cookies = response.headers['Set-Cookie']
            cookies = cookies.split(';')[0]
        img = Image.open(io.BytesIO(response.body))
        result = cnn.predict(img)
        self.write({'cookies': cookies, 'captcha': result})


def herald_lib_crack_service():
    return tornado.web.Application([
        (r"/", LibHandler),
    ])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = herald_lib_crack_service()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()