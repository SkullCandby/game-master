import sqlite3 as sql
from flask import Flask, render_template, request, redirect, url_for
from defs import understand
import os

app = Flask(__name__, template_folder="templates")
app.config["IMAGE_UPLOADS"] = "C:/Users/dvmes/PycharmProjects/game-master/static/pictures/"

global name
name = "/"


@app.route(name)
def start():
    about = understand()
    print(about['html'])
    return render_template('start.html', text=about['text'], image_filename=about['img'], lst=about['paths'], name=about['scene'])


@app.route(name, methods=["POST"])
def start_post():
    res = request.form.get('name')
    if res != 'Edit':
        con = sql.connect('game.db')
        cur = con.cursor()
        cur.execute('''UPDATE users
                               SET scene = ?
                               WHERE ip = ?''', (res, request.remote_addr))

        con.commit()
        return redirect('/')
    return redirect('/edit')


@app.route("/edit")
def authour():
    return render_template('edit.html')


@app.route("/edit", methods=["POST"])
def editor():
    scene_name = "/" + request.form.get('scene_name')
    scene_paths = request.form.get('scene_paths')
    scene_text = request.form.get('scene_text')
    scene_img = ''
    if request.files:
        scene_img = request.files['scene_img']

        scene_img.save(os.path.join(app.config["IMAGE_UPLOADS"], scene_img.filename))


    scene_html = ""
    scene_html = scene_name + ".html"
    print(scene_name, scene_paths, scene_img.filename, type(scene_img), 'DWADADAWDWADAWD')
    con = sql.connect('game.db')
    cur = con.cursor()
    print(scene_name, cur.execute('''SELECT name FROM scene''').fetchone(), '////')
    if scene_name not in cur.execute('''SELECT * FROM scene''').fetchall():
        try:
            cur.execute("INSERT INTO scene VALUES (?, ?, ?, ?, ?)",
                        (scene_name, scene_paths, scene_img.filename, scene_text, 'start.html'))
        except sql.IntegrityError:
            cur.execute('''UPDATE scene
                                   SET paths = ?, img = ?, lvl = ?, html = ?
                                   
                                   WHERE name = ?''', (scene_paths, scene_img.filename, scene_text, 'copy_file.html', scene_name,))
    con.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run()
