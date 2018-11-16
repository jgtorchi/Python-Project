import unittest
import filecmp
from concordance import *

class TestList(unittest.TestCase):

    def test_01(self):
       conc = Concordance()
       conc.load_stop_table("stop_words.txt")
       conc.load_concordance_table("file1.txt")
       conc.write_concordance("file1_con.txt")
       self.assertTrue(filecmp.cmp("file1_con.txt", "file1_sol.txt"))

    def test_02(self):
       conc = Concordance()
       conc.load_stop_table("stop_words.txt")
       conc.load_concordance_table("file2.txt")
       conc.write_concordance("file2_con.txt")
       self.assertTrue(filecmp.cmp("file2_con.txt", "file2_sol.txt"))

    def test_03(self):
       conc = Concordance()
       conc.load_stop_table("stop_words.txt")
       conc.load_concordance_table("declaration.txt")
       conc.write_concordance("declaration_con.txt")
       self.assertTrue(filecmp.cmp("declaration_con.txt", "declaration_sol.txt"))

    def test_04(self):
        conc = Concordance()
        with self.assertRaises(FileNotFoundError):
            conc.load_stop_table("non_existent.txt")

    def test_05(self):
        with self.assertRaises(FileNotFoundError):
            conc = Concordance()
            conc.load_concordance_table("non_existent.txt")

    def test_06(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_index("cat"), 3)

        ht.insert("dog", 8)
        self.assertEqual(ht.get_num_items(), 2)
        self.assertEqual(ht.get_index("dog"), 6)
        self.assertAlmostEqual(ht.get_load_factor(), 2 / 7)

        ht.insert("mouse", 10)
        self.assertEqual(ht.get_num_items(), 3)
        self.assertEqual(ht.get_index("mouse"), 4)
        self.assertAlmostEqual(ht.get_load_factor(), 3 / 7)

        ht.insert("elephant", 12) # hash table should be resized
        self.assertEqual(ht.get_num_items(), 4)
        self.assertEqual(ht.get_table_size(), 15)
        self.assertAlmostEqual(ht.get_load_factor(), 4 / 15)
        self.assertEqual(ht.get_index("cat"), 12)
        self.assertEqual(ht.get_index("dog"), 14)
        self.assertEqual(ht.get_index("mouse"), 13)
        self.assertEqual(ht.get_index("elephant"), 9)
        keys = ht.get_all_keys()
        keys.sort()
        self.assertEqual(keys, ["cat", "dog", "elephant", "mouse"])
        self.assertFalse(ht.in_table("a"))

    def test_07(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        ht.insert("mou", 5)
        self.assertEqual(ht.get_index("mou"), 4)
        self.assertEqual(ht.get_value("mou"), [5])
        self.assertEqual(ht.in_table("mou"), True)

    def test_08(self):
        ht = HashTable(7)
        ht.insert("mou", 5)
        ht.insert("cat", 5)
        ht.insert("cat", 6)
        ht.insert("cat", 7)
        ht.insert("cat", 8)
        ht.insert("cat", 9)
        self.assertEqual(ht.get_index("cat"), 4)
        self.assertEqual(ht.get_value("cat"), [5,6,7,8,9])
        self.assertEqual(ht.get_value("apple"), None)
        self.assertEqual(ht.in_table("cat"), True)
        ht.insert("sar", 9)
        ht.insert("asdw", 9)
        ht.insert("rad", 9)
        self.assertEqual(ht.get_value("cat"), [5, 6, 7, 8, 9])

    def test_09(self):
       conc = Concordance()
       conc.load_stop_table("stop_words.txt")
       conc.load_concordance_table("War_And_Peace.txt")
       conc.write_concordance("War_And_Peace_con.txt")


if __name__ == '__main__':
   unittest.main()
