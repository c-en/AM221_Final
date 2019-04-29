
# coding: utf-8

# In[2]:


import gurobipy as gb
import numpy as np
import csv


# In[3]:


NUMDISTRICTS = 9
NUMTOWNS = 351

# basic voter data as numpy arrays - POPULATION, DEMOCRATS, REPUBLICANS, INDEPENDENTS
# each town is assigned an index in the idx dict; e.g. to get index of BEDFORD use idx['BEDFORD']
# to get population of BEDFORD use POP[idx['BEDFORD']]
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
with open ('Adjacencies_Fixed.csv', 'r') as adjfile:
    adjreader = csv.reader(adjfile, delimiter=',')
    ADJ = np.zeros((i,i))
    for row in adjreader:
        i1 = idx[row[0]]
        for t2 in row[1:]:
            if not t2 == '':
                ADJ[i1][idx[t2]] = 1


# In[62]:


# init model
m = gb.Model()

# min and max population for each district
MINPOP = 720000
MAXPOP = 735000

# big-M (for population of state)
M = 10**6

# total number of voters
VOTERS=sum(REPS)+sum(DEMS)

# init variables
# Dwin_i - whether D wins district i (0/1)
# Rwin_i - whether R wins district i (0/1)
# Ddiff_i - D wasted votes minus R wasted votes in district i (free variable)
# y - variable for removing abs. value from objective (pos float)
# z_t^i - if town t in district i (0/1)

Dwin = []
for i in range(NUMDISTRICTS):
    Dwin.append(m.addVar(name='Dwin'+str(i), vtype=gb.GRB.BINARY))
    
Rwin = []
for i in range(NUMDISTRICTS):
    Rwin.append(m.addVar(name='Rwin'+str(i), vtype=gb.GRB.BINARY))
    
Ddiff = []
for i in range(NUMDISTRICTS):
    Ddiff.append(m.addVar(name='Ddiff'+str(i), lb=-1e31))
    
y = m.addVar(name='y')

z = [[] for t in range(len(idx))]
for t, zt in enumerate(z):
    for i in range(NUMDISTRICTS):
        zt.append(m.addVar(name='z_'+str(t)+'('+str(i)+')', vtype=gb.GRB.BINARY))    

        
# f_ij - amount of flow from town i to town j (pos float)
# sink_t - whether district 0 has a sink at town t (0/1)
f = [[] for t in range(NUMTOWNS)]
for t, ft in enumerate(f):
    for i in range(NUMTOWNS):
        ft.append(m.addVar(name='f_'+str(t)+'('+str(i)+')'))

sink = []
for i in range(NUMTOWNS):
    sink.append(m.addVar(name='sink'+str(i), vtype=gb.GRB.BINARY))
                  
m.update()

# init constraints
# each town is in exactly one district
# sum_i z_t^i = 1
for t in range(len(TOWNS)):
    m.addConstr(sum(z[t]), sense=gb.GRB.EQUAL, rhs=1., name='towndist'+str(t))
    
# district population constraint:
# MINPOP <= sum_t z_t^i * POP_i <= MAXPOP for all districts i
for i in range(NUMDISTRICTS):
    m.addConstr(sum([z[t][i]*POP[t] for t in range(len(TOWNS))]), sense=gb.GRB.LESS_EQUAL, rhs=MAXPOP, name='maxpop'+str(i))
    m.addConstr(sum([z[t][i]*POP[t] for t in range(len(TOWNS))]), sense=gb.GRB.GREATER_EQUAL, rhs=MINPOP, name='minpop'+str(i))    
    
# constraints to define Dwin and Rwin
for i in range(NUMDISTRICTS):
    m.addConstr(Dwin[i]+Rwin[i], sense=gb.GRB.EQUAL, rhs=1., name='onewins'+str(i))
    m.addConstr(sum([z[t][i]*(DEMS[t]-REPS[t]) for t in range(len(TOWNS))])-M*Dwin[i], sense=gb.GRB.LESS_EQUAL, rhs=0., name='checkDwins'+str(i))
    m.addConstr(sum([z[t][i]*(REPS[t]-DEMS[t]) for t in range(len(TOWNS))])-M*Rwin[i], sense=gb.GRB.LESS_EQUAL, rhs=0., name='checkRwins'+str(i))

# constraints to find number of wasted votes
for i in range(NUMDISTRICTS):
    m.addConstr(sum([z[t][i]*(DEMS[t]-3*REPS[t]) for t in range(len(TOWNS))])/2+2*M*Rwin[i]-Ddiff[i], sense=gb.GRB.GREATER_EQUAL, rhs=0., name='wastedgap1'+str(i))
    m.addConstr(sum([z[t][i]*(DEMS[t]-3*REPS[t]) for t in range(len(TOWNS))])/2-2*M*Rwin[i]-Ddiff[i], sense=gb.GRB.LESS_EQUAL, rhs=0., name='wastedgap2'+str(i))
    m.addConstr(sum([z[t][i]*(3*DEMS[t]-REPS[t]) for t in range(len(TOWNS))])/2+2*M*Dwin[i]-Ddiff[i], sense=gb.GRB.GREATER_EQUAL, rhs=0., name='wastedgap3'+str(i))
    m.addConstr(sum([z[t][i]*(3*DEMS[t]-REPS[t]) for t in range(len(TOWNS))])/2-2*M*Dwin[i]-Ddiff[i], sense=gb.GRB.LESS_EQUAL, rhs=0., name='wastedgap4'+str(i))

