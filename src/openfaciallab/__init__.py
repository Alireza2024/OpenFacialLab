"""OpenFacialLab: a small, engine-independent facial pose prototype."""
from .core import FacialPose, combine_poses, smooth_pose
__all__ = ["FacialPose", "combine_poses", "smooth_pose"]
