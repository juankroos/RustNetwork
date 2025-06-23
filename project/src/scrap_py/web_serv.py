from aiohttp import web

routes = web.RouteTableDef()
@routes.get('/')
async def hello(request):
    data = {'hello':
            'data''hello'},{'blabla' :'yo'}
    return web.json_response(data)

@routes.post('/post')
async def post_handler(request):
    pass

@routes.put('/put')
async def put_handler(request):
    pass


class Handler:
    def __init__(self):
        pass

    @routes.get('/')
    async def handle_main_page(self,request):
        return web.Response(text="blabla la premiere page")
    @routes.get('/greeting')
    async def handle_greeting(self, request):
        name = request.match_info.get('name', "anonymous")
        text = "hello, {}".format(name)
        return web.Response(text=txt)
    
handler = Handler()


app = web.Application()
app.add_routes(routes)

web.run_app(app)
