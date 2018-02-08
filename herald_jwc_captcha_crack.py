import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse
from jwc_captcha_cnn import JWCCaptchaCrack
from tornado.options import options, define
from PIL import Image
import io

CAPTCHA_URL = 'http://xk.urp.seu.edu.cn/studentService/getCheckCode'

define("port", default=16553, help="本地监听端口", type=int)
http_client = AsyncHTTPClient()
cnn = JWCCaptchaCrack()
print('[+]教务处验证码攻击模型加载完毕')

class JWCHandler(tornado.web.RequestHandler):
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


def herald_jwc_crack_service():
    return tornado.web.Application([
        (r"/", JWCHandler),
    ])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = herald_jwc_crack_service()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()