# constraints to find z (efficiency gap in # of votes)
m.addConstr(sum(Ddiff)-y, sense=gb.GRB.LESS_EQUAL, rhs=0., name='Egap1')
m.addConstr(-sum(Ddiff)-y, sense=gb.GRB.LESS_EQUAL, rhs=0., name='Egap2')


# Force district 1 to be contiguous using flow
# Only one sink and it must be in district 1
m.addConstr(sum(sink), sense=gb.GRB.EQUAL, rhs=1, name='onesink')

for t in range(NUMTOWNS):
    m.addConstr(sink[t]-z[t][0], sense=gb.GRB.LESS_EQUAL, rhs=0, name='sinkdistrict'+str(t))
    
# No flow from outside region and inflow does not exceeed M-1 (big-M = most towns in a district = NUMTOWNS)
for t in range(NUMTOWNS):
    m.addConstr(sum([f[t][t2] for t2 in np.where(ADJ[t]==1)[0]])+(1-NUMTOWNS)*z[t][0], sense=gb.GRB.LESS_EQUAL, rhs=0., name='flow'+str(t))

# Net outflow
for t in range(NUMTOWNS):
    m.addConstr(sum([f[t][t2] for t2 in np.where(ADJ[t]==1)[0]])-sum([f[t3][t] for t3 in np.where(ADJ[t]==1)[0]])-z[t][0]+NUMTOWNS*sink[t], sense=gb.GRB.GREATER_EQUAL, rhs=0., name='flowconstraint'+str(t))


m.update()


# objective
print('INITIALIZING OBJECTIVE')
# min y/sum_i(r_i+d_i) (towns i)
m.update()
m.setObjective(y/VOTERS, gb.GRB.MINIMIZE)
print('SOLVING')
m.optimize()


# In[61]:


# Code for looking at some results

#print([ri.x for ri in r]) # Print values of r
print(Ddiff) # Print wasted vote differences in each district
print(y)
demarray=np.zeros(9)
reparray=np.zeros(9)
poparray=np.zeros(9)
for i in range(NUMDISTRICTS):
    for t in range(len(TOWNS)):
        demarray[i]+=z[t][i].x*DEMS[t]
for i in range(NUMDISTRICTS):
    for t in range(len(TOWNS)):
        reparray[i]+=z[t][i].x*REPS[t]
for i in range(NUMDISTRICTS):
    for t in range(len(TOWNS)):
        poparray[i]+=z[t][i].x*POP[t]
print(demarray) # Print number of Democrats in each district
print(reparray) # Print number of Republicans in each district
print(poparray)
print(sum(REPS)+sum(DEMS))

# Print names of towns in each district
for number in range(9):
    print(number+1)
    district=np.zeros(351)
    for i in range(351):
        district[i]=z[i][number].x
    print(district) # Print vector indicating which towns are in district "number+1"
    for i in range(351):
        if district[i]==1:
            print(("'"+str(TOWNS[i])+"',").strip()) # Print list of towns in district "number+1"
            
    

        


# In[57]:


sinkarray=np.zeros(351)
for i in range(NUMTOWNS):
    sinkarray[i]=sink[i].x
    if sink[i].x>0:
        print(i)

print([ri.x for ri in [f[t][77] for t in np.where(ADJ[77]==1)[0]]])
print([TOWNS[t] for t in np.where(ADJ[77]==1)[0]])

print([ri.x for ri in [f[t][84] for t in np.where(ADJ[84]==1)[0]]])
print([TOWNS[t] for t in np.where(ADJ[84]==1)[0]])


print(sinkarray)
print(TOWNS[77])

print([ri.x for ri in z[77]])
print(sink[77].x)
print(sink[77].x>=np.array([ri.x for ri in z[77]]))

TOWNS=np.array(TOWNS)
np.where(TOWNS=='HAVERHILL')


# In[100]:


ADJ[0][1]
a=2*np.arange(20)
a[np.where(ADJ[0]==1)[0]]
type(f[0])
#f[0][np.where(ADJ[0]==1)[0].astype(int)]


sum(np.asarray(f)[0][np.where(ADJ[0]==1)])
sum([f[0][j] for j in np.where(ADJ[0]==1)[0]])
#ADJ[0][np.where(ADJ[0]==1)]

#sum([f[0][j] for j in np.where(ADJ[0]==1)])
#sum([f[0][j] for j in np.where(ADJ[0][j]==1)])


# In[89]:


sum(f[0][8:11])


# In[96]:


sum([a[j] for j in np.where(ADJ[0]==1)[0]])


# In[9]:


t=15
sum([f[t][j] for j in np.where(ADJ[t]==1)[0]])


# In[155]:


[TOWNS[j] for j in np.where(sum(ADJ!=np.transpose(ADJ)))[0]]


# In[8]:


sum([f[t3][t] for t3 in np.where(ADJ[t]==1)[0]])

