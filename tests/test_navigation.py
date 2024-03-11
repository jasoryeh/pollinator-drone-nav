import unittest

import pollinator.navigation as nav

class TestNavigation(unittest.TestCase):

    def test_nav_coordinate1(self):
        w = 1000
        h = 1000
        # bottom right
        horiz, vert = nav.calculate_move_coordinate((w, h), ((w / 2) + 1, (h / 2) + 1))
        self.assertLess(horiz, 0)
        self.assertLess(vert, 0)
        self.assertEqual(horiz, -1)
        self.assertEqual(vert, -1)

    def test_nav_coordinate2(self):
        w = 1000
        h = 1000
        # bottom left
        horiz, vert = nav.calculate_move_coordinate((w, h), ((w / 2) - 1, (h / 2) + 1))
        self.assertGreater(horiz, 0)
        self.assertLess(vert, 0)
        self.assertEqual(horiz, 1)
        self.assertEqual(vert, -1)

    def test_nav_coordinate3(self):
        w = 1000
        h = 1000
        horiz, vert = nav.calculate_move_coordinate((w, h), ((w / 2) - 1, (h / 2) - 1))
        self.assertGreater(horiz, 0)
        self.assertGreater(vert, 0)
        self.assertEqual(horiz, 1)
        self.assertEqual(vert, 1)

    def test_nav_coordinate4(self):
        w = 1000
        h = 1000
        horiz, vert = nav.calculate_move_coordinate((w, h), ((w / 2) + 1, (h / 2) - 1))
        self.assertLess(horiz, 0)
        self.assertGreater(vert, 0)
        self.assertEqual(horiz, -1)
        self.assertEqual(vert, 1)

    def test_nav_coordinate5(self):
        w = 1000
        h = 1000
        horiz, vert = nav.calculate_move_coordinate((w, h), ((w / 2), (h / 2)))
        self.assertEqual(horiz, 0)
        self.assertEqual(vert, 0)
        self.assertEqual(horiz, 0)
        self.assertEqual(vert, 0)

    def test_nav_bounds1(self):
        w = 1000
        h = 1000
        # for a item detected at bottom left
        horiz, vert = nav.calculate_move_bounds((w, h), (556, 600, 987, 700))
        self.assertLess(horiz, 0)
        self.assertLess(vert, 0)
        self.assertEqual(horiz, 500 - (556 + ((987 - 556) / 2)))
        self.assertEqual(vert, 500 - (600 + ((700 - 600) / 2)))

    def test_nav_bounds2(self):
        w = 1000
        h = 1000
        # for a item detected at bottom right
        horiz, vert = nav.calculate_move_bounds((w, h), (34, 678, 345, 700))
        self.assertGreater(horiz, 0)
        self.assertLess(vert, 0)
        self.assertEqual(horiz, 500 - (34 + ((345 - 34) / 2)))
        self.assertEqual(vert, 500 - (678 + ((700 - 678) / 2)))

    def test_nav_bounds3(self):
        w = 1000
        h = 1000
        # for a item detected at top right
        horiz, vert = nav.calculate_move_bounds((w, h), (678, 50, 800, 300))
        self.assertLess(horiz, 0)
        self.assertGreater(vert, 0)
        self.assertEqual(horiz, 500 - (678 + ((800 - 678) / 2)))
        self.assertEqual(vert, 500 - (50 + ((300 - 50) / 2)))

    def test_nav_bounds4(self):
        w = 1000
        h = 1000
        # for a item detected at top left
        horiz, vert = nav.calculate_move_bounds((w, h), (34, 20, 234, 300))
        self.assertGreater(horiz, 0)
        self.assertGreater(vert, 0)
        self.assertEqual(horiz, 500 - (34 + ((234 - 34) / 2)))
        self.assertEqual(vert, 500 - (20 + ((300 - 20) / 2)))


if __name__ == '__main__':
    unittest.main()
