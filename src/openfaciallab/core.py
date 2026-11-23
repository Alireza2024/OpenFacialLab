"""Minimal blendshape facial pose utilities, without third-party dependencies."""
from dataclasses import dataclass, field
from typing import Dict


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


@dataclass
class FacialPose:
    """Normalized 0..1 blendshape weights, suitable for prototype pipelines."""
    weights: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.weights = {str(k): _clamp(v) for k, v in self.weights.items()}

    def set(self, name: str, value: float) -> None:
        self.weights[name] = _clamp(value)

    def to_dict(self) -> Dict[str, float]:
        return dict(self.weights)


def combine_poses(*poses: FacialPose) -> FacialPose:
    """Add blendshape weights and clamp at 1.0; a simple baseline, not anatomical rig logic."""
    result: Dict[str, float] = {}
    for pose in poses:
        for name, value in pose.weights.items():
            result[name] = _clamp(result.get(name, 0.0) + value)
    return FacialPose(result)


def smooth_pose(previous: FacialPose, target: FacialPose, alpha: float) -> FacialPose:
    """Linear interpolation from previous to target; alpha 0 freezes, 1 snaps."""
    a = _clamp(alpha)
    names = previous.weights.keys() | target.weights.keys()
    return FacialPose({name: (1-a)*previous.weights.get(name, 0.0)
                       + a*target.weights.get(name, 0.0) for name in names})
