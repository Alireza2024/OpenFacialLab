# Experimental Maya Blendshape Transfer

The script [`transfer_blendshapes.py`](transfer_blendshapes.py) is an **untested early prototype** of a Maya-based facial target transfer pipeline, inspired by a workflow supplied by the project owner.

It uses `maya.cmds`, Maya's `CreateWrap` command, a temporary source blendShape, and target-by-target baking.

## Before running

- Use an expendable copy of your Maya scene.
- Align the neutral source and destination meshes.
- Create a source target group whose child transforms are the blendshape targets.
- Prepare source and destination transfer meshes with an appropriate wrap binding.
- Check every output against the neutral target; some wrap setups require a corrected neutral and additional subtraction of offsets.
- Update the example object names at the bottom of the script.

## Limitations

Not tested in Autodesk Maya. Depending on the scene, wrap direction, geometry history, or pre-existing deformers, results may be wrong. This is not a reliable automatic retargeting solution or a substitute for a production rig. A future iteration should validate point counts, aliases, wrap construction, deltas, and cleanup with Maya integration tests.

## Rights

Only contribute code you own or are permitted to share under the repository license.
