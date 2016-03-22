# -*- coding: utf-8 -*
from flask import render_template, session, redirect, url_for, current_app, request
from . import main
from flask.ext.login import login_required, current_user


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/show_py', methods=['GET', 'POST'])
def show_py():
    filen = request.args.get("filen").strip()
    with open(filen) as f:
        contents = f.readlines()
    return render_template("main/show_py.html", contents = contents)
    
@main.route('/search', methods=['GET', 'POST'])
def search():
    page = request.args.get('page', 1, type=int)

    if request.method == 'POST' or page:
         keyword = request.args.get('keyword') if request.args.get('keyword') else request.form['search'] 
         print keyword, request.args.get('keyword')
         if keyword :
                filelists = search_aux(keyword)
                pagenum, remain = divmod(len(filelists), current_app.config['PAGINATION_NUM'])
                pagenum += 1 if remain else 0
                filelist = filelists[(page-1)*current_app.config['PAGINATION_NUM']:\
                                     page*current_app.config['PAGINATION_NUM']]
                return render_template("main/search.html", pagenum=pagenum,
                                       page=page, filelist=filelist, keyword=keyword)

    return redirect(url_for('main.index'))


def search_aux(keyword):
    filelists = []
    import subprocess
    for dirname in current_app.config['SITE_PY']:
        proc =  subprocess.Popen(["grep", "-R", "-l","--include=*.py",
                                  keyword, dirname], stdout=subprocess.PIPE)
        filelist = [ filen for filen in proc.stdout ]
        filelists.extend(filelist)
        proc.stdout.close()
        try:
            proc.kill()
        except OSError:
           # can't kill a dead proc
            pass
        
    return filelists
