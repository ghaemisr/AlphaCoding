import math


class MinHeap:
    '''
    Child nodes are greater than or equal to parent nodes
    '''

    def __init__(self):
        self.data = []
        self.leaves = 0
        self.height = 0

    def pop(self):
        root = self.data[0]
        # move the last leaf to the root
        self.data[0] = self.data[len(self.data) - 1]
        self.data = self.data[:len(self.data) - 1]
        # perform bubble down, heap property
        current_index = 0
        while (True):
            # compare node to children
            left = (current_index * 2) + 1
            right = (current_index * 2) + 2
            # get smaller child
            smallest_child = None
            if (left > len(self.data) - 1):
                # case no left node exists, then no right node exists, heap is satisfied
                break
            elif (right > len(self.data) - 1):
                # case no right node exists, then left node is smallest
                smallest_child = left
            elif (self.data[left] > self.data[right]):
                smallest_child = right
            else:
                smallest_child = left

            # compare node to it's smallest child, and perform swap if needed
            if (self.data[current_index] > self.data[smallest_child]):
                # swap
                self.data[current_index], self.data[smallest_child] = self.data[smallest_child], self.data[
                    current_index]
                current_index = smallest_child
            else:
                break
        return root

    def insert(self, value):
        # place item at bottom left of heap
        self.data.append(value)
        index_inserted = len(self.data) - 1
        # fix heap property
        while (index_inserted != 0):
            # if the index is less than the parent, swap up
            parent = math.floor((index_inserted - 1) / 2)
            if (index_inserted != 0 and self.data[parent] >= self.data[index_inserted]):
                # swap
                self.data[parent], self.data[index_inserted] = self.data[index_inserted], self.data[parent]
                index_inserted = parent
            else:
                break

    def heapify(self, l):
        for i in range(0, len(l)):
            if (len(self.data) < 1):
                self.data.append(l[i])
            else:
                self.insert(l[i])

    def get_height(self):
        nodes = len(self.data)
        node_max = math.pow(2, 0)
        i = 1
        while (nodes > node_max):
            node_max += math.pow(2, i)
            i += 1
        return i

    def count_leaves(self):
        nodes = len(self.data)
        max_nodes = math.pow(2, 0)
        print(nodes, max_nodes)
        i = 1
        while (nodes > max_nodes):
            max_nodes += math.pow(2, i)
            i += 1
            print(nodes, max_nodes)
        max_nodes -= math.pow(2, i - 1)
        return int(nodes - max_nodes)


mheap = MinHeap()
x = [2, 7, 3, 1, 9, 44, 23]
print(x)
mheap.heapify(x)
print(mheap.data)
print(mheap.pop())
print(mheap.data)
print(mheap.count_leaves())
print(mheap.get_height())