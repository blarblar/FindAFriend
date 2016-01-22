# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 12:59:50 2016

@author: Dave
"""
import pandas as pd
import os

path = 'C:/Users/Dave/Documents/Python Scripts/yasp/batchtest/'
os.chdir(path)

#display all rows
def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

#returns 4 entries per match, only the hid's 4 teammates
def teammates(df, hid):
    heroFrame = df[df['hero_id'] == hid]
    teammates = df[df['team_id'].isin(heroFrame['team_id'])]
    teammates = teammates[teammates.hero_id != hid]
    
    #this is an alternate formulation that I haven't gotten to run quickly yet
#    teammates = set( [(m, w) for m, w in zip(matches, wins)])
#    #teammates = [(m, w) for m, w in zip(matches, wins)]
#    filter = [(m, w) in teammates for m, w in zip(df.match_id, df.win)] 
#    teammates = df[filter]
    
    return teammates
    
#this is for only getting tandem winrates, not for items    
def friendgames(df,hid):
    
    working = teammates(df, hid)
    heroid = working.loc[:,['hero_id','win']]
    onlyids = heroid['hero_id'].unique()
    onlyids.sort()
    onlywins = heroid.groupby('hero_id').sum()
    onlycounts = heroid['hero_id'].value_counts(sort = False)
    
    toreturn = pd.DataFrame({'hero1':hid,
                             'hero2':onlyids,
                             'numwins':onlywins['win'],
                             'totalgames':onlycounts})
    
    #qwe['hero2'].replace(herodict, inplace=True)
    
    return toreturn
    
#The main method, this creates 109 entries one entry at a time
def packheroitems(df,hid,countfilter = None):
    itemwinbucket = pd.Series()
    itemlossbucket = pd.Series()
    toreturn = pd.DataFrame()
    
    #initialization
    working = teammates(df, hid) #hid's 4 teammates
    heroid = working.loc[:,['hero_id','win']]
    onlyids = heroid['hero_id'].unique() #generate list to iterate over
    onlyids.sort()
    onlywins = heroid.groupby('hero_id').sum() #for hid's winrate
    
    #number of games with each other hid as teammates
    onlycounts = heroid['hero_id'].value_counts(sort = False)
    
    indexcounter = 0  #only for indexing  
    
    for hero in onlyids: #iterate over all friend hid
        current = working[working['hero_id'] == hero]
        
        if hero != hid: #for sanity checking only
            
            #put items of each teammate all in one list for stats
            onlyitems = current[current['win']==True]
            itemwinbucket = itemwinbucket.append(onlyitems['item0'])
            itemwinbucket = itemwinbucket.append(onlyitems['item1'])
            itemwinbucket = itemwinbucket.append(onlyitems['item2'])
            itemwinbucket = itemwinbucket.append(onlyitems['item3'])
            itemwinbucket = itemwinbucket.append(onlyitems['item4'])
            itemwinbucket = itemwinbucket.append(onlyitems['item5'])
            
            onlyitems = current[current['win']==False]
            itemlossbucket = itemlossbucket.append(onlyitems['item0'])
            itemlossbucket = itemlossbucket.append(onlyitems['item1'])
            itemlossbucket = itemlossbucket.append(onlyitems['item2'])
            itemlossbucket = itemlossbucket.append(onlyitems['item3'])
            itemlossbucket = itemlossbucket.append(onlyitems['item4'])
            itemlossbucket = itemlossbucket.append(onlyitems['item5'])
            
            itemwinbucket = itemwinbucket.value_counts()
            itemlossbucket = itemlossbucket.value_counts()
            
            #filter out the items with poor statistics here
            #countfilter removes entries with low numgames from consideration
            if countfilter is not None:
                itemtotals = itemwinbucket + itemlossbucket
                itemtotals = itemtotals[itemtotals > countfilter]
                itemwinbucket = itemwinbucket[itemwinbucket.keys().isin(itemtotals.keys())]
                itemlossbucket = itemlossbucket[itemlossbucket.keys().isin(itemtotals.keys())]
            
            #sort down to completed items only - no half-finished items
            itemwinbucket = itemwinbucket[itemwinbucket.keys().isin(itemexport.keys())]
            itemlossbucket = itemlossbucket[itemlossbucket.keys().isin(itemexport.keys())]
            
            #compare itemwins and itemlosses for winrate analysis
            compare = itemwinbucket/(itemlossbucket + itemwinbucket)
            compare = compare.dropna() #drop any item without both wins and losses
            compare.sort(ascending = False)
    
            #Set values for line entry construction
            #Find the items with the 3 highest and 3 lowest winrates
            win1 = compare.keys()[0]
            win1w = itemwinbucket[win1]
            win1c = itemwinbucket[win1] + itemlossbucket[win1]
            
            win2 = compare.keys()[1]
            win2w = itemwinbucket[win2]
            win2c = itemwinbucket[win2] + itemlossbucket[win2]
            
            win3 = compare.keys()[2]
            win3w = itemwinbucket[win3]
            win3c = itemwinbucket[win3] + itemlossbucket[win3]
            
            loss1 = compare.tail(3).keys()[2]
            loss1w = itemwinbucket[loss1]
            loss1c = itemwinbucket[loss1] + itemlossbucket[loss1]
            
            loss2 = compare.tail(3).keys()[1]
            loss2w = itemwinbucket[loss2]
            loss2c = itemwinbucket[loss2] + itemlossbucket[loss2]
            
            loss3 = compare.tail(3).keys()[0]
            loss3w = itemwinbucket[loss3]
            loss3c = itemwinbucket[loss3] + itemlossbucket[loss3]
            
            numwins = onlywins['win'][hero]
            totalgames = onlycounts[hero]
            
            toappend = pd.DataFrame({'herocompare':hid,
                                     'itemhero':hero,
                                     'witem1':win1,
                                     'witem1numwins':win1w,
                                     'witem1numgames':win1c,
                                     'witem2':win2,
                                     'witem2numwins':win2w,
                                     'witem2numgames':win2c,
                                     'witem3':win3,
                                     'witem3numwins':win3w,
                                     'witem3numgames':win3c,
                                     'litem1':loss1,
                                     'litem1numwins':loss1w,
                                     'litem1numgames':loss1c,
                                     'litem2':loss2,
                                     'litem2numwins':loss2w,
                                     'litem2numgames':loss2c,
                                     'litem3':loss3,
                                     'litem3numwins':loss3w,
                                     'litem3numgames':loss3c,
                                     'numwins':numwins,
                                     'totalgames':totalgames},
                                     index = [indexcounter])
            
            toreturn = toreturn.append(toappend)
            indexcounter += 1
    return toreturn
        
        
        
#Set up heroes
heroname = ['Abaddon', 'Alchemist','Ancient Apparition', 'Anti-Mage', 
'Axe', 'Bane', 'Batrider', 'Beastmaster', 'Bloodseeker', 
'Bounty Hunter', 'Brewmaster', 'Bristleback', 'Broodmother', 
'Centaur Warrunner', 'Chaos Knight', 'Chen', 'Clinkz', 
'Clockwerk', 'Crystal Maiden', 'Dark Seer', 'Dazzle', 'Death Prophet',
 'Disruptor', 'Doom', 'Dragon Knight', 'Drow Ranger', 
'Earth Spirit', 'Earthshaker', 'Elder Titan', 'Ember Spirit', 
'Enchantress', 'Enigma', 'Faceless Void', 'Gyrocopter', 
'Huskar', 'Invoker', 'Io', 'Jakiro', 'Juggernaut', 'Keeper of the Light',
 'Kunkka', 'Legion Commander', 'Leshrac', 'Lich', 
'Lifestealer', 'Lina', 'Lion', 'Lone Druid', 'Luna', 'Lycan', 
'Magnus', 'Medusa', 'Meepo', 'Mirana', 'Morphling', 'Naga Siren',
 'Natures Prophet', 'Necrophos', 'Night Stalker', 
'Nyx', 'Ogre Magi', 'Omniknight', 'Oracle', 'Outworld Devourer',
 'Phantom Assassin', 'Phantom Lancer', 'Phoenix', 
'Puck', 'Pudge', 'Pugna', 'Queen of Pain', 'Razor', 'Riki', 
'Rubick', 'Sand King', 'Shadow Demon', 'Shadow Fiend', 'Shadow Shaman',
 'Silencer', 'Skywrath Mage', 'Slardar', 'Slark', 
'Sniper', 'Spectre', 'Spirit Breaker', 'Storm Spirit', 'Sven', 
'Techies', 'Templar Assassin', 'Terrorblade', 'Tidehunter', 
'Timbersaw', 'Tinker', 'Tiny', 'Treant Protector', 'Troll Warlord',
 'Tusk', 'Undying', 'Ursa', 'Vengeful Spirit', 
'Venomancer', 'Viper', 'Visage', 'Warlock', 'Weaver', 
'Windranger', 'Winter Wyvern', 'Witch Doctor', 'Wraith King', 
'Zeus']

heroidnum = [102,73, 68, 1, 2, 3, 65, 38, 4, 62, 78, 99, 61, 96, 81, 66, 
56, 51, 5, 55, 50, 43, 87, 69, 49, 6, 107, 7, 103, 106, 58, 33, 
41, 72, 59, 74, 91, 64, 8, 90, 23, 104, 52, 31, 54, 25, 26, 80, 
48, 77, 97, 94, 82, 9, 10, 89, 53, 36, 60, 88, 84, 57, 111, 76, 
44, 12, 110, 13,  14, 45, 39, 15, 32, 86, 16, 79, 11, 27, 75, 
101, 28, 93, 35, 67, 71, 17, 18, 105, 46, 109, 29, 98, 34, 19, 
83, 95, 100, 85, 70, 20, 40, 47, 92, 37, 63, 21, 112, 30, 42, 
22]

herodict = dict(zip(heroidnum, heroname))

#set up items
import json
def writefile(filename, data):
    with open(filename, 'w') as fout:
        json.dump(data, fout)

def readfile(filename):
    with open(filename, 'r') as fout:
        return json.load(fout)

items = readfile('itemvalues.json')
itemdict = {}

for i in items['items']:
    itemdict[i['id']] = i['localized_name']

itemseries = pd.Series(itemdict)

completeditems = [1,247,31,32,36,37,41,48,220,50,55,63,65,79,81,90,92,
                  96,98,100,232,102,104,201,202,203,204,194,108,110,112,
                  114,116,119,121,123,226,125,242,127,131,135,137,139,
                  141,143,145,147,149,236,151,152,249,154,156,158,160,
                  162,164,166,168,170,172,174,196,176,178,180,235,185,
                  187,229,190,231,206,208,210,212,214,254]
                  
itemexport = itemseries[itemseries.keys().isin(completeditems)]




#initialize
fullframe = pd.read_csv('TotalDecYasp')
fullframe = fullframe.drop('Unnamed: 0',1)

fullframe["team_id"] = fullframe.match_id.map(str) + fullframe.win.map(str)

#hero_id: 0 does not exist, remove any games with hid = 0
todrop = fullframe[fullframe['hero_id']==0] 
fullframe = fullframe[~fullframe['match_id'].isin(todrop['match_id'])]

fullwins = pd.DataFrame() #used for only heroes
fullitems = pd.DataFrame() #used for heroes and items together



#start processing data
for i in range(1, 113):
    print(i) #track progress
    #fullwins = fullwins.append(friendgames(fullframe, i))
    fullitems = fullitems.append(packheroitems(fullframe,i))
               
fullitems.to_csv('filteredwinrateswithitemsnogem.csv')

withnames = fullitems
withnames['herocompare'].replace(herodict,inplace = True)
withnames['itemhero'].replace(herodict,inplace = True)
withnames['witem1'].replace(itemexport,inplace = True)
withnames['witem2'].replace(itemexport,inplace = True)
withnames['witem3'].replace(itemexport,inplace = True)
withnames['litem1'].replace(itemexport,inplace = True)
withnames['litem2'].replace(itemexport,inplace = True)
withnames['litem3'].replace(itemexport,inplace = True)
withnames.to_csv('filteredwinrateswithitemnamesnogem')