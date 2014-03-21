# -*- coding: utf-8 -*-

import sys

class HuffmanNode(object):
    '''
    Class representing Huffman node.
    '''
    def __init__(self, left_child=None, right_child=None, parent=None):
        '''
        Initializes Huffman node.

        Args:
            left_child: HuffmanNode object, optional.
            right_child: HuffmanNode object, optional.
            parent: HuffmanNode object, optional
        '''
        self.left =  left_child
        self.right = right_child
        self.parent = parent

    def set_left_child(node):
        '''
        Sets the given node as the left child.

        Args:
            node: HuffmanNode object.
        '''
        self.left = node

    def set_right_child(node):
        '''
        Sets the given node as the right child.

        Args:
            node: HuffmanNode object.
        '''
        self.right = node

    def set_parent(node):
        '''
        Sets the given node as the parent.

        Args:
            node: HuffmanNode object.
        '''
        self.parent = node

    def get_parent():
        '''
        Returns nodes parent.

        Returns:
            HuffmanNode object.
        '''
        return self.parent

    def get_left():
        '''
        Returns nodes left child.

        Returns:
            HuffmanNode object.
        '''
        return self.left

    def get_right():
        '''
        Returns nodes right child.

        Returns:
            HuffmanNode object.
        '''
        return self.right

    def get_children():
        '''
        Returns both children of the node.

        Returns:
            Instance method object.
        '''
        return((self.left, self,right))

def read_in(filename):
    '''
    Reads given file as bytecode, and calculates weights for each byte.

    Args:
        filename: String, string representation of the inputfilename.
            Must include path to the file if not in the same directory as
            this script.

    Returns:
        Dictionary. Keys are weights and data are bytes.
    '''

    # Read file, and calculate weights.
    tokenized = {}
    with open(filename, 'rb') as f:
        byte = f.read(1)
        while byte:
            if byte not in tokenized.keys():
                tokenized[byte] = 1
            else:
                tokenized[byte] += 1
            byte = f.read(1)

    # Invert tokenized, so that weights are keys.
    result = {}
    for k in tokenized.keys():
        result[tokenized[k]] = k
    del tokenized
    return result

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if len(sys.argv) < 3:
        message = '''
        Invalid commandline arguments.

        Proper usage:
            python huffman.py -(option) input/output filename.

            Options:
                -e      Encode given file with Huffman compression.
                -d      Decode given file from Huffman compression.

            Input/output filename should contain path to file,
            if the files location differs from scripts location.
        '''
        sys.exit(message)
    else:
        option = sys.argv[1]
        filename = sys.argv[2]
        if option is '-e':
            # Encode flow here
            pass
        elif option is '-d':
            # Decode flow here
            pass
        else:
            sys.exit('Invalid option: %s'%option)

    ##
    # Omaa testiä.
    ##
    left = HuffmanNode()
    right = HuffmanNode()
    root = HuffmanNode(left_child=left, right_child=right)
    ##
    # Testailut loppuu.
    ##



if __name__ == '__main__':
    main()
