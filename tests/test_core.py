import unittest
from openfaciallab import FacialPose, combine_poses, smooth_pose

class TestFacialPose(unittest.TestCase):
    def test_clamping(self):
        self.assertEqual(FacialPose({"a": 1.5, "b": -0.3}).to_dict(), {"a": 1, "b": 0})

    def test_combine(self):
        self.assertEqual(combine_poses(FacialPose({"a": 0.8}), FacialPose({"a": 0.5})).weights["a"], 1)

    def test_smooth(self):
        self.assertEqual(smooth_pose(FacialPose(), FacialPose({"a": 1}), 0.25).weights["a"], 0.25)

if __name__ == "__main__":
    unittest.main()
