#!/usr/bin/env python3

import os
import sys
import struct

from io import StringIO
from random import SystemRandom
from collections import defaultdict


class Binary2EnglishDictionary(object):

    """ Encode/decode binary data to from an English dictionary """

    def __init__(self, master_dict, length_limit=8):
        """
        Reads in a master dictionary and ensures its long enough to encode any
        byte.
        """
        if not os.path.exists(master_dict) or not os.path.isfile(master_dict):
            raise ValueError("Master dictionary does not exist or is not file")
        with open(master_dict, "rb") as dictionary_file:
            self._dictionary_data = list(set(
                line.strip() for line in dictionary_file.readlines() if len(line) <= length_limit
            ))
        if len(self._dictionary_data) < 255:
            raise ValueError("Master dictionary is not long enough")

    def encode_file(self, input_file):
        """
        Encodes an input file of bytes using a randomized selection from the
        master dictionary.
        """
        SystemRandom().shuffle(self._dictionary_data)
        dictionary = self._dictionary_data[:256]
        output_file = StringIO()
        byte = input_file.read(1)
        while byte != '':
            output_file.write("%s " % self._encode_byte(byte, dictionary))
            byte = input_file.read(1)
        return output_file.getvalue(), dictionary

    def _encode_byte(self, byte, dictionary):
        """ Encodes a byte into a word using a given dictionary """
        index = int(byte.encode('hex'), 16)
        return dictionary[index]

    def decode_file(self, input_file, dictionary):
        """ Decode a file of words using a given dictionary back into bytes """
        output_file = StringIO()
        words = input_file.read().split()
        for word in words:
            byte = self._decode_byte(word, dictionary)
            output_file.write(byte)
        return output_file.getvalue()

    def _decode_byte(self, word, dictionary):
        """ Decodes a word into a byte using a given dictionary """
        index = dictionary.index(word)
        return struct.pack("B", index)


class Binary2DictlessEnglish(object):

    """
    Encodes data such that the decoder does not need the encoder's dictioary.
        a/k/a "Dictless mode"

    We have to use a larger encoder dictionary in this mode, so make sure you
    have lots of memory :)
    """

    def __init__(self, dictionary):
        """ Read in dictionary and compute indexes """
        self._random = SystemRandom()
        self._encoder_words = defaultdict(list)
        with open(dictionary, "rb") as fp:
            for line in fp:
                self._precompute_word(line.strip())
        self._check_encoder()

    def _check_encoder(self):
        """ Ensure we have at least one word for each index """
        for index in range(0, 256):
            if not len(self._encoder_words[index]):
                raise ValueError("Invalid encoder, no word(s) encode to %d" % (
                    index
                ))

    def _precompute_word(self, word):
        """ Builds a dictionary of words that compute to an index """
        index = self._word_sum(word.decode())
        self._encoder_words[index].append(word)

    def _word_sum(self, word):
        """ Sum of ASCII values modded by one byte """
        return sum(ord(char) for char in word) % 256

    def encode_file(self, input_file):
        """ Encodes all bytes in a file to words """
        output_file = StringIO()
        byte = input_file.read(1)
        while byte != b'':
            output_file.write("%s " % self._encode_byte(byte))
            byte = input_file.read(1)
        return output_file.getvalue()

    def decode_file(self, input_file):
        """ Decodes a file of words back into bytes """
        output_file = StringIO()
        words = input_file.read().split()
        for word in words:
            byte = self._decode_byte(word)
            output_file.write(byte)
        return output_file.getvalue().strip()

    def _encode_byte(self, byte):
        """ Takes a byte returns a word """
        index = int(byte.hex(), 16)
        return self._random.choice(self._encoder_words[index]).decode()

    def _decode_byte(self, word):
        """ Takes a word returns a byte """
        return struct.pack("B", self._word_sum(word))


if __name__ == "__main__":
    dictless_encoder = Binary2DictlessEnglish(sys.argv[1])
    with open(sys.argv[2], "rb") as fp:
        enc_data = dictless_encoder.encode_file(fp)
    with open("output.txt", "wb") as fp:
        fp.write(enc_data)
    with open("output.txt", "rb") as fp:
        dec_data = dictless_encoder.decode_file(fp)
    with open("file.orig", "wb") as fp:
        fp.write(dec_data)
