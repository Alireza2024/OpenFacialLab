from openfaciallab import FacialPose, combine_poses, smooth_pose

smile = FacialPose({"mouthSmileLeft": 0.7, "mouthSmileRight": 0.7})
blink = FacialPose({"eyeBlinkLeft": 1.0, "eyeBlinkRight": 1.0})
combined = combine_poses(smile, blink)
print("Combined:", combined.to_dict())
print("Halfway:", smooth_pose(FacialPose(), combined, 0.5).to_dict())
