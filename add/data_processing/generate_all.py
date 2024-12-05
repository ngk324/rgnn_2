import numpy as np
import os 

def pause():
    programPause = input("Press the <ENTER> key to continue...")

with open('./num_nodes.txt') as f:
    num_nodes = [line.rstrip() for line in f]
f.close()

num_nodes = num_nodes[:20]

rawpath = '../weights/raw/'
if not os.path.exists(rawpath):
    os.makedirs(rawpath)

num_prev = 0
f = open(rawpath + 'weights_A.txt', 'w')
e = open(rawpath + 'weights_edge_labels.txt', 'w')
nl = open(rawpath + 'weights_node_labels.txt', 'w')
gi = open(rawpath + 'weights_graph_indicator.txt', 'w')
gl = open(rawpath + 'weights_graph_labels.txt', 'w')


num_previous_nodes = 0
graph_counter = 1
for i in range(1,21):
    print(i)
    #f = open(rawpath + 'subgraph_' + str(i) txt', 'w')
    dir = '../weights/raw/subgraphs_' + str(i) +'/'
    num_n = int(num_nodes[i-1])
    for core in range(num_n):
        with open(dir + str(core) + '_' + 'embedding_weights.txt') as g:
            w = [line.rstrip() for line in g]
        g.close()

        with open(dir + str(core) + '_' + 'embedding.txt') as g:
            adj = [tuple(map(int, line.rstrip().split(','))) for line in g]
        g.close()

        if (i != 1 and core != 0) or (i == 1 and core > 0) or (i != 1):
            gl.write('\n')
            #nl.write('\n')


        print(core,len(adj))
        for k in range(len(adj)):
            # makes weights_A and edge_labels
            edge_start = adj[k][0] + num_prev
            edge_end = adj[k][1] + num_prev
            if (i != 20 and core != num_n - 1) or (i == 20 and core < num_n):
                f.write(str(edge_start)+', '+str(edge_end)+'\n')
                e.write(str(w[k])+'\n')
            elif (i == 20 and core == num_n - 1) :
                f.write(str(edge_start)+', '+str(edge_end))
                e.write(str(w[k]))

            #if k % 2 == 0 and k != len(adj) - 2:
            #    gl.write(str(w[k]) + ', ')
            #elif k % 2 == 0 and k == len(adj) - 2:
            #    gl.write(str(w[k]))

        for k in range(74):
            if k < 73:
                gl.write(str(w[k*2]) + ', ')
            else:
                gl.write(str(w[k*2]))


            


        for k in range(147):
            nl.write('\n')
            for l in range(147):
                if l < 73:
                    nl.write(str(w[l*2])+',')
                    #gl.write(str(w[k*2]) + ', ')
                elif l == 73: 
                    nl.write(str(w[l*2]))
                    #gl.write(str(w[k*2]))
            gi.write(str(graph_counter)+'\n')

        num_prev += 147
        graph_counter += 1
        
        #if core == 10:
        #    break
    #break

nl.close()
gi.close()
gl.close()
e.close()
f.close()
