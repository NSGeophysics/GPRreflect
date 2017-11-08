# -*- coding: utf-8 -*-
"""
Created on Fri May  8 09:33:24 2015
Updated on Tue Apr  4 2017 

@author: plattner@alumni.ethz.ch

GPRreflect module
"""


def drawReflector(xax,depth,xs,ys):
    # Content of the function drawReflector is copied
    # from http://matplotlib.org/users/event_handling.html
    
    from matplotlib import pyplot as plt
    import numpy as np
    
    class PointCollecting:
        def __init__(self, line):
            self.line = line
            self.xs = list(line.get_xdata())
            self.ys = list(line.get_ydata())
            self.cid = line.figure.canvas.mpl_connect('button_press_event',self)
        
        def __call__(self, event):
            #print 'coords', self.xs, self.ys
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()


    fig=plt.figure()
    ax=fig.add_subplot(111)

    ax.set_xlabel('along profile position')
    ax.set_ylabel('depth')
    ax.set_aspect('equal')
    ax.axis([xax[0],xax[1],-abs(depth),0])
    ax.set_title('Add reflector, close without adding reflector to calculate')
    

    #refl,=ax.plot(xs, ys,'.',markersize=2)
    refl,=ax.plot([],[])

    PointCollecting = PointCollecting(refl)
    
    ax.hold=True
    ax.plot(xs, ys,'.',markersize=2)

    plt.show()
    x=np.asarray(refl.get_xdata())
    y=np.asarray(refl.get_ydata())
    
    return x,y


def smoothit(x,y,winsize,res):

    import numpy as np

    from scipy import interpolate

    t = np.arange(0,x.size,1)
    fx = interpolate.interp1d(t,x)
    fy = interpolate.interp1d(t,y)

    ti = np.arange(0,x.size-1,res)
    xi=fx(ti)
    yi=fy(ti)



    # Now calculate running mean
    # Put first value of xs winsize times
    xilong=np.insert(xi,0,[xi[0]]*winsize)
    xiloong=np.append(xilong,[xi[-1]]*winsize)
    yilong=np.insert(yi,0,[yi[0]]*winsize)
    yiloong=np.append(yilong,[yi[-1]]*winsize)

    # Define the zero arrays to be filled
    xs=[0]*xi.size
    ys=[0]*yi.size

    for i in range(winsize, ti.size+winsize):
        xs[i-winsize]=np.mean(xiloong[range(i-winsize,i+winsize)])
        ys[i-winsize]=np.mean(yiloong[range(i-winsize,i+winsize)])

    xs=np.asarray(xs)
    ys=np.asarray(ys)
    return xs,ys



def GPRreflect(x,z,v):

    import numpy as np
    
    # Define what we mean by near horizontal:
    horz=0.0001

    # First calculate tangent
    xtan = x[range(1,x.size)] - x[range(0,x.size-1)]
    ztan = z[range(1,x.size)] - z[range(0,x.size-1)]
    tannorm = np.sqrt(np.square(xtan) + np.square(ztan))
    xtan=xtan/tannorm
    ztan=ztan/tannorm

    # Perpendicular direction of [a b] is [-b a]
    zperp = -xtan
    xperp = ztan

    # Remove all points where the perpendicular direction is (almost) horizontal
    zperp = zperp[np.where(abs(zperp)>horz)]
    xperp = xperp[np.where(abs(zperp)>horz)]
    x = x[np.where(abs(zperp)>horz)]
    z = z[np.where(abs(zperp)>horz)]


    # For each perpendicular direction, calculate where the line along it
    # hits the subsurface
    t=-np.divide(z,zperp)
    # Surface x position
    xp=x+t*xperp
    # Length of this line
    dist = np.sqrt( np.square(x-xp) + np.square(z) )
    # Two way travel time
    tp=2*dist/v

    return xp,tp


def showGPR(xax,depth,v):

    from matplotlib import pyplot as plt
    import numpy as np

    # Set some parameters: Displayed travel time is 200 ns:
    travtime = 200

    # 'Close window when you are done drawing the reflector'

    winsize=50
    res=1./100.

    xx=np.empty(0)
    yy=np.empty(0)
    xxs=np.empty(0)
    yys=np.empty(0)
    xxp=np.empty(0)
    ttp=np.empty(0)


    while True:
        x,y = drawReflector(xax,depth,xxs,yys)
        if x.size==0:
            break
        xs,ys = smoothit(x,y,winsize,res)
        xx=np.append(xx,x)
        yy=np.append(yy,y)
        xxs=np.append(xxs,xs)
        yys=np.append(yys,ys)

        # Call GPRreflect and plot both in a subplot thing
        xp,tp =  GPRreflect(xs,ys,v)
        xxp=np.append(xxp,xp)
        ttp=np.append(ttp,tp)


    f, axarr = plt.subplots(2, sharex=True)

    axarr[0].plot(xx,yy,'x')
    axarr[0].hold=True
    axarr[0].plot(xxs,yys,'.',markersize=2)
    axarr[0].set_ylabel('depth [m]')
    #axarr[0].set_aspect('equal')
    axarr[0].axis([xax[0],xax[1],-abs(depth),0])


    axarr[1].plot(xxp,-ttp,'.',markersize=3)
    axarr[1].set_ylabel('two way travel time [ns]')
    axarr[1].axis([xax[0],xax[1],-travtime, 0])
    axarr[1].set_xlabel('Along profile position [m]')

    plt.show()


if __name__ == "__main__":
    showGPR([0,20],5,0.06)

