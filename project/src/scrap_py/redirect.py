@aiohttp_jinja2.template('login.html')
async def login(request):

    if request.method == 'POST':
        form = await request.post()
        error = validate_login(form)
        if error:
            return {'error': error}
        else:
            # login form is valid
            location = request.app.router['index'].url_for()
            raise web.HTTPFound(location=location)

    return {}

app.router.add_get('/', index, name='index')
app.router.add_get('/login', login, name='login')
app.router.add_post('/login', login, name='login')