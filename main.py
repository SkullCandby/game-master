import sqlite3 as sql
from flask import Flask, render_template, request, redirect, url_for
from defs import understand
import os

# добавить в бд картинки
app = Flask(__name__, template_folder="templates")
app.config["IMAGE_UPLOADS"] = "C:/Users/dvmes/PycharmProjects/game-master/static/pictures/"

global name, amount
name = "/"
amount = 2
global scene_name, scene_entity, scene_paths
scene_entity = {}
scene_name = ''
# biom_list - это хуета где лежит список возможных биомов .. текст это описание .. сцена_биом это биом который выбрали
global biom_list, scene_text, scene_biom
scene_text = ''
biom_list = ["Govno", "Zhopa"]
scene_paths = ''


@app.route(name)
def start():
    about = understand()
    print(about)
    return render_template('start.html', text=about['text'], image_filename=about['img'], lst=about['paths'], name=about['scene'])


@app.route(name, methods=["POST"])
def start_post():
    con = sql.connect('game.db')
    cur = con.cursor()
    res = request.form.get('name')
    av_scenes_ = cur.execute("""SELECT name FROM scene1""").fetchall()
    av_scenes = []
    [av_scenes.append(x[0]) for x in av_scenes_]
    print(av_scenes, '////1224414', res)
    if res != 'Edit' and res in av_scenes:
        cur.execute('''UPDATE users1
                               SET scene = ?
                               WHERE ip = ?''', (res, request.remote_addr))

        con.commit()
        return redirect('/')
    return redirect('/edit')


@app.route("/edit")
def authour():
    entity_list = []
    biom_list = []
    con = sql.connect('game.db')
    cur = con.cursor()
    print(cur.execute('''SELECT mobs FROM bioms''').fetchall(), cur.execute('''SELECT mobs FROM bioms''').fetchone())
    bebra = cur.execute('''SELECT name FROM bioms''').fetchall()
    [biom_list.append(x[0]) for x in bebra]
    a = []
    [a.append(x[0].split(';')) for x in cur.execute('''SELECT mobs FROM bioms''').fetchall()]
    print(a)
    new = set()
    for elem in a:
        for elem_ in elem:
            new.add(elem_)
    entity_list = list(new)
    print(entity_list)
    return render_template('edit.html', entity_list=entity_list, scene_name=scene_name, entity=scene_entity,
                           biom_list=biom_list, scene_text=scene_text, scene_paths=scene_paths)


@app.route("/edit", methods=["POST"])
def editor():
    global scene_name, scene_paths, scene_entity
    global amount, scene_text, scene_biom
    print('YA YEBAL MAt` vkada', request.form.get('Send'))
    if request.form.get('add') is not None:
        amount += 1
        scene_name = request.form.get('scene_name')
        scene_entity[request.form.get('select_entity')] = request.form.get('select_amount')
        scene_text = request.form.get('scene_text')
        scene_paths = request.form.get('scene_paths')
        print("ENTITY--", scene_entity)
        return redirect('/edit')
    elif request.form.get('Send') is not None:

        scene_img = ''
        scene_html = ""
        scene_html = scene_name + ".html"
        con = sql.connect('game.db')
        cur = con.cursor()
        print(scene_name, cur.execute('''SELECT name FROM scene''').fetchone(), '////')
        scene_names = []
        [scene_names.append(x[0]) for x in cur.execute('''SELECT name FROM scene1''').fetchall()]
        print(scene_names)
        # получаем всю хуйню
        scene_name = request.form.get('scene_name')
        scene_text = request.form.get('scene_text')
        scene_paths = request.form.get('scene_paths')
        scene_biom = request.form.get('select_biom')
        # добавить проверку в андерстенд есть ли в биоме (по хуйне)
        scene_entity[request.form.get('select_entity')] = request.form.get('select_amount')
        print("Вся хуйня", scene_biom, scene_text, scene_name, scene_paths, scene_entity)

        try:
            cur.execute("INSERT INTO scene1 VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (scene_name, scene_biom, str(scene_entity), scene_paths, 'start.html', scene_text,
                         scene_img))
        except sql.IntegrityError:
            print('HDWHDOUWAHOUWHDWADJLWADBNLWJDNWLJNDLAJNLAWNDDNLAWDNWLNADLJND')
            cur.execute('''UPDATE scene1
                                   SET paths = ?, img = ?, html = ?, biom = ?, mobs = ?, text = ?
                                   
                                   WHERE name = ?''',
                        (scene_paths, scene_img, 'start.html', scene_biom, str(scene_entity), scene_text, scene_name,))
        con.commit()
        return redirect('/')
    # ^___^ nyaaa ya anime psih mne pohui ^ ____ ^


if __name__ == "__main__":
    app.run()
