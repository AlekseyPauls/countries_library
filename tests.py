# -*- coding: utf-8 -*-
import unittest
from countries_lib.country import normalize_country_name, match_country_name, del_country_name


class NormalizeCountryNameTestCase(unittest.TestCase):

    def test_simple_name(self):
        self.assertEqual(normalize_country_name('Russia'), 'Russia')

    def test_punctuation_sensitivity(self):
        self.assertEqual(normalize_country_name('Russia!!!:)'), 'Russia')

    def test_upper_register(self):
        self.assertEqual(normalize_country_name('RUSSIA'), 'Russia')

    def test_low_register(self):
        self.assertEqual(normalize_country_name('russia'), 'Russia')

    def test_missed_letter(self):
        self.assertEqual(normalize_country_name('Rusia'), 'Russia')

    def test_excess_letter(self):
        self.assertEqual(normalize_country_name('Russiaa'), 'Russia')

    def test_another_letter(self):
        self.assertEqual(normalize_country_name('Rassia'), 'Russia')

    def test_simple_two_words_name(self):
        self.assertEqual(normalize_country_name('Russian Federation'), 'Russia')

    def test_excess_word_name(self):
        self.assertEqual(normalize_country_name('The Russia'), 'Russia')

    def test_american_paris_like_construction(self):
        self.assertEqual(normalize_country_name('Paris, USA'), 'United States')

    def test_standard_accuracy_result(self):
        self.assertEqual(normalize_country_name('azazaza'), 'None')

    def test_correct_accuracy_type(self):
        self.assertEqual(normalize_country_name('Russia', 0.9), 'Russia')

    def test_incorrect_accuracy_type(self):
        self.assertEqual(normalize_country_name('Russia', '0.7'), 'Invalid argument type')
        self.assertEqual(normalize_country_name('Russia', []), 'Invalid argument type')

    def test_incorrect_accuracy_value(self):
        self.assertEqual(normalize_country_name('Russia', 3.0), 'Invalid argument type')
        self.assertEqual(normalize_country_name('Russia', -0.5), 'Invalid argument type')


class MatchAndDelCountryNameTestCase(unittest.TestCase):

    def test_non_existing_object_delete(self):
            del_country_name('SpecialNameForTest')
            self.assertEqual(normalize_country_name('SpecialNameForTest'), 'None')

    def test_match(self):
            match_country_name('SpecialNameForTest', 'SpecialNameForTest')
            self.assertEqual(normalize_country_name('SpecialNameForTest'), 'SpecialNameForTest')

    def test_existing_object_delete(self):
            del_country_name('SpecialNameForTest')
            self.assertEqual(normalize_country_name('SpecialNameForTest'), 'None')

    def test_correct_priority_match(self):
            match_country_name('SpecialNameForTest', 'SpecialNameForTest', 1)
            self.assertEqual(normalize_country_name('SpecialNameForTest'), 'SpecialNameForTest')
            del_country_name('SpecialNameForTest')

    def test_incorrect_priority_match(self):
        self.assertEqual(match_country_name('SpecialNameForTest', 'SpecialNameForTest', 3), 'Invalid argument type')
        self.assertEqual(match_country_name('SpecialNameForTest', 'SpecialNameForTest', -5), 'Invalid argument type')
        self.assertEqual(match_country_name('SpecialNameForTest', 'SpecialNameForTest', 1.2), 'Invalid argument type')
        self.assertEqual(match_country_name('SpecialNameForTest', 'SpecialNameForTest', '1'), 'Invalid argument type')
        self.assertEqual(match_country_name('SpecialNameForTest', 'SpecialNameForTest', []), 'Invalid argument type')

    def test_incorrect_match(self):
        self.assertEqual(match_country_name(1, 'SpecialNameForTest'), 'Invalid argument type')
        self.assertEqual(match_country_name('SpecialNameForTest', 1), 'Invalid argument type')
        self.assertEqual(match_country_name([], 'SpecialNameForTest'), 'Invalid argument type')
        self.assertEqual(match_country_name('SpecialNameForTest', []), 'Invalid argument type')

    def test_incorrect_delete(self):
        self.assertEqual(del_country_name(1), 'Invalid argument type')
        self.assertEqual(del_country_name(1.5), 'Invalid argument type')
        self.assertEqual(del_country_name([]), 'Invalid argument type')


if __name__ == '__main__':
    unittest.main()
