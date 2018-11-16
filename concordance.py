from hash_quad import *
import string

class Concordance:

    def __init__(self):
        self.stop_table = None          # hash table for stop words
        self.concordance_table = None   # hash table for concordance

    def load_stop_table(self, filename):
        """ Read stop words from input file (filename) and insert each word as a key into the stop words hash table.
        Starting size of hash table should be 191: self.stop_table = HashTable(191)
        If file does not exist, raise FileNotFoundError"""
        self.stop_table = HashTable(191)
        try:
            read_file = open(filename, 'r')
        except FileNotFoundError:
            raise FileNotFoundError
        for line in read_file:
            if line[len(line) - 1:] == '\n':
                line = line[:len(line) - 1]
            self.stop_table.insert(line, 0)
        read_file.close()

    def load_concordance_table(self, filename):
        """ Read words from input text file (filename) and insert them into the concordance hash table, 
        after processing for punctuation, numbers and filtering out words that are in the stop words hash table.
        Do not include duplicate line numbers (word appearing on same line more than once, just one entry for that line)
        Starting size of hash table should be 191: self.concordance_table = HashTable(191)
        If file does not exist, raise FileNotFoundError"""
        self.concordance_table = HashTable(191)
        try:
            read_file = open(filename, 'r')
        except FileNotFoundError:
            raise FileNotFoundError
        i = 0
        for line in read_file:
            i += 1
            word = ''
            words_found_in_line = []
            for x in range(0,len(line)):
                if (97 <= ord(line[x]) <= 122) or (65 <= ord(line[x]) <= 90):
                    word += line[x]
                elif ord(line[x]) == 39:
                    pass
                else:
                    if (len(word) > 0) and (not(self.stop_table.in_table(word.lower()))) and (not(word.lower() in words_found_in_line)):
                        self.concordance_table.insert(word.lower(), i)
                        words_found_in_line.append(word.lower())
                    word = ''
        read_file.close()

    def write_concordance(self, filename):
        """ Write the concordance entries to the output file(filename)
        See sample output files for format."""
        key_list = self.concordance_table.get_all_keys()
        key_list.sort()
        write_text = ''
        for x in range(0,len(key_list)):
            values = self.concordance_table.get_value(key_list[x])
            values_str = ''
            for y in range(0, len(values)):
                values_str += str(values[y]) + ' '
            write_text += key_list[x] + ': ' + values_str[:len(values_str) - 1] + '\n'
        write_text = write_text[:len(write_text) - 1]
        write_file = open(filename, 'w')
        write_file.write(write_text)
        write_file.close()
