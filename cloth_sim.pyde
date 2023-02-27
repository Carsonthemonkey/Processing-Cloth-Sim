import random
#global variables
gravity = 5

class node:
    def __init__(self, x, y, pin):
        self.pin = pin
        self.x = x
        self.y = y
        self.velocityX = 0
        self.velocityY = 0
        self.col = (255,255,255)
class thread:
    def __init__(self, node1_index, node2_index):
        self.u_index = node1_index
        self.v_index = node2_index
        self.rest = 50
def move_node(node):
    node.x += node.velocityX
    node.y += node.velocityY

def collide(thread):
    buffer = 5
    A_x = nodelist[thread.u_index].x
    A_y = nodelist[thread.u_index].y
    B_x = nodelist[thread.v_index].x
    B_y = nodelist[thread.v_index].y
    
    if mouseX > min(A_x, B_x) - buffer and mouseX < max(A_x, B_x) + buffer and mouseY > min(A_y, B_y) - buffer and mouseY < max(A_y, B_y) + buffer:
        if B_x != A_x:
            if A_x < B_x:
                slope = float(B_y - A_y)/float(B_x - A_x)
                Y_sol = ((mouseX - A_x) * slope) + A_y
            else:
                slope = float(A_y - B_y)/float(A_x - B_x)
                Y_sol = ((mouseX - B_x) * slope) + B_y
            #print("Y solution: %s" %Y_sol)
            #print("mouse Y: %s" % mouseY)
            if mouseY > Y_sol - buffer and mouseY < Y_sol + buffer:
                print(True)
                return True
            else:
                return False
        else:
            return True
def contract(thread):
    Xaccel = ((thread_length(thread) - thread.rest) * ((nodelist[thread.u_index].x - nodelist[thread.v_index].x) / thread_length(thread)))/10
    Yaccel = ((thread_length(thread) - thread.rest) * ((nodelist[thread.u_index].y - nodelist[thread.v_index].y) / thread_length(thread)))/10
    nodelist[thread.u_index].velocityY += -Yaccel
    nodelist[thread.v_index].velocityY += Yaccel
    nodelist[thread.u_index].velocityX += -Xaccel
    nodelist[thread.v_index].velocityX += Xaccel
    
def thread_length(thread):
    return dist(nodelist[thread.u_index].x, nodelist[thread.u_index].y, nodelist[thread.v_index].x, nodelist[thread.v_index].y)

def draw_node(node):
    noStroke()
    fill(node.col[0],node.col[1],node.col[2])
    circle(node.x,node.y, 8)

def draw_thread(thread):
    stroke(255,255,255)
    strokeWeight(5)
    line(nodelist[thread.u_index].x, nodelist[thread.u_index].y, nodelist[thread.v_index].x, nodelist[thread.v_index].y)
    
def cloth_gen(Width, Height, resolution):
    left = width/2 - Width/2
    right = width/2 + Width/2
    top = height/2 - Height/2
    bottom = height/2 + Height/2
    
    vertical_resolution = int((float(resolution) / Width) * Height)
    step_resolution = int(float(Width)/resolution)
    vertical_step_resolution = int(float(Height)/vertical_resolution)

    pointlist = []
    thread_list = []
    
    for y in range(0, Height, int(vertical_step_resolution)):
        for x in range(0, Width, step_resolution):
            pointlist.append(node(x +left, y + 20, False))
    pointlist[0].pin = True
    pointlist[resolution-1].pin = True
    pointlist[(resolution-1) * 3/4].pin = True
    pointlist[(resolution-1) * 1/4].pin = True
    pointlist[(resolution-1) * 1/2].pin = True
    index = 0
    for i in pointlist:
        if index and index % resolution != 0:
            thread_list.append(thread(index, index-1))
        if index < (vertical_resolution - 1) * resolution:
            thread_list.append(thread(index, index + resolution))
        index += 1
    return (pointlist, thread_list)

def thread_gen(nodelist):
    index = 0
    threadlist = []
    for node in nodelist:
        if index:
            threadlist.append(thread(index, index-1))
        index += 1
    return threadlist
            
def setup():
    global nodelist, threadlist, fps
    size(1200,900)
    threadlist = []
    nodelist = []
    
    cloth = cloth_gen(800,500,20)
    nodelist = cloth[0]
    threadlist = cloth[1]
    # nodelist.append(node(width/2, 100, False))
    # nodelist.append(node(width/2 +100, 150, False))
    # nodelist.append(node(width/2, 600, False))
     
    #threadlist = thread_gen(nodelist)
    #nodelist.append(node(width/2,height/2, False))
    #nodelist.append(node(width/2,height/2, True))
            
    
    background(60,40,100)
    fps = 30
    frameRate(fps)
    
def draw():
    global nodelist, threadlist, fps
    background(60,40,100)
    
    #---gravity calculations---
    for node in nodelist:
        if not node.pin:
            node.velocityY += float(gravity)/fps
            
    #---thread pull calculations--
    for thread in threadlist:
        stretch = thread_length(thread) - thread.rest 
        if stretch > 0:
            contract(thread)
    #---drag---
    for node in nodelist:
            node.velocityX *= 0.99
            node.velocityY *= 0.99
    #---Final movement---
    for node in nodelist:
        if not node.pin:
            move_node(node)

        
    #--Draw screen---
    for thread in threadlist:
        draw_thread(thread)
        
    for node in nodelist:
        draw_node(node)
    
    #controls
    if mousePressed:
        for thread in threadlist:
            cut = collide(thread)
            if cut:
                threadlist.remove(thread)
    if keyPressed:
        if key == 'c':
            try:
                threadlist.remove(threadlist[random.randint(0,len(threadlist)-1)])
            except:
                ()

   # circle(particle.x,particle.y,50)
