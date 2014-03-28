# -*- coding: utf-8 -*-

import sys
from Queue import PriorityQueue
import heapq # Mitäs vittua? Tätä ei käytetä mihkään, mutta ilman sitä priorityqueue fukkaa.

class HuffmanNode():
    '''
    Class representing Huffman node.
    '''
    def __init__(self,weight=None,symbol=None,left_child=None,right_child=None,parent=None):
        self.weight = weight
        self.symbol = symbol
        self.left = left_child
        self.right = right_child
        self.parent = parent

    def get_weight(self):
        '''
        Returns weight of the nodes symbol.

        Returns:
            Integer
        '''
        return self.weight
    def get_symbol(self):
        '''
        Returns the symbol that the node contains.

        Returns:
            Byte
        '''
        return self.symbol
    def get_left_child(self):
        '''
        Returns nodes left child.

        Returns:
            HuffmanNode object
        '''
        return self.left
    def get_right_child(self):
        '''
        Returns nodes right child.

        Returns:
            HuffmanNode object
        '''
        return self.right
    def get_parent(self):
        '''
        Returns nodes parent node.

        Returns:
            HuffmanNode object
        '''
        return self.parent
    def set_weight(self,weight):
        '''
        Sets weight for the node.

        Args:
            weight: Integer
        '''
        self.weight = weight
    def set_symbol(self,symbol):
        '''
        Sets symbol for the node.

        Args:
            symbol: Bytecode.
        '''
        self.symbol = symbol
    def set_left_child(self,node):
        '''
        Sets given node as the left child.

        Args:
            node: HuffmanNode object.
        '''
        self.left = node
    def set_right_child(self,node):
        '''
        Sets given node as the right child.

        Args:
            node: HuffmanNode object.
        '''
        self.right = node
    def set_parent(self,node):
        '''
        Sets given node as the parent node.

        Args:
            node: HuffmanNode object.
        '''
        self.parent = node


def read_in_raw(filename, return_raw=False):
    '''
    Reads given non Huffman coded file as bytecode, and calculates weights for each byte.

    Args:
        filename: String, string representation of the inputfilename.
            Must include path to the file if not in the same directory as
            this script.

    Returns:
        PriorityQueue object containing Huffman nodes.
    '''
    # Read file, and calculate weights.
    tokenized = {}
    with open(filename, 'rb') as f:
        if return_raw:
            raw_string = f.read()
            return raw_string
        byte = f.read(1)
        while byte:
            if byte not in tokenized.keys():
                tokenized[byte] = 1
            else:
                tokenized[byte] += 1
            byte = f.read(1)

    print 'number of unique characters: %d'%len(tokenized.keys())
    # Create and populate priority queue with Huffman nodes
    queue = PriorityQueue()
    for key in tokenized.keys():
        weight = tokenized[key]
        node = HuffmanNode(weight=weight, symbol=key)
        queue.put((weight, node))

    return queue


def create_huffman_tree(filename):
    '''
    Encodes the given file to Huffman code.

    Args:
        filename: String, name of the file to be encoded.
        Must contain path to the file if the location differs
        from scripts location.
    Returns:
        PENDING
    '''
    queue = read_in_raw(filename)
    counter = 0
    while queue.qsize() > 1:
        left = queue.get()[1]
        right = queue.get()[1]
        weight = left.get_weight() + right.get_weight()
        node = HuffmanNode(weight=weight,
                            left_child=left,
                            right_child=right
                            )
        queue.put((weight,node))
        counter += 1

    root = queue.get()[1]

    return root

def iterate_tree(root, binary=''):
    symbols_and_binaries = []
    if root.get_left_child():
        symbols_and_binaries.extend(iterate_tree(root.get_left_child(),binary+'0'))
    if root.get_right_child():
        symbols_and_binaries.extend(iterate_tree(root.get_right_child(),binary+'1'))
    if root.get_symbol():
        print('Symbol: %s,      Huffman: %s,        weight: %d'%(root.get_symbol(),binary, root.get_weight()),)
        symbols_and_binaries.append((root.get_symbol(), binary))
    if symbols_and_binaries:
        return symbols_and_binaries
    
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if len(sys.argv) < 3:
        message = '''
        Invalid commandline arguments.

        Proper usage:
            python huffman.py -(option) input filename.

            Options:
                -e      Encode given file with Huffman compression.
                -d      Decode given file from Huffman compression.

            Input filename should contain path to file, if the
            files location differs from scripts location.
        '''
        sys.exit(message)
    else:
        option = sys.argv[1]
        filename = sys.argv[2]
        if option in '-e':
            # Encode flow here
            root = create_huffman_tree(filename)
            symbol_binary_dict = dict(iterate_tree(root))
            raw_string =  read_in_raw(filename, return_raw=True)
            encoded_string = ''.join(symbol_binary_dict[char] for char in raw_string)
            with open('output', 'wb') as textfile:
                textfile.write(encoded_string)
        elif option in '-d':
            # Decode flow here
            pass
        else:
            sys.exit('Invalid option: %s'%option)


if __name__ == '__main__':
    main()
