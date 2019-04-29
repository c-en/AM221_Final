
# coding: utf-8

# In[6]:


import gurobipy as gb
import numpy as np
import csv


# In[7]:


NUMDISTRICTS = 9

# basic voter data as numpy arrays - POPULATION, DEMOCRATS, REPUBLICANS, INDEPENDENTS
# each town is assigned an index in the idx dict; e.g. to get index of BEDFORD use idx['BEDFORD']
# e.g. to get population of BEDFORD use POP[idx['BEDFORD']]
with open("Voter_Data_MA_CSV_Version_2.csv", 'r') as votefile:
    votereader = csv.reader(votefile, delimiter=',')
    next(votereader)
    TOWNS = []
    POP = []
    DEMS = []
    REPS = []
    INDS = []
    idx = {}
    i = 0
    for row in votereader:
        town = row[0]
        TOWNS.append(town)
        idx[town] = i
        i += 1
        POP.append(int(row[-1]))
        DEMS.append(int(row[-3]))
        REPS.append(int(row[-2]))
        INDS.append(POP[-1] - DEMS[-1] - REPS[-1])
    POP = np.array(POP)
    DEMS = np.array(DEMS)
    REPS = np.array(REPS)
    INDS = np.array(INDS)

# pairwise distance data, as a numpy array
# use idx dict to get indices
with open("dist_pairs.csv", 'r') as distfile:
    # pairwise dist
    distreader = csv.reader(distfile, delimiter=',')
    DIST = np.zeros((i,i))
    for row in distreader:
        DIST[idx[row[0]]][idx[row[1]]] = float(row[-1])

# pairwise adjacency matrix (1/0 for adjacent/not adj)
# use idx dict to get indices
with open ('Adjacencies.csv', 'r') as adjfile:
    adjreader = csv.reader(adjfile, delimiter=',')
    ADJ = np.zeros((i,i))
    for row in adjreader:
        i1 = idx[row[0]]
        for t2 in row[1:]:
            if not t2 == '':
                ADJ[i1][idx[t2]] = 1


# In[8]:


# calculate adjusted vote distributions so that each party has 50% vote share
TOTAL_DEMS = float(sum(DEMS))
TOTAL_REPS = float(sum(REPS))
TOTAL_INDS = float(sum(INDS))
TOTAL_POP = sum(POP)
p = (TOTAL_REPS + TOTAL_INDS - TOTAL_DEMS)/(2*TOTAL_INDS)
ADJUSTED_DEMS = (DEMS + p * INDS).astype(int)
ADJUSTED_REPS = (REPS + (1-p) * INDS).astype(int)


# In[4]:


# init model
m = gb.Model()

# big-M (for population of state)
M = 10**6

# coeff of radius term in objective
l = 10**(-4)

# min and max population for each district
MINPOP = 720000
MAXPOP = 735000

# init variables
print('INITIALIZING VARIABLES')
# dw_i - if democrat wins district i (0/1)
# rw_i - if republican wins district i (0/1)
# PB - positive difference between D and R
# z_t^i - if town t in district i (0/1)
# r_i - max dist between towns in district i, 0<=i<=9 (pos float)
PB = m.addVar(name='PB', vtype=gb.GRB.INTEGER)
z = [[] for t in range(len(idx))]
for t, zt in enumerate(z):
    for i in range(NUMDISTRICTS):
        zt.append(m.addVar(name='z_'+str(t)+'('+str(i)+')', vtype=gb.GRB.BINARY))    
r = []
dw = []
rw = []
for i in range(NUMDISTRICTS):
    r.append(m.addVar(name='r'+str(i)))
    dw.append(m.addVar(name='dw'+str(i), vtype=gb.GRB.BINARY))
    rw.append(m.addVar(name='rw'+str(i), vtype=gb.GRB.BINARY))
m.update()

# init constraints
print('INITIALIZING CONSTRAINTS')
# each town is in exactly one district
# sum_i z_t^i = 1
for t in range(len(TOWNS)):
    m.addConstr(sum(z[t]), sense=gb.GRB.EQUAL, rhs=1., name='towndist'+str(t))
    
# constraints to show which party won a district
# dw_i + rw_i = 1 for all district i
# M * dw_i - sum_t(z_t^i*(DEMS_i - REPS_i)) >= 0
# M * rw_i - sum_t(z_t^i*(REPS_i - DEMS_i)) > 0
for i in range(NUMDISTRICTS):
    m.addConstr(dw[i] + rw[i], sense=gb.GRB.EQUAL, rhs=1., name='onewinner'+str(i))
    m.addConstr(M*dw[i] - sum([z[t][i]*(ADJUSTED_DEMS[t] - ADJUSTED_REPS[t]) for t in range(len(TOWNS))]), sense=gb.GRB.GREATER_EQUAL, rhs=0., name='demwin'+str(i))
    m.addConstr(M*rw[i] - sum([z[t][i]*(ADJUSTED_REPS[t] - ADJUSTED_DEMS[t]) for t in range(len(TOWNS))]), sense=gb.GRB.GREATER_EQUAL, rhs=0., name='repwin'+str(i))

# count number of dem/rep districts, and partisan bias
# PB >= D-R, PB >= R-D
m.addConstr(PB - sum(dw) + sum(rw), sense=gb.GRB.GREATER_EQUAL, rhs=0., name='PB1')
m.addConstr(PB - sum(rw) + sum(dw), sense=gb.GRB.GREATER_EQUAL, rhs=0., name='PB2')
    
# diameter r_i of a district is greater than every pairwise distance between towns in the district
# r_i >= dist_st * (z_s^i + z_t^i - 1) for all districts i, towns s t
for i in range(NUMDISTRICTS):
    for s in range(len(TOWNS)):
        for t in range(len(TOWNS)):
            m.addConstr(r[i] - DIST[s][t] * (z[s][i] + z[t][i] - 1.), sense=gb.GRB.GREATER_EQUAL, rhs=0., name="r"+str(i)+'_'+str(s)+'-'+str(t))
            
# district population constraint:
# MINPOP <= sum_t z_t^i * POP_i <= MAXPOP for all districts i
for i in range(NUMDISTRICTS):
    m.addConstr(sum([z[t][i]*POP[t] for t in range(len(TOWNS))]), sense=gb.GRB.LESS_EQUAL, rhs=MAXPOP, name='maxpop'+str(i))
    m.addConstr(sum([z[t][i]*POP[t] for t in range(len(TOWNS))]), sense=gb.GRB.GREATER_EQUAL, rhs=MINPOP, name='minpop'+str(i))
    
# objective
print('INITIALIZING OBJECTIVE')
# min PB + sum_i r_i (districts i)
m.update()
m.setObjective(PB + l*sum(r), gb.GRB.MINIMIZE)
print('SOLVING')
m.optimize()


# In[6]:


print([ri.x for ri in r])
print(sum([ri.x for ri in r]) * 10**(-4))


# In[2]:


with open("PB_testrun.csv", 'w') as f:
    dwriter = csv.writer(f, delimiter=',')
    for i in range(NUMDISTRICTS):
        towns = []
        for t in range(len(TOWNS)):
            if z[t][i].x == 1:
                towns.append(TOWNS[t])
        print('********************************')
        print('DISTRICT '+str(i))
        print(towns)
        dwriter.writerow(towns)





