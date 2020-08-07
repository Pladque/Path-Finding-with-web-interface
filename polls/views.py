from django.shortcuts import render
from . import pathFinding as pf
import time
from . import functions as f

NUMER_OF_TILES = 2992

# Create your views here.

def home(request):  #clear board
    tiles_number = range(0,2992)
    tiles_and_path = []

    for i in tiles_number:
        tiles_and_path.append((False, i, False, False,False))

    return  render(request,"base.html",{'tiles_and_path':tiles_and_path,'tiles_number': tiles_number})

def findPath(request):
    tiles_number = range(0, NUMER_OF_TILES)

    # Reading input:
    if request.POST.get('walls'):
        walls = request.POST.get('walls')
    else:
        walls = ";-1"

    if request.POST.get('start'):
        start = request.POST.get('start')
    else:
        start = -1
    if request.POST.get('finish'):
        finish = request.POST.get('finish')
    else:
        finish = -1
    if request.POST.get('accuracy'):
        accuracy = int(request.POST.get('accuracy')) / 1000
    else:
        accuracy = 0.999
    #######################
    ######## finding path #######
    timer_start = time.time()
    path, history = pf.findPath(start, finish, walls, accuracy)
    timer_finish =time.time()

    time_to_find_path = round(timer_finish - timer_start,2)

    path = list(dict.fromkeys(path))
    history = list(dict.fromkeys(history))

    ##########################

    tiles_and_path = []     # table with tuples(if_path, id, if_start, id_finish, if_wall, if_checked_history)

    # converting path, walls, start and endpoint to tuples, to make it readable for frontend
    if type(walls) == str:
        walls_table = walls.split(';')
        walls_table.remove('')  # bo 0. element jets null
        walls_table = list(dict.fromkeys(walls_table))
    else:
        walls_table = []

    for i in tiles_number:
        if_done = False
        if i == int(start):
            if_done = True
            tiles_and_path.append((False, i, True, False, False, False))
            pass
        elif i == int(finish):
            if_done = True
            tiles_and_path.append((False, i, False, True, False, False))
            pass
        else:
            for wall in walls_table:
                if int(wall) == i:
                    tiles_and_path.append((False, i, False, False, True, False))
                    if_done = True
            if if_done is False:
                for p in path:
                    if p == i:
                        tiles_and_path.append((True, i, False, False, False, False))
                        if_done = True
            if if_done is False:
                for h in history:
                    if h == i:
                        tiles_and_path.append((False, i, False, False, False, True))
                        if_done = True
        if if_done is False:
            tiles_and_path.append((False, i, False, False, False))
    ################################################################################

    message = ""
    if len(path) == 0 and start != -1:
        message = "PATH NOT FOUND "

    print(accuracy)

    return render(request, "base.html", {'tiles_and_path': tiles_and_path, 'time': time_to_find_path, 'start_id': start, 'finish_id': finish, 'walls_ids': walls, 'msg': message, 'accuracy':accuracy*1000})   #tu dodaj zeby wysylalo zapisane wczesniej sciany itp