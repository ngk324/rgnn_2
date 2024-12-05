from find_maximal_subgraphs import *
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

one_hop_num = 74
two_hop_num = 73

#f = open(rawpath + 'weights_A.txt', 'w')
num_previous_nodes = 0
for i in range(1,21):
    print(i)
    dir = '../weights/weights/' + str(i)
    num_n = int(num_nodes[i-1])
    filepath = rawpath + 'subgraphs_' + str(i) +'/'
    #print(filepath)
    os.makedirs(os.path.dirname(filepath),exist_ok=True)
    for core in range(num_n):
        print("Graph:",i,"Core:",core)
        #print(core)
        f = open(rawpath + 'subgraphs_' + str(i)+'/' + str(core)+'_subgraph.txt', 'w')
        one_hop_nbrs = set([core])
        one_hop_nbrs.update(find_1hop_neighbors(dir, core))
        two_hop_nbrs = find_2hop_neighbors(dir, core)
        two_hop_nbrs_alone = list(two_hop_nbrs)
       #print("\n1h nbrs",one_hop_nbrs)
        #print("\n2h nbrs", two_hop_nbrs_alone)

        two_hop_nbrs.update(one_hop_nbrs)
        two_hop_edges, _ = count_edges_in_subgraph(dir, two_hop_nbrs)
        two_hop_edges = list(two_hop_edges)
        two_hop_edges = sorted(two_hop_edges, key=lambda e: (e[0], e[1]))
        nodemap = {}
        nodes_sorted = list(two_hop_nbrs)
        nodes_sorted.sort()
        for j in range(len(nodes_sorted)):
            nodemap[nodes_sorted[j]] = j
        
        all_nodes = set(range(0,one_hop_num+two_hop_num))
        diff_nodes = all_nodes.symmetric_difference(two_hop_nbrs)
        diff_nodes_list=list(diff_nodes)
        #print(diff_nodes_list)
        #print("\n2h-1h diff nodes", diff_nodes)
        one_hop_nbrs = list(one_hop_nbrs)
        two_hop_nbrs = list(two_hop_nbrs)
        random_node_permutation = np.random.permutation(147)
        r = open(rawpath + 'subgraphs_' + str(i)+'/' + str(core)+'_mapping.txt', 'w')
        for node_n in random_node_permutation:
            r.write(str(node_n)+'\n')
        r.close()
        for edge in two_hop_edges:
            edge_start = nodemap[edge[0]]
            edge_end = nodemap[edge[1]]
            #edge_start = nodemap[edge[0]]
            #edge_end = nodemap[edge[1]]
            f.write(str(edge_start)+', '+str(edge_end)+'\n')
            f.write(str(edge_end)+', '+str(edge_start)+'\n')
        num_previous_nodes += len(two_hop_nbrs)
        f.close()

        one_two_hop_mapping = {core:0}
        counter = 1

        #print("1h len:",len(one_hop_nbrs))
        #print("2h len:",len(two_hop_nbrs_alone))
        for k in range(one_hop_num):
            if len(one_hop_nbrs) > k:
                if one_hop_nbrs[k] != core:
                    one_two_hop_mapping.update({one_hop_nbrs[k]:counter})
                    counter = counter + 1
            else:
                na_node = diff_nodes.pop()
                #print(na_node)
                one_two_hop_mapping.update({na_node:counter})
                counter = counter + 1


        for k in range(one_hop_num,two_hop_num+one_hop_num):
            val = k - one_hop_num
            if len(two_hop_nbrs_alone) > val:
                if two_hop_nbrs_alone[val] != core:
                    one_two_hop_mapping.update({two_hop_nbrs_alone[val]:counter})
                    counter = counter + 1
            else:
                na_node = diff_nodes.pop()
                one_two_hop_mapping.update({na_node:counter})
                counter = counter + 1

        one_two_hop_mapping = dict(sorted(one_two_hop_mapping.items()))
        m = open(rawpath + 'subgraphs_' + str(i)+'/' + str(core)+'_embedding_mapping.txt', 'w')
        for og_node,converted_node in one_two_hop_mapping.items():
            m.write(str(og_node) + ' ' + str(converted_node) + '\n')
        m.close()
        w = open(rawpath + 'subgraphs_' + str(i)+'/' + str(core)+'_embedding_weights.txt', 'w')
        a = open(rawpath + 'subgraphs_' + str(i)+'/' + str(core)+'_embedding.txt', 'w')
        
        for k in range(one_hop_num):
            true_node = k
            if len(one_hop_nbrs) > k:
                true_node = one_hop_nbrs[k]
            else:
                true_node = diff_nodes_list[k-len(one_hop_nbrs)]

            n1 = random_node_permutation[one_two_hop_mapping[true_node]]
            core1 = random_node_permutation[one_two_hop_mapping[core]]

            edge_exists = False

            if core != true_node:
                if core > true_node:
                    filepath = dir + '/' + str(i) + '_' + str(true_node) + '-' + str(core) + '.txt'
                    if os.path.exists(filepath):
                        edge_exists = True
                        with open(filepath) as g:
                            vals = [line.rstrip() for line in g]   
                            w.write(vals[1]+'\n' + vals[1]+'\n')
                            a.write(str(n1) + ', ' + str(core1) + '\n' + str(core1) + ', ' + str(n1) + '\n')

                else:
                    filepath = dir + '/' + str(i) + '_' + str(core) + '-' + str(true_node) + '.txt'
                    if os.path.exists(filepath):
                        edge_exists = True
                        with open(filepath) as g:
                            vals = [line.rstrip() for line in g]   
                            w.write(vals[1]+'\n' + vals[1]+'\n')
                            a.write(str(core1) + ', ' + str(n1) + '\n' + str(n1) + ', ' + str(core1) + '\n')
                
                if not edge_exists:
                    w.write(str(-10)+'\n'+str(-10)+'\n')
                    a.write(str(core1) + ', ' + str(n1) + '\n' + str(n1) + ', ' + str(core1) + '\n')

        #counter = 0
        for j in range(one_hop_num):
            for k in range(j+1,one_hop_num):
                edge_exists = False
                true_node1 = j
                true_node2 = k

                if len(one_hop_nbrs)  > j:
                    true_node1 = one_hop_nbrs[j]
                else:
                    true_node1 = diff_nodes_list[j-len(one_hop_nbrs)]

                if len(one_hop_nbrs)  > k:
                    true_node2 = one_hop_nbrs[k]
                else:
                    true_node2 = diff_nodes_list[k-len(one_hop_nbrs)]

            
                node1 = random_node_permutation[one_two_hop_mapping[true_node1]]
                node2 = random_node_permutation[one_two_hop_mapping[true_node2]]

                if core != true_node1 and core != true_node2:
                    if true_node1 > true_node2:
                        filepath = dir + '/' + str(i) + '_' + str(true_node2) + '-' + str(true_node1) + '.txt'
                        if os.path.exists(filepath):
                            edge_exists = True
                            with open(filepath) as g:
                                vals = [line.rstrip() for line in g]   
                                w.write(vals[1]+'\n' + vals[1]+'\n')
                                a.write(str(node2) + ', ' + str(node1) + '\n' + str(node1) + ', ' + str(node2) + '\n')


                    else:
                        filepath = dir + '/' + str(i) + '_' + str(true_node1) + '-' + str(true_node2) + '.txt'
                        if os.path.exists(filepath):
                            edge_exists = True
                            with open(filepath) as g:
                                vals = [line.rstrip() for line in g]   
                                w.write(vals[1]+'\n' + vals[1]+'\n')
                                a.write(str(node1) + ', ' + str(node2) + '\n' + str(node2) + ', ' + str(node1) + '\n')

                    if not edge_exists:
                        w.write(str(-10)+'\n'+str(-10)+'\n')
                        a.write(str(node1) + ', ' + str(node2) + '\n' + str(node2) + ', ' + str(node1) + '\n')
        
        for j in range(one_hop_num):
            for k in range(two_hop_num):
                edge_exists = False
                true_node1 = j
                true_node2 = k+one_hop_num

                if len(one_hop_nbrs) > j:
                    true_node1 = one_hop_nbrs[j]
                else:
                    true_node1 = diff_nodes_list[j-len(one_hop_nbrs)]

                if len(two_hop_nbrs_alone) > k:
                    true_node2 = two_hop_nbrs_alone[k]
                else:
                    true_node2 = diff_nodes_list[k-len(two_hop_nbrs_alone)+one_hop_num-len(one_hop_nbrs)]

            
                node1 = random_node_permutation[one_two_hop_mapping[true_node1]]
                node2 = random_node_permutation[one_two_hop_mapping[true_node2]]

                if core != true_node1 and core != true_node2:
                    if true_node1 > true_node2:
                        filepath = dir + '/' + str(i) + '_' + str(true_node2) + '-' + str(true_node1) + '.txt'
                        if os.path.exists(filepath):
                            edge_exists = True
                            with open(filepath) as g:
                                vals = [line.rstrip() for line in g]   
                                w.write(vals[1]+'\n' + vals[1]+'\n')
                                a.write(str(node2) + ', ' + str(node1) + '\n' + str(node1) + ', ' + str(node2) + '\n')


                    else:
                        filepath = dir + '/' + str(i) + '_' + str(true_node1) + '-' + str(true_node2) + '.txt'
                        if os.path.exists(filepath):
                            edge_exists = True
                            with open(filepath) as g:
                                vals = [line.rstrip() for line in g]   
                                w.write(vals[1]+'\n' + vals[1]+'\n')
                                a.write(str(node1) + ', ' + str(node2) + '\n' + str(node2) + ', ' + str(node1) + '\n')

                    if not edge_exists:
                        w.write(str(-10)+'\n'+str(-10)+'\n')
                        a.write(str(node1) + ', ' + str(node2) + '\n' + str(node2) + ', ' + str(node1) + '\n')



        for j in range(two_hop_num):
            for k in range(j+1,two_hop_num):
                edge_exists = False
                true_node1 = j+one_hop_num
                true_node2 = k+one_hop_num

                if len(two_hop_nbrs_alone) > j:
                    true_node1 = two_hop_nbrs_alone[j]
                else:
                    true_node1 = diff_nodes_list[j-len(two_hop_nbrs_alone)+one_hop_num-len(one_hop_nbrs)]

                if len(two_hop_nbrs_alone) > k:
                    true_node2 = two_hop_nbrs_alone[k]
                else:
                    true_node2 = diff_nodes_list[k-len(two_hop_nbrs_alone)+one_hop_num-len(one_hop_nbrs)]

            
                node1 = random_node_permutation[one_two_hop_mapping[true_node1]]
                node2 = random_node_permutation[one_two_hop_mapping[true_node2]]

                if core != true_node1 and core != true_node2:
                    if true_node1 > true_node2:
                        filepath = dir + '/' + str(i) + '_' + str(true_node2) + '-' + str(true_node1) + '.txt'
                        if os.path.exists(filepath):
                            edge_exists = True
                            with open(filepath) as g:
                                vals = [line.rstrip() for line in g]   
                                w.write(vals[1]+'\n' + vals[1]+'\n')
                                a.write(str(node2) + ', ' + str(node1) + '\n' + str(node1) + ', ' + str(node2) + '\n')


                    else:
                        filepath = dir + '/' + str(i) + '_' + str(true_node1) + '-' + str(true_node2) + '.txt'
                        if os.path.exists(filepath):
                            edge_exists = True
                            with open(filepath) as g:
                                vals = [line.rstrip() for line in g]   
                                w.write(vals[1]+'\n' + vals[1]+'\n')
                                a.write(str(node1) + ', ' + str(node2) + '\n' + str(node2) + ', ' + str(node1) + '\n')

                    if not edge_exists:
                        w.write(str(-10)+'\n'+str(-10)+'\n')
                        a.write(str(node1) + ', ' + str(node2) + '\n' + str(node2) + ', ' + str(node1) + '\n')
        #break
        w.close()
        a.close()
    #break
#f.close()











