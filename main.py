import sqlite3
import io
from bottle import Bottle, run, redirect, response
from PIL import Image


app = Bottle()
conn = sqlite3.connect('data.db')
img_list = []
for i in range(10):
    img = Image.open(f'./assets/shuzi{i}.png')
    img = img.resize((50, 50))
    img_list.append(img)


@app.route('/')
def index():
    return redirect('https://github.com/ten1fs/count', 301)


@app.route('/hello')
def hello():
    return 'Hello,World!'


@app.route('/get/<key>')
def count(key):
    if key is None:
        return 'key不能为空'
    c = conn.cursor()
    c.execute('select count(*) from count where k = ?', (key, ))
    result = c.fetchall()
    if result[0][0] == 0:
        c.execute('insert into count(k, v) values(?,?)', (key, 1))
    else:
        c.execute('select v from count where k = ?', (key, ))
        result = c.fetchall()
        v = int(result[0][0])
        v += 1
        c.execute('update count set v = ? where k = ?', (v, key))
    conn.commit()
    c.execute('select v from count where k = ?', (key, ))
    result = c.fetchall()
    v = int(result[0][0])
    num_str = str(v).zfill(10)
    target_img = Image.new('RGBA', (500, 60))
    for (j, item) in enumerate(num_str):
        idx = int(item)
        target_img.paste(img_list[idx], (j * 50, 5))
    buffer = io.BytesIO()
    target_img.save(buffer, 'PNG')
    data = buffer.getvalue()
    buffer.close()
    response.set_header('Content-Type', 'image/png')
    return data


run(app, host='localhost', port=8080)