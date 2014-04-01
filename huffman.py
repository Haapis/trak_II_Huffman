# -*- coding: utf-8 -*-

import sys
from Queue import PriorityQueue
from array import *
import heapq 
import pickle

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
        return_raw (optional): Boolean, if true, return the raw input

    Returns:
        PriorityQueue object containing Huffman nodes.
        If return_raw is true, return the raw input from input file
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
    pickle.dump(root, open('tree', 'wb'))
    return root

# Assigns binary representations to symbols and returns a list of tuples containing assigned values
def iterate_tree(root, binary=''):
    symbols_and_binaries = []
    if root.get_left_child():
        symbols_and_binaries.extend(iterate_tree(root.get_left_child(),binary+'0'))
    if root.get_right_child():
        symbols_and_binaries.extend(iterate_tree(root.get_right_child(),binary+'1'))
    if root.get_symbol():
        # print('Symbol: %s,      Huffman: %s,        weight: %d'%(root.get_symbol(),binary, root.get_weight()),)
        symbols_and_binaries.append((root.get_symbol(), binary))
    if symbols_and_binaries:
        return symbols_and_binaries

def encode(huffman_alphabet, input_filename):
    '''
    Compresses file with huffman compression. File to be compressed is defined by input_filename

    Args:
        huffman_alphabet: Dict, contains huffman coding for each symbol. (from input file)
        input_filename: String, defines which file is to be compressed. If file is in different
            directory, filename should also contain path to the file.
    '''
    binary_string = ''
    with open(input_filename, 'rb') as f:
        byte = f.read(1)
        while byte:
            binary_string += huffman_alphabet[byte]
            byte = f.read(1)
    
    outfile = input_filename+'.huff'
    #bytearray = bytearray(binary_string)
    with open(outfile, 'wb') as out:
        byte_array = array('B')
        low = 0
        high = 8
        while True:
            if(high<len(binary_string)):
                byte_array.append(int(binary_string[low:high],2))
                low = high
                high += 8
            else:
                byte_array.append(int(binary_string[low:],2))
                break
        byte_array.tofile(out)
            

def decode(root, input_file):
    outfile = input_file[:-5]
    inf = open(input_file, 'rb')
    binary = inf.read()
    inf.close()
    decoded = ''
    node = root
    for byte in binary:
        byte = bin(ord(byte))[2:].rjust(8, '0')
        for bit in byte:
            if bit == '0':
                node = node.get_left_child()
            else:
                node = node.get_right_child()

            symbol = node.get_symbol()
            if symbol:
                decoded += symbol
                node = root
    


    with open(outfile, 'wb') as out:
        out.write(decoded)
    # decoded_string = ''.join(decoded_chars)
    # return decoded_string
    
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
            huffman_alphabet = dict(iterate_tree(root))
            encode(huffman_alphabet, filename)
        elif option in '-d':
            # Decode flow here
            root = pickle.load(open('tree', 'rb'))
            decode(root, filename)
        else:
            sys.exit('Invalid option: %s'%option)

if __name__ == '__main__':
    main()
