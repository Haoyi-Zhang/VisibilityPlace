"""Vector drawing primitives; copied into each independent project generator."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

plt.rcParams.update({'font.family':'STIXGeneral', 'mathtext.fontset':'stix',
                     'font.size':9, 'pdf.fonttype':42, 'ps.fonttype':42,
                     'text.usetex':False, 'axes.unicode_minus':False})
CM = 1 / 2.54

class Drawing:
    def __init__(self, bounds):
        x0,y0,x1,y1 = bounds
        self.fig = plt.figure(figsize=((x1-x0)*CM,(y1-y0)*CM))
        self.ax = self.fig.add_axes([0,0,1,1], xlim=(x0,x1), ylim=(y0,y1))
        self.ax.set_aspect('equal'); self.ax.axis('off')
        self.nodes = {}
        self.labels = []

    def text(self,x,y,label,size=9,ha='center',va='center'):
        artist=self.ax.text(x,y,label,fontsize=size,ha=ha,va=va,
                            linespacing=1.15,clip_on=False,zorder=4)
        self.labels.append([artist,None])
        return artist

    def box(self,name,x,y,w,h,label,dashed=False,shape='rect',size=9):
        style = {'edgecolor':'black','facecolor':'white','linewidth':.55,
                 'linestyle':(0,(4,3)) if dashed else 'solid', 'zorder':2}
        if shape == 'diamond':
            obj = Polygon([(x-w/2,y),(x,y+h/2),(x+w/2,y),(x,y-h/2)],**style)
        elif shape == 'circle': obj = Circle((x,y),w/2,**style)
        else: obj = Rectangle((x-w/2,y-h/2),w,h,**style)
        self.ax.add_patch(obj); self.text(x,y,label,size)
        self.labels[-1][1]=(x-w/2,y-h/2,x+w/2,y+h/2)
        self.nodes[name] = (x,y,w,h,shape)

    def point(self,name,side):
        x,y,w,h,_ = self.nodes[name]
        return {'n':(x,y+h/2),'s':(x,y-h/2),'e':(x+w/2,y),
                'w':(x-w/2,y),'nw':(x-w/2,y+h/2),
                'ne':(x+w/2,y+h/2),'c':(x,y)}[side]

    def line(self,points,dashed=False):
        xs,ys=zip(*points)
        self.ax.plot(xs,ys,color='black',linewidth=.55,
                     linestyle=(0,(4,3)) if dashed else 'solid',zorder=1)

    def arrow(self,p,q,dashed=False,via=()):
        points=[p,*via,q]
        if via:self.line(points[:-1],dashed)
        self.ax.add_patch(FancyArrowPatch(points[-2],points[-1],
                         arrowstyle='-|>',mutation_scale=7.5,linewidth=.55,
                         color='black',shrinkA=0,shrinkB=0,
                         linestyle=(0,(4,3)) if dashed else 'solid',zorder=1))

    def edge(self,a,b,sa='s',sb='n',**kwargs):
        self.arrow(self.point(a,sa),self.point(b,sb),**kwargs)

    def frame(self,x,y,w,h):
        self.ax.add_patch(Rectangle((x,y),w,h,fill=False,edgecolor='black',
                                   linewidth=.55,linestyle=(0,(4,3)),zorder=0))

    def save(self,out,name):
        # Fixed physical canvas: do not enlarge or rasterize the scientific figure.
        self.fig.canvas.draw()
        renderer=self.fig.canvas.get_renderer()
        x0,x1=self.ax.get_xlim();y0,y1=self.ax.get_ylim()
        for artist,node in self.labels:
            b=artist.get_window_extent(renderer).transformed(self.ax.transData.inverted())
            if b.x0<x0-.02 or b.x1>x1+.02 or b.y0<y0-.02 or b.y1>y1+.02:
                raise ValueError(name+': clipped label '+repr(artist.get_text()))
            if node and (b.x0<node[0]-.02 or b.x1>node[2]+.02 or b.y0<node[1]-.02 or b.y1>node[3]+.02):
                raise ValueError(name+': label exceeds node '+repr(artist.get_text()))
        self.fig.savefig(out/(name+'.pdf'),format='pdf',
                         metadata={'Creator':'Python Matplotlib','Producer':None,
                                   'CreationDate':None,'ModDate':None})
        plt.close(self.fig)


def compiler(out):
    d = Drawing((0, 0, 8.9, 4.2))
    for name,x,y,label in [('s',.45,2.3,'$s$'),('u',1.6,3.0,'$u$'),
                            ('v',1.6,1.5,'$v$'),('t',2.85,2.3,'$t$')]:
        d.box(name,x,y,.43,.43,label,shape='circle',size=8)
    d.edge('s','u','n','w'); d.edge('s','v','s','w')
    d.edge('u','t','e','n'); d.edge('v','t','e','s')
    d.text(.83,2.95,'keep',7.5); d.text(.8,1.62,'restrict',7.5)
    d.text(2.65,1.43,'boundary',7.5)
    d.box('pm1',1.6,3.72,.68,.4,'$m_1$',size=8)
    d.box('pm2',1.6,.8,.68,.4,'$m_2$',size=8)
    d.text(1.65,.25,'(a) Policy states',8)
    d.line([(3.35,.08),(3.35,4.1)],dashed=True)
    for name,x,y,label,w in [
        ('S',3.8,1.15,'$S$',.42),('s0',4.25,2.55,'$s,0$',.7),
        ('u0',5.5,3.35,'$u,0$',.7),('m1',6.6,3.35,'$m_1$',.65),
        ('t0',8.0,2.55,'$t,0$',.7),('v1',5.5,1.3,'$v,1$',.7),
        ('t1',7.55,1.3,'$t,1$',.7),('T',8.55,.85,'$T$',.42)]:
        d.box(name,x,y,w,.42,label,size=8)
    d.edge('S','s0','n','s'); d.edge('s0','u0','n','w')
    d.edge('u0','m1','e','w');d.edge('m1','t0','e','n')
    d.edge('s0','v1','e','n');d.edge('v1','t1','e','w',dashed=True)
    d.text(6.5,1.0,'disabled',7.5)
    d.edge('t0','T','s','n'); d.edge('t1','T','e','w')
    d.text(6.45,.25,'(b) Compiled paths',8)
    d.save(out,'compiler')


def certificate(out):
    d = Drawing((0, 0, 8.6, 3.0))
    for name,x,label in [('s',.45,'$0$'),('u',2.1,'$a$'),
                         ('v',6.15,'$a+1$'),('t',8.1,'$k$')]:
        d.box(name,x,2.25,.7,.7,label,shape='circle',size=8.5)
    d.edge('s','u','e','w',dashed=True)
    d.edge('u','v','e','w')
    d.edge('v','t','e','w',dashed=True)
    d.text(1.25,2.65,r'$\cdots$',8.5);d.text(7.15,2.65,r'$\cdots$',8.5)
    d.text(3.15,2.62,'$e_m$',8.5);d.text(5.05,2.62,'$y_m$',8.5)
    d.text(4.1,1.87,'$X_m=1$',8.5)
    d.box('p',2.1,.62,3.2,.62,r'$h_v-h_u\leq X_m$',size=8.5)
    d.box('dual',6.2,.62,3.2,.62,r'$y_m-z_m\leq c_m$',size=8.5)
    d.arrow((2.95,2.14),d.point('p','n'))
    d.arrow((5.2,2.14),d.point('dual','n'))
    d.save(out,'certificate')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    compiler(args.output);certificate(args.output)


