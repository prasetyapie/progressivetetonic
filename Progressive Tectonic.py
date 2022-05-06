#Arch 431//Medium//Spring 22//Ericson
#
#Pietra Prasetya
#04.27.22
#
#Progressive Tectonic
#
#This project creates Networked Housing Complex On Any Site
#
#
#*****************************************************************************

#imported Libraries

import rhinoscriptsyntax as rs
import math
from math import*
from scriptcontext import escape_test
import random
from random import randrange
import scriptcontext as sc
import Rhino
import System

###############################################

### DEFINITIONS ###

def random_points_in_curve(min_x,min_y,max_x,max_y,number,curve):
    count = 0
    points = []
    while count <= number:
        x = random.uniform(min_x,max_x)
        y = random.uniform(min_y,max_y)
        point = x,y
        point = rs.AddPoint(point)
        if rs.PointInPlanarClosedCurve(point,curve)== 1 :
            count += 1
        if rs.PointInPlanarClosedCurve(point,curve)== 0 :
            rs.DeleteObject(point)
        points.append(point)
    return (points)

def box(line,number):
    box = rs.BoundingBox(line)
    box = rs.coerce3dpointlist(box)


    point_a = box[0]
    point_b = box[1]
    point_c = box[2]
    point_d = box[3]


    min_x = point_a[0]
    min_y = point_a[1]

    max_x = point_c[0]
    max_y = point_c[1]
    points = random_points_in_curve(min_x,min_y,max_x,max_y,number,line)
    return (points)

def move_start_point_angle( start_point , angle , distance ):
    start_x , start_y = start_point[0], start_point[1]
    new_x = cos(radians(angle))*distance + start_x
    new_y = sin(radians(angle))*distance + start_y
    
    return (new_x, new_y)

def explode_point(Start_Point,Distance,Number,Site):
    Count = 0
    Lines = []
    P_end = []
    while Count <= Number:
        Count += 1
        A = random.uniform(-Distance,Distance)
        B = random.uniform(-Distance,Distance)
        C = random.uniform(-Distance,Distance)
        P2 = ( Start_Point[0] + A , Start_Point[1] + B , Start_Point [2] )
        P2_point = rs.AddPoint(P2)
        if rs.PointInPlanarClosedCurve(P2_point,Site) == 1 :
            P_end.append(P2)
        if rs.PointInPlanarClosedCurve(P2_point,Site) == 0 :
            rs.DeleteObject(P2_point)
    return (P_end)

def make_building ( start_point , point_b , point_c , Max_Height , Thickness ):
    

    mid_point = ( ( (start_point[0]+point_b[0]+point_c[0]) / 3) , ( (start_point[1]+point_b[1]+point_c[1]) / 3)  )

    points = start_point , point_b , point_c , mid_point

    for i in points:
        rs.AddPoint(i)

    line_1 = rs.AddLine( start_point , mid_point)
    line_2 = rs.AddLine( point_b , mid_point)
    line_3 = rs.AddLine( point_c , mid_point)

    vector = rs.AddLine( (0,0,0) , (0,0,Max_Height) )

    surface_1 = rs.ExtrudeCurve( line_1 , vector)
    surface_2 = rs.ExtrudeCurve( line_2 , vector)
    surface_3 = rs.ExtrudeCurve( line_3 , vector)

    build_1 = rs.OffsetSurface( surface_1 , Thickness , tolerance = None, both_sides = True , create_solid = True)
    build_2 = rs.OffsetSurface( surface_2 , Thickness , tolerance = None, both_sides = True , create_solid = True)
    build_3 = rs.OffsetSurface( surface_3 , Thickness , tolerance = None, both_sides = True , create_solid = True)
    object_color(build_1)
    object_color(build_2)
    object_color(build_3)
    rs.DeleteObjects(line_1)
    rs.DeleteObjects(line_2)
    rs.DeleteObjects(line_3)
    rs.DeleteObjects(surface_1)
    rs.DeleteObjects(surface_2)
    rs.DeleteObjects(surface_3)
    rs.DeleteObjects(vector)

def branch( start_point, end_point , angle_add , max_length , min_length, Max_Height , Max_Width ,Site ):
    
    
    unit_block = []
    
    ### list points
    start_x , start_y   =  start_point[0], start_point[1] 
    end_x , end_y   =  end_point[0] , end_point[1]  

    ### get angle of line_a
    line_a = rs.AddLine ( start_point , end_point )
    
    if (end_x - start_x) == 0 :
        angle_a = 90
    else:
        tangent_a = ( ( end_y - start_y ) / ( end_x - start_x ) )
        angle_a = degrees( math.atan2( ( end_y - start_y ) , ( end_x - start_x ) ))
    
    ### add random angle to angle_a 
    angle_addition = random.uniform(10,angle_add)
    
    angle_b = angle_a + angle_addition
    angle_c = angle_a - angle_addition
    
    ### get end points
    
    point_b = move_start_point_angle(end_point, angle_b, max_length)
    #if rs.PointInPlanarClosedCurve(point_b,Site) == 0 :
    #    rs.DeleteObject(point_b)

    point_c = move_start_point_angle(end_point, angle_c, max_length)
    #if rs.PointInPlanarClosedCurve(point_c,Site) == 0 :
    #    rs.DeleteObject(point_c)
    

    mh = random.uniform(10,Max_Height)
    mw = random.uniform(6,Max_Width)
    #mh = 1
    #mw = 10
    
    make_building(start_point,point_b,point_c,mh,mw)
    

    

    ### looping
    distance = ( rs.Distance(start_point, point_b) + rs.Distance(start_point, point_c) ) / 2
    
    if distance > min_length:
        
        escape_test(True)
        
        angle_addition = random.uniform(10,angle_add)
        
        angle_b2 = angle_b + angle_addition
        angle_c2 = angle_c - angle_addition


        end_b = move_start_point_angle(point_b, angle_b2, max_length*.5)
        if rs.PointInPlanarClosedCurve(point_b,Site) == 1 :
            branch(point_b,end_b,angle_add, max_length*.5, min_length,mh,mw,Site)
            
        end_c = move_start_point_angle(point_c, angle_c2, max_length*.5)
        if rs.PointInPlanarClosedCurve(end_c,Site) == 1 :
            branch(point_c,end_c,angle_add, max_length*.5, min_length,mh,mw,Site)
            
        
    rs.DeleteObjects(line_a)

    return(unit_block)

def object_color(object):
 
    A = random.randint(75,255)
    B = random.randint(100,255)
    C = random.randint(75,255)
    
    Color = rs.CreateColor((A,B,C))
    rs.AddMaterialToObject(object)
    rs.ObjectColor(object,Color)
    Index = rs.ObjectMaterialIndex(object)
    rs.MaterialColor(Index,Color)

def RotateOblique(RotateX):
    Rx = float(RotateX)
    
    rs.RotateView(None,1,angle=Rx)

def hide_grid():
    views = rs.ViewNames()
    for view in views:
        rs.ViewDisplayMode(view,'Rendered')
        rs.ShowGrid(view,show=False)
        rs.ShowGridAxes(view,show=False)
        rs.ShowWorldAxes(view,show=False)

def RotateOblique(RotateX):
    Rx = float(RotateX)
    
    rs.RotateView(None,1,angle=Rx)

def GetCaptureView(Scale,FileName,NewFolder):
    #Source: https://github.com/mcneel/rhino-developer-samples/blob/6/rhinopython/SampleViewCaptureToFile.py
    #Modified by Mark Ericson to include file/folder directory and scale. 2.18.21

    #this function saves the current viewport to the desktop in a specified folder as a png.
    #Use scale to scale up or down the viewport size to inccrease/ecrease resolution
    #Will overwrite folders and files with same name. 


    view = sc.doc.Views.ActiveView;
    if view:
        view_capture = Rhino.Display.ViewCapture()
        view_capture.Width = view.ActiveViewport.Size.Width*Scale
        view_capture.Height = view.ActiveViewport.Size.Height*Scale
        view_capture.ScaleScreenItems = False
        view_capture.DrawAxes = False
        view_capture.DrawGrid = False
        view_capture.DrawGridAxes = False
        view_capture.TransparentBackground = False
        bitmap = view_capture.CaptureToBitmap(view)
        if bitmap:
            #locate the desktop and get path
            folder = System.Environment.SpecialFolder.Desktop
            path = System.Environment.GetFolderPath(folder)
            #convert foldername and file name sto string
            FName = str(NewFolder)
            File = str(FileName)
            #combine foldername and desktop path
            Dir = System.IO.Path.Combine(path,FName)
            #creat path to tje new folder
            NFolder = System.IO.Directory.CreateDirectory(Dir)
            Dir = System.IO.Path.Combine(Dir,FileName +".png")
            print (Dir)
            #save the file
            bitmap.Save(Dir, System.Drawing.Imaging.ImageFormat.Png);

def play():
    
    rs.MessageBox("This Script Will Generate A Networked Housing Complex In Any Chosen Site")
    
    Site = rs.GetObject('Select Site')
    number = rs.GetInteger('How Many Starting Points?')

    box(Site,number)

    startpoints = rs.GetObjects('Select Starting Points')
    
    startpoints = rs.coerce3dpointlist(startpoints)
    
    Max_Angle = rs.GetInteger('Enter Maximum Angle')
    
    Max_Height = rs.GetInteger('Enter Maximum Building Height')
    Max_Width = rs.GetInteger('Enter Maximum Building Width')
    
    Max_Length = rs.GetInteger('Enter Maximum Building Length')
    Min_Length = rs.GetInteger('Enter Minimum Building Length')
    
    for i in startpoints:
        P2 = explode_point(i, 100 , 5 , Site) 
        escape_test(True)
        for j in P2 :
            escape_test(True)
            branch(i,j,Max_Angle,Max_Length,Min_Length,Max_Height,Max_Width, Site)

    
    
    points = rs.ObjectsByType(1)
    curves = rs.ObjectsByType(8)
    

    rs.DeleteObjects(points)
    
    
    #rs.ZoomExtents()
    
    #for i in range(360):
    #    escape_test(True)
    #    rs.Sleep(20)
    #    RotateOblique(1)



### MAIN ###






#play()


GetCaptureView(15,"pietradish2","pietradish")





























#start_point = rs.GetPoint('start')
#end_point = rs.GetPoint('end')
#angle_add = 15
#max_length = 300
#min_length = 20
#Max_Height = 10
#Max_Width = 6
#Site = rs.GetObject('site')

#branch( start_point, end_point , angle_add , max_length , min_length, Max_Height , Max_Width ,Site )
###############################################

