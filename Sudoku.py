import time, pyautogui, threading, os, random, sys, string
from tkinter import *
from win32 import win32api, win32gui
import PIL.ImageTk as ImageTk
from PIL import Image
from datetime import datetime

def destroy(event):
    root.destroy()

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)

root = Tk()
root.geometry("600x600+%d+%d" % ((width/2)-300, (height/2)-300))
root.overrideredirect(1)
root.bind("<Escape>", destroy)
main = Frame(root, bg="blue")

class Tile:
    def __init__(self, location, number, x, y):
        self.number = number
        self.x = x
        self.y = y
        self.label = Label(location, text=number, bg="white", fg="black", width=5, height=2)
        self.label.grid(row=x, column=y, pady=(10,10), padx=(13,6))
        self.label.bind("<Enter>", self.highlight)
        self.label.bind("<Leave>", self.unhighlight)
        self.label.bind("<Button-1>", self.text_update)
    def highlight(self, event):
        self.label.config(bg="orange")
    def unhighlight(self, event):
        self.label.config(bg="white")
    def text_update(self, event):
        pass
    def destroy(self):
        self.label.destroy()

def position_converter(position, value):
    positions = {}
    squares = {}
    row = 0
    column = 0
    small_square = 0
    for x in range(0,81):
        positions[x] = (row, column)
        squares[x] = small_square
        column += 1
        if column == 3:
            small_square += 1
        elif column == 6:
            small_square += 1
        elif column == 9:
            row += 1
            column = 0
            if row < 3:
                small_square = 0
            elif row < 6:
                small_square = 3
            elif row < 9:
                small_square = 6
    for y in range(0,81):
        if positions[y] == position:
            if value:
                return squares[y]
            else:
                return y

def check_small_squares(slot, num):
    global small_squares
    for s in small_squares[slot]:
        if s == num:
            return False
    return True

def generate_nums():
    global all_nums, small_squares, root, progress, progress_l, main
    poss = string.digits.replace("0", "")
    small_squares = [[],[],[],[],[],[],[],[],[]]
    rows = [[],[],[],[],[],[],[],[],[]]
    columns = [[],[],[],[],[],[],[],[],[]]
    stuck = (0,0)
    row = 0
    column = 0
    repeat = True
    position = (row, column)
    highest = (row, column)
    backtrack = [[0,0], 0] #[[row,column],count]
    progress = Toplevel()
    progress_l = Label(progress, text="0")
    progress_l.pack(pady=(25,0))
    #progress.geometry("100x100+%d+%d" % ((width/2)-50, (height/2)-50))
    progress.geometry("100x100+3000+3000")
    progress.overrideredirect(1)
    progress.attributes("-topmost", True)
    while repeat:
        root.update()
        root.update_idletasks()
        new = True
        while new:
            #print(position)
            if len(poss) == 0:
                poss = string.digits.replace("0", "")
                #print(backtrack[0])
                #print(row, column)
                if backtrack[0] != [row,column]:
                    #print("<<%s" %(backtrack[1]))
                    backtrack = [[row,column],1]
                    #print("fail at (%s,%s)" %(row,column))
                else:
                    backtrack[1] += 1
                for x in range(0,backtrack[1]):
                    column -= 1
                    if column == -1:
                        row -= 1
                        column = 8
                    if row < 0:
                        row = 0
                        column = 0
                    position = (row, column)
                    try:
                        rows[row].pop()
                        columns[column].pop()
                        small_squares[position_converter(position, True)].pop()
                    except:
                        pass
            if stuck[0] == row:
                stuck = (row, stuck[1] + 1)
                if stuck[1] == 1000:
                    #print(stuck)
                    #print(poss)
                    small_squares = [[],[],[],[],[],[],[],[],[]]
                    rows = [[],[],[],[],[],[],[],[],[]]
                    columns = [[],[],[],[],[],[],[],[],[]]
                    stuck = (0,0)
                    row = 0
                    column = 0
                    position = (row, column)
                    highest_poss = (0,0)
            else:
                stuck = (row, 0)
            num = poss[random.randint(0,len(poss)-1)]
            poss = poss.replace(num, "")
            for r in range(0,9):
                if position[0] == r:
                    if num not in rows[r]:
                        for c in range(0,9):
                            if position[1] == c:
                                if num not in columns[c]:
                                    if check_small_squares(position_converter(position, True), num):
                                        small_squares[position_converter(position, True)].append(num)
                                        rows[position[0]].append(num)
                                        columns[position[1]].append(num)
                                        all_nums = rows
                                        progress_l.configure(text=str((position_converter(position, False) / 80)*100) + "%\nOn Square: " + str(position_converter(position, False)))
                                        new = False
                                    else:
                                        new = True
                                else:
                                    new = True
                    else:
                        new = True
        column += 1
        if column == 9:
            row += 1
            column = 0
        position = (row, column)
        if position == (9,0):
            repeat = False

def board():
    global all_nums, main, progress, tiles
    generate_nums()
    progress.destroy()
    tiles = []
    for row in range(0,9):
        for column in range(0,9):
            tile = Tile(main, all_nums[row][column], row, column)
            tiles.append(tile)
    main.pack(fill="both", expand=True)

completions = 0
times = 0
tt = 0
start_time = time.time()
while True:
    t1 = time.time()
    board()
    completions += 1
    times += (time.time()-t1)
    tt += times
    print("Completed: " + str(completions) + "\nAverage Time: " + str((times/completions)) + "\nThis Time: " + str(time.time()-t1) + "\nElapsed Time: " + str(time.time() - start_time) + "\n##########################")
    for x in tiles:
        x.destroy()
    if completions == 10000:
        print("_____________\nCOMPLETED 10,000\n_____________")

root.mainloop()
