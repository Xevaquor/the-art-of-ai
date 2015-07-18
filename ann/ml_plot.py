# -*- coding: utf-8 -*-
"""
The art of an Artificial Intelligence
http://art-of-ai.com
https://github.com/Xevaquor/the-art-of-ai

Module in this version does not handle w = [0,0,0] or w = [_, _, 0] properly
"""

__author__ = 'xevaquor'
__license__ = 'MIT'

import numpy as np
import matplotlib.pyplot as plt
 
def init_common(plot_size=[-5,5,-5,5]):
    plt.grid()
    ax = plt.axes()
    ax.set_aspect('equal')
    plt.axis(plot_size)
 
def plot_boundary(w, fill=True, linecolor='black', pos_color='green',
                  neg_color='purple'):
    X = np.linspace(-100,100,50)    
    Y = (-w[1] * X - w[0]) / w[2]
    plt.plot(X, Y, color=linecolor)
    
    if not fill:
        return
    
    ax = plt.axes()
    angle = np.arctan2(w[2], w[1])
    if angle < 0: 
        pos_color, neg_color = neg_color, pos_color
    
    ax.fill_between(X, Y, y2=-100, interpolate=True, color=neg_color, alpha=0.2)
    ax.fill_between(X, Y, y2=100, interpolate=True, color=pos_color, alpha=0.2)
 
def plot_normal_vector(w, head_len=0.5, head_width=0.3, color='black'):
    d = -w[0] / np.linalg.norm(w[1:])
    angle = np.arctan2(w[2], w[1])    
    xoffset = np.cos(angle) * d
    yoffset = np.sin(angle) * d
    ax = plt.axes()
    if np.abs(head_len) > np.max(np.abs(w[1:])):
        print('[ml_plot] Arrow too $short, omitting') # yes, I know it is possible to
        # handle it
        return

    dx = w[1] - head_len * np.cos(angle)
    dy = w[2] - head_len * np.sin(angle)
    ax.arrow(xoffset, yoffset, dx, dy,ec=color, fc=color,
             head_width=head_width, head_length = head_len, antialiased=True)
             
if __name__ == '__main__':
    w = [-2,2,2]
    init_common()
    plot_boundary(w, neg_color='orange')
    plot_normal_vector(w)
    