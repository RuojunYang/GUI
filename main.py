import tkinter as tk
import datetime
from tkcalendar import *
from configparser import ConfigParser
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from mpl_toolkits.basemap import Basemap


def gui(name):
    config = ConfigParser()
    config.read('config.cfg')
    window = tk.Tk()
    window.title('GUI_' + name)
    window.geometry('1400x800')
    window.configure(bg='white')
    a = DoubleVar()
    b = DoubleVar()
    c = DoubleVar()
    d = DoubleVar()

    s = tk.Scale(window, label=config.get('variables', 'v1'), from_=0.7, to=1.3, orient=tk.HORIZONTAL,
                 length=200, showvalue=True, tickinterval=0.1, resolution=0.01, variable=a)
    s.configure(bg='white')
    s.set(1)
    s.place(x=0, y=0)
    # s.pack()
    s = tk.Scale(window, label=config.get('variables', 'v2'), from_=0.7, to=1.3, orient=tk.HORIZONTAL,
                 length=200, showvalue=True, tickinterval=0.1, resolution=0.01, variable=b)
    s.configure(bg='white')
    s.set(1)
    s.place(x=0, y=80)
    # s.pack()
    s = tk.Scale(window, label=config.get('variables', 'v3'), from_=0.7, to=1.3, orient=tk.HORIZONTAL,
                 length=200, showvalue=True, tickinterval=0.1, resolution=0.01, variable=c)
    s.configure(bg='white')
    s.set(1)
    s.place(x=0, y=160)
    # s.pack()
    s = tk.Scale(window, label=config.get('variables', 'v4'), from_=0.7, to=1.3, orient=tk.HORIZONTAL,
                 length=200, showvalue=True, tickinterval=0.1, resolution=0.01, variable=d)
    s.configure(bg='white')
    s.set(1)
    s.place(x=0, y=240)
    # s.pack()

    now = datetime.datetime.now()
    cal = Calendar(window, selectmode='day', year=now.year, month=now.month, day=now.day)
    cal.place(x=0, y=340)

    fig = Figure(figsize=(10, 8), dpi=100)
    ax = fig.gca()
    extent = [config.getint('variables', 'min_lon'), config.getint('variables', 'max_lon'),
              config.getint('variables', 'min_lat'), config.getint('variables', 'max_lat')]
    # extent = [-180, 180, -90, 90]
    bm = Basemap(llcrnrlon=extent[0], llcrnrlat=extent[2],
                 urcrnrlon=extent[1], urcrnrlat=extent[3],
                 projection='cyl', resolution='l', fix_aspect=False, ax=ax)
    step = int(min(config.getint('variables', 'max_lon') - config.getint('variables', 'min_lon'), config.getint('variables', 'max_lat') - config.getint('variables', 'min_lat'))/10)
    bm.drawcoastlines()
    bm.drawcountries()
    bm.drawcounties()
    meridians = np.arange(extent[0], extent[1] + step, step)
    parallels = np.arange(extent[2], extent[3] + step, step)

    ax.set_yticks(parallels)
    ax.set_yticklabels(parallels)
    ax.set_xticks(meridians)
    ax.set_xticklabels(meridians)
    ax.set_xlabel('Longitude (°E)', labelpad=10)
    ax.set_ylabel('Latitude (°N)', labelpad=10)
    bm.readshapefile('./CHN_adm1/CHN_adm1', 'states', drawbounds=True, linewidth=2, color='black')
    bm.readshapefile('./CHN_adm2/CHN_adm2', 'states', drawbounds=True, linewidth=1, color='black')
    ax.set_title(
        cal.get_date())
    dt = datetime.datetime.strptime(cal.get_date(), '%m/%d/%y')
    doy = (dt - datetime.datetime(dt.year, 1, 1)).days + 1
    dt_str = dt.strftime('%Y%m%d')

    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.figure = fig

    canvas.draw()
    canvas.get_tk_widget().place(x=300, y=0)
    button = tk.Button(window, text="Update Figure", command=lambda: sel(canvas))
    button.place(x=0, y=520)
    # button.pack()

    label = Label(window)
    label.place(x=0, y=360)

    def sel(canvas):
        fig = Figure(figsize=(10, 8), dpi=100)
        ax = fig.gca()
        extent = [config.getint('variables', 'min_lon'), config.getint('variables', 'max_lon'),
                  config.getint('variables', 'min_lat'), config.getint('variables', 'max_lat')]
        # extent = [-180, 180, -90, 90]
        bm = Basemap(llcrnrlon=extent[0], llcrnrlat=extent[2],
                     urcrnrlon=extent[1], urcrnrlat=extent[3],
                     projection='cyl', resolution='l', fix_aspect=False, ax=ax)
        step = int(min(config.getint('variables', 'max_lon') - config.getint('variables', 'min_lon'),
                       config.getint('variables', 'max_lat') - config.getint('variables', 'min_lat')) / 10)
        bm.drawcoastlines()
        bm.drawcountries()
        bm.drawcounties()
        meridians = np.arange(extent[0], extent[1] + step, step)
        parallels = np.arange(extent[2], extent[3] + step, step)

        ax.set_yticks(parallels)
        ax.set_yticklabels(parallels)
        ax.set_xticks(meridians)
        ax.set_xticklabels(meridians)
        ax.set_xlabel('Longitude (°E)', labelpad=10)
        ax.set_ylabel('Latitude (°N)', labelpad=10)
        bm.readshapefile('./CHN_adm1/CHN_adm1', 'states', drawbounds=True, linewidth=2, color='black')
        bm.readshapefile('./CHN_adm2/CHN_adm2', 'states', drawbounds=True, linewidth=1, color='black')
        ax.set_title(
            cal.get_date())
        dt = datetime.datetime.strptime(cal.get_date(), '%m/%d/%y')
        doy = (dt - datetime.datetime(dt.year, 1, 1)).days + 1
        dt_str = dt.strftime('%Y%m%d')
        canvas.figure = fig

        canvas.draw()
        canvas.get_tk_widget().place(x=300, y=0)

    window.resizable(False, False)

    window.mainloop()


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.cfg')
    gui(config.get('variables', 'name'))
