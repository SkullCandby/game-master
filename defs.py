import sqlite3 as sql
from flask import Flask, render_template, request, redirect,url_for


def edit_1():
    con = sql.connect('game.db')
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

        con.commit()
        return (result)