import sqlite3 as sql
from flask import Flask, render_template, request, redirect,url_for

print(sql.sqlite_version)
def edit_1():
    con = sql.connect('game')
    cur = con.cursor()
    if request.remote_addr not in cur.execute('''SELECT * FROM users''').fetchall():
        try:
            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (request.remote_addr,request.remote_addr,0, 'house',))
        except sql.IntegrityError:
            pass

    a = cur.execute('''SELECT * from users WHERE ip = ?''', (str(request.remote_addr), )).fetchall()[0]
    con.commit()
    return(a)


def edit():
    con = sql.connect('game.db')
    cur = con.cursor()
    edit, back = request.form.get('edit'), request.form.get('back')
    if back is not None:
        con.commit()
        con.close()
        return redirect("/")
    else:
        name = request.form.get('name')
        cur.execute('''UPDATE users
                       SET name = ?
                       WHERE ip = ?''', (name, request.remote_addr))
        con.commit()
        con.close()
        return redirect('/edit')


def understand():
        result = dict()
        con = sql.connect('game.db')
        cur = con.cursor()
        ips_ = cur.execute("""SELECT ip FROM users1""").fetchall()
        ips = []
        [ips.append(x[0]) for x in ips_]
        print(ips)
        if request.remote_addr in ips:
            scene = cur.execute('''SELECT scene FROM users1 WHERE ip = ?''', (request.remote_addr,)).fetchone()[0]
            print(scene)
        else:
            scene = 'begin'
            cur.execute("""INSERT INTO users1 (IP, name, inv, hp, DMG, scene, armor, COIN) VALUES(?, '', '', ?, ?, ?, 100, 100)""", (request.remote_addr, 0, 0,'begin',))
            con.commit()
        print('link -->', scene)
        html = cur.execute('''SELECT html FROM scene1 WHERE name = ?''', (scene,)).fetchone()[0]
        print('html -->', html)
        paths = cur.execute("""SELECT paths FROM scene1 WHERE name=?""", (scene,)).fetchall()[0]
        # taking images

        img = 'pictures/' + cur.execute("""SELECT img FROM scene1 WHERE name=?""", (scene,)).fetchone()[0]
        print(img)
        text = cur.execute("""SELECT text FROM scene1 WHERE name=?""", (scene,)).fetchone()[0]
        img_link = "{{ url_for('static', filename='pictures/" + str(img[0]) + "') }}"
        lst = paths[0].split(",")
        leng = len(lst)
        result['html'] = html
        result['paths'] = lst
        result['leng'] = leng
        result['scene'] = scene
        result['img'] = img
        result['text'] = text
        print('GGGG', result)
        con.commit()
        return (result)


def new_understand(req):
    result = dict()
    con = sql.connect('game.db')
    cur = con.cursor()
    ips_ = cur.execute("""SELECT ip FROM users1""").fetchall()
    ips = []
    [ips.append(x[0]) for x in ips_]
    if req in ips:
        scene = cur.execute('''SELECT scene FROM users1 WHERE ip = ?''', (req,)).fetchone()[0]
    else:
        scene = 'begin'
        cur.execute(
            """INSERT INTO users1 (IP, name, inv, hp, DMG, scene, armor, COIN) VALUES(?, '', '', ?, ?, ?, 100, 100)""",
            (req, 0, 0, 'begin',))
        con.commit()
    html = cur.execute('''SELECT html FROM scene1 WHERE name = ?''', (scene,)).fetchone()[0]
    paths = cur.execute("""SELECT paths FROM scene1 WHERE name=?""", (scene,)).fetchall()[0]
    # taking images

    img = 'pictures/' + cur.execute("""SELECT img FROM scene1 WHERE name=?""", (scene,)).fetchone()[0]
    text = cur.execute("""SELECT text FROM scene1 WHERE name=?""", (scene,)).fetchone()[0]
    biom = cur.execute("""SELECT biom FROM scene1 WHERE name=?""", (scene,)).fetchone()[0]
    img_link = "{{ url_for('static', filename='pictures/" + str(img[0]) + "') }}"
    lst = paths[0].split(",")

    a = []
    [a.append(eval(x[0])) for x in cur.execute("""SELECT mobs FROM scene1 WHERE name=?""", (scene,)).fetchall()]
    av_mobs = cur.execute('''SELECT mobs FROM bioms WHERE name = ? ''', (biom,)).fetchall()[0][0].split(';')
    a = a[0]
    new_a = a.copy()
    drop_lst = {}
    for key, value in new_a.items():
        if key not in av_mobs:
            del a[key]
            mob_drop = cur.execute('''SELECT stuff FROM mobs WHERE name = ?''', (key,)).fetchall()
            for i in range(len(mob_drop)):
                final_lst = mob_drop[i][0].split(';')
                for j in range(len(final_lst)):
                    new_lst = final_lst[j].split('*')
                    n = 1
                    el = final_lst[j]
                    if len(new_lst) != 1:
                        n = int(new_lst[1]) # ya poshel ssat`
                        el = new_lst[0]
                    try:
                        drop_lst[el] += n * int(value)
                    except KeyError:
                        drop_lst[el] = 0
                        drop_lst[el] += n * int(value)

    result['html'] = html
    result['paths'] = lst
    result['scene'] = scene
    result['img'] = img
    result['text'] = text
    result['biom'] = biom
    result['mobs'] = a
    result['drop'] = drop_lst
    con.commit()
    return (result)

print("nowshit",new_understand('127.0.0.1'))