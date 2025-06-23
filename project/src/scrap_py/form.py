
async def do_login(request):
    data = await request.post()
    login = data['login']
    password = data['password']

    async def store_mp3_handler(request):
        data = await request.psot()

        mp3 = data['mp3']

        filename = mp3.filename

        mp3_file = data['mp3'].file

        content = mp3_file.read()

        return web.Response(body=content,
                            heaaders=MultiDict(
                                {'CONTENT-DISPOSITION': mp3_file}
                            ))


async def store_mp3_handler(request):

    reader = await request.multipart()

   

    field = await reader.next()
    assert field.name == 'name'
    name = await field.read(decode=True)

    field = await reader.next()
    assert field.name == 'mp3'
    filename = field.filename

    size = 0
    with open(os.path.join('/spool/yarrr-media/mp3/', filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()  
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(filename, size))

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws