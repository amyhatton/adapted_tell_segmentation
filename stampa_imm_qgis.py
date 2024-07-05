import pickle #for serialization
from qgis.PyQt import QtGui #
import os 
import random
import numpy as np
import json

my_path = "/Users/hatton/Nextcloud/My files/code/casini_2023/adapted_tell_segmentation"
project = QgsProject.instance()
print(project.mapLayers())
'vw_site_survey_poly'

#get the working directory
import os 
os.getcwd() 
# path = os.path.dirname(__file__)

def centroid2vec(cx,cy):
    name = "test_tile"
    tile_meters = 1000

    left = cx - (tile_meters/2)
    top = cy + (tile_meters/2)
    right = cx + (tile_meters/2)
    bottom = cy - (tile_meters/2)


    layer =  QgsVectorLayer('Polygon?crs=EPSG:3857', name , "memory") #create a polygon layer called layer and store in memory
    pr = layer.dataProvider() #connection to underlying file or database
    poly = QgsFeature() # a single feature including its id, geom, attributes

    points = [
        QgsPointXY(left,top), #position with x y coords, here the left top coord
        QgsPointXY(right,top),
        QgsPointXY(right,bottom),
        QgsPointXY(left,bottom),
        ]
    poly.setGeometry(QgsGeometry.fromPolygonXY([points])) #set geometry of polygon based on points above
    pr.addFeatures([poly]) #add the polgyon to the data layer
    layer.updateExtents() #update the extent
    QgsProject.instance().addMapLayers([layer]) #add the layer to the current open project in qgis


#It is used to save an image for each site, where the site is in the centre of the image. 
def save_tile(cx,cy,
            tile_meters=500,shiftx=0,shifty=0,
            outputSize=512,
            fn = "", uzbekistan=False,fn1=""):

    rasters = ["Bing aerial"] #google vs bing or whatever other imagery you are using

    project = QgsProject.instance() #the current project
    manager = project.layoutManager() #constructor for layoutmanager - the project will become the parent object for this manager
    layoutName = "ctx_saver" #name of layout
    layouts_list = manager.printLayouts() #stores the names of layout so we can loop trough them

    for layout in layouts_list: #if a layout name = a new layout I want to create we remove it before creating the new one
        if layout.name() == layoutName:
            manager.removeLayout(layout)

    layout = QgsPrintLayout(project) #constructor to create a print layout
    layout.initializeDefaults() #initialises an empty layout
    layout.setName(layoutName) #name the new layout
    manager.addLayout(layout) # add the new layout to the manager

    layers = [] #cretae a list called layers
    for r in rasters: 
        layers = layers + project.mapLayersByName(r) #add the other layers that are rasters?

    assert(os.path.exists(fn)==False) #gives an error if the path fn does already exist

    print(my_path)
    left = cx - (tile_meters/2)
    top = cy + (tile_meters/2)
    right = cx + (tile_meters/2)
    bottom = cy - (tile_meters/2)
    extent = QgsRectangle(left,top,right,bottom) #set the extent of a rectangle
    if(uzbekistan==True): # choose the set of points (eg usbekistan or other area)
        df_sites = pd.read_csv(my_path + "/testsetUzbeko_v2.csv") #read in the dataframe of points
        df_sites.loc[df_sites['ShortCode'] == fn1, ['extent']] = extent #?? locate the sites where shortcode = fn1
        df_sites.to_csv(my_path + "/testsetUzbeko_v2.csv", index=False) #write csv file

    map = QgsLayoutItemMap(layout)
    map.setRect(0,0,outputSize,outputSize)
    ms = QgsMapSettings()
    ms.setLayers(layers)
    ms.setExtent(extent)
    map.setExtent(extent)
    ms.setOutputSize(QSize(outputSize,outputSize))
    layout.addLayoutItem(map)
    map.attemptMove(QgsLayoutPoint(0,0,QgsUnitTypes.LayoutPixels))
    map.attemptResize(QgsLayoutSize(outputSize,outputSize,QgsUnitTypes.LayoutPixels))
    layout.pageCollection().page(0).setPageSize(map.sizeWithUnits())

    exporter = QgsLayoutExporter(layout)
    
    exporter.exportToImage(fn, QgsLayoutExporter.ImageExportSettings())
    layout.removeLayoutItem(map)
    return True
    
    


import pandas as pd


    
    
#function to create tiles 
def save_dataset_1000(masks,TEST=None,NEGS=None,TRAIN=None):
    df_sites = pd.read_csv(my_path + r"/trainset1000.csv") #read in sites from train set csv
    df_negs = pd.read_csv(my_path + r"/negs1000.csv") #read in 
    df_maysan = pd.read_csv(my_path + r"/maysan1000.csv")
    print(df_maysan.shape) #get the number of rows and columns in df_maysan
    # masks
    if masks:
        if TEST:
            for i,s in df_maysan.iterrows():
                save_tile(s.cx,s.cy,tile_meters=1000,outputSize=1024,
                    fn= my_path + "/datasets/bing_1k/maysan/masks/"+str(s.entry_id)+".png"
                )
                if i%100==0: print("img:",i)
            print("Mask test done")
        if TRAIN:    
            for i,s in df_sites.iterrows():
                save_tile(s.cx,s.cy,tile_meters=1000,outputSize=1024,
                    fn= my_path + "/datasets/bing_1k/train/masks/"+str(s.entry_id)+".png"
                )
                if i%100==0: print("img:",i)
            print("Mask train done")
        if NEGS:
            for i,s in df_negs.iterrows():
                save_tile(s.cx,s.cy,tile_meters=1000,outputSize=1024,
                    fn= my_path +  "/datasets/bing_1k/train/masks/"+str(s.id)+".png"
                )
                if i%100==0: print("img:",i)
            print("Mask negs done")
    # sites
    else:
        if TRAIN:
            for i,s in df_sites.iterrows():
                save_tile(s.cx,s.cy,tile_meters=1000,outputSize=1024,
                    fn=my_path + "/datasets/bing_1k/train/sites/"+str(s.entry_id)+".jpg"
                )
                if i%100==0: print("img:",i)
            print("sites train done")
        if NEGS:
            for i,s in df_negs.iterrows():
                save_tile(s.cx,s.cy,tile_meters=1000,outputSize=1024,
                    fn=my_path + "/datasets/bing_1k/train/sites/"+str(s.id)+".jpg"
                )
                if i%100==0: print("img:",i)
            print("sites negs done")
        if TEST:
            for i,s in df_maysan.iterrows():
                save_tile(s.cx,s.cy,tile_meters=1000,outputSize=1024,
                    fn=my_path + "/datasets/bing_1k/maysan/sites/"+str(s.entry_id)+".jpg"
                )
                if i%100==0: print("img:",i)
            print("sites test done") 

#is used to save the co-ordinates of each tile centroid in the selection area
def save_coor(cx,cy,idx):
    dictionary = {
    "name": "tile"+str(idx) ,
    "cx": cx,
    "cy": cy}
    with open(my_path + "coor_maysan.json") as fp:
        listObj = json.load(fp)
    
    listObj.append(dictionary)
    with open(my_path + "coor_maysan.json", "w") as json_file:
        json.dump(listObj, json_file,
                indent=4,
                separators=(',', ': '))


#given a polygon, returns the list of vertices
def extract_vertex_from_polygon(fn=my_path + 'sel_area.shp'):
    layer=QgsVectorLayer(fn)
    iter = layer.getFeatures()
    for feature in iter:
        geom = feature.geometry()
        vertices = feature.geometry().asMultiPolygon()
        points = []
        for v in vertices:
            points.append(v)
        points=points[0][0]
        return(points)

def tile_maysan(masks,fn=my_path + 'sel_area_512.shp'):
    points=extract_vertex_from_polygon(fn)[:-1]
    #print(points[1][0])
    points_order=np.sort(np.array(points).ravel())
    #print(points_order)
    coordinateX=points_order[4:]
    coordinateY=points_order[:-4]
    #print(coordinateY)
    est=max(coordinateX)
    nord=max(coordinateY)
    ovest=min(coordinateX)
    sud=min(coordinateY)
    
    tile_spost=500
    cx=ovest+tile_spost
    cy=sud+tile_spost
    print((est-cx)/(tile_spost*2))
    iterorr=round((est-cx)/(tile_spost*2)+0.01)
    itervert=round((nord-cy)/(tile_spost*2)+0.01)
    print(iterorr)
    itertot=iterorr*itervert
    print("it will create`: ",itertot," images")
    scorr_vert=False
  
    for i in range(1,itertot+1):
        
        if(scorr_vert==False):
            cx=cx+tile_spost*2
            if(i==1): cx=ovest+tile_spost
            if(masks==True):
                save_tile(cx,cy,tile_meters=1000,outputSize=1024,
                fn=my_path + "/datasets/maysan_sel_tile/masks/"+str(i)+".png")
            else:
                save_tile(cx,cy,tile_meters=1000,outputSize=1024,
                fn=my_path +"/datasets/maysan_sel_tile/sites/"+str(i)+".jpg")
                #save_coor(cx,cy,i)
            if(i%iterorr)==0: scorr_vert=True
        else:
            cy=cy+tile_spost*2
            cx=ovest+tile_spost
            if(masks==True):
                save_tile(cx,cy,tile_meters=1000,outputSize=1024,
                fn=my_path +"/datasets/maysan_sel_tile/masks/"+str(i)+".png")
            else:
                save_tile(cx,cy,tile_meters=1000,outputSize=1024,
                fn=my_path +"/datasets/maysan_sel_tile/sites/"+str(i)+".jpg")
                #save_coor(cx,cy,i)
            scorr_vert=False
    print("Done!")

#saves the dataset size 2048x2048 pixels, if filter=True the dataset is filtered
def save_dataset_2000(filter,masks,TEST=None,NEGS=None,TRAIN=None):
    df_sites = pd.read_csv(my_path + r"./dataset1000withFilter.csv")
    df_negs = pd.read_csv(my_path +r"./negs1000.csv")
    df_maysan = pd.read_csv(my_path +r"./maysan1000.csv")
    if (filter==True): df_sites=df_sites[df_sites["filter"]==True]
    print(df_sites.shape)
    # masks
    if masks:
        if TEST: #if its the test set then
            for i,s in df_maysan.iterrows(): #iterate through the rows of df
                save_tile(s.cx,s.cy,tile_meters=2000,outputSize=2048, #use save tile funtion and save tile with 2000mx2000m and 2048 pixels
                    fn=my_path +"/datasets/bing_2k/maysan/masks/"+str(s.entry_id)+".png" #locations and name of the tile
                )
                if i%100==0: print("img:",i) #if i is divisible by 100 then print img: i
            print("Mask test done") 
        if TRAIN:    
            for i,s in df_sites.iterrows():
                save_tile(s.cx,s.cy,tile_meters=2000,outputSize=2048,
                    fn=my_path +"/datasets/bing_2k/train/masks/"+str(s.entry_id)+".png"
                )
                if i%100==0: print("img:",i)
            print("Mask train done")
        if NEGS: #these are for non-sites 
            for i,s in df_negs.iterrows():
                save_tile(s.cx,s.cy,tile_meters=2000,outputSize=2048,
                    fn=my_path +"/datasets/bing_2k/train/masks/"+str(s.id)+".png"
                )
                if i%100==0: print("img:",i)
            print("Mask negs done")
    # sites
    else:
        if TRAIN:
            for i,s in df_sites.iterrows():
                save_tile(s.cx,s.cy,tile_meters=2000,outputSize=2048,
                    fn=my_path +"/datasets/bing_2k/train/sites/"+str(s.entry_id)+".jpg"
                )
                if i%100==0: print("img:",i)
            print("sites train done")
        if NEGS:
            for i,s in df_negs.iterrows():
                save_tile(s.cx,s.cy,tile_meters=2000,outputSize=2048,
                    fn=my_path +"/datasets/bing_2k/train/sites/"+str(s.id)+".jpg"
                )
                if i%100==0: print("img:",i)
            print("sites negs done")
        if TEST:
            for i,s in df_maysan.iterrows():
                save_tile(s.cx,s.cy,tile_meters=2000,outputSize=2048,
                    fn=my_path +"/datasets/bing_2k/maysan/sites/"+str(s.entry_id)+".jpg"
                )
                if i%100==0: print("img:",i)
            print("sites test done") 

def save_dataset_2000_uzbeko(masks):
    df_sites = pd.read_csv(my_path +"testsetUzbeko_v2.csv")
    print(df_sites.shape)
    # masks
    if masks:
        for i,s in df_sites.iterrows():
            save_tile(s.cx,s.cy,tile_meters=2000,outputSize=2048,
                    fn=my_path +"/datasetUzbeko/masks/"+str(s.ShortCode)+".png",
                    uzbekistan=True,fn1=str(s.ShortCode)
                )
            if i%100==0: print("img:",i)
        print("Mask train done")
        
    # sites
    else:
       
        for i,s in df_sites.iterrows():
            save_tile(s.cx,s.cy,tile_meters=2000,outputSize=2048,
                fn=my_path +"/datasetUzbeko/sites/"+str(s.ShortCode)+".jpg"
            )
            if i%100==0: print("img:",i)
        print("sites train done")
       
