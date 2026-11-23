"""Experimental Maya blendshape transfer prototype.

Based on a workflow supplied by the project owner:
source blendshape targets -> source deformation -> wrap -> destination duplicates.

IMPORTANT: This code requires Autodesk Maya and a compatible scene setup.
It has NOT been tested in Maya. Run only on a disposable scene copy.
This is a prototype; it is not an APFS reproduction.
"""
import maya.cmds as cmds
import maya.mel as mel


def _shape(transform):
    shapes = cmds.listRelatives(transform, shapes=True, noIntermediate=True, fullPath=True) or []
    if len(shapes) != 1 or cmds.nodeType(shapes[0]) != "mesh":
        raise RuntimeError("Expected a transform with one visible mesh shape: %s" % transform)
    return shapes[0]


def _unique(name):
    if not cmds.objExists(name):
        return name
    i = 1
    while cmds.objExists("%s_%03d" % (name, i)):
        i += 1
    return "%s_%03d" % (name, i)


def transfer_targets(mesh_a, mesh_b, target_group, source_transfer_mesh, destination_transfer_mesh):
    """Bake source target shapes onto another mesh via a Maya wrap deformer.

    Parameters:
        mesh_a: source neutral transform
        mesh_b: target neutral transform
        target_group: transform containing source target mesh transforms
        source_transfer_mesh: transfer driver mesh, matching mesh_a topology
        destination_transfer_mesh: mesh preconfigured to receive the wrap

    Assumes matching neutral poses, pre-aligned geometry, correct wrap binding,
    and that target meshes are compatible with mesh_a.

    No scene edits are attempted before basic validation. Operations after
    validation are destructive to *temporary nodes only* but may still
    change deformer evaluation. Save a scene copy first.
    """
    required = [mesh_a, mesh_b, target_group, source_transfer_mesh, destination_transfer_mesh]
    missing = [item for item in required if not cmds.objExists(item)]
    if missing:
        raise ValueError("Missing required scene objects: %s" % ", ".join(missing))
    for mesh in [mesh_a, mesh_b, source_transfer_mesh, destination_transfer_mesh]:
        _shape(mesh)

    targets = cmds.listRelatives(target_group, children=True, type="transform", fullPath=True) or []
    targets = [t for t in targets if cmds.listRelatives(t, shapes=True, noIntermediate=True)]
    if not targets:
        raise RuntimeError("No target mesh transforms found in %s" % target_group)
    for target in targets:
        _shape(target)

    output = cmds.group(empty=True, name=_unique("grp_facial_transfer_output"))
    source_bs = None
    wrapped = None
    cycler = None
    driver_bs = None
    try:
        source_bs = cmds.blendShape(targets, mesh_a, name=_unique("bs_ofl_source"), frontOfChain=True)[0]
        aliases = cmds.aliasAttr(source_bs, query=True) or []
        target_aliases = [aliases[i] for i in range(0, len(aliases), 2)]
        if len(target_aliases) != len(targets):
            raise RuntimeError("Could not resolve source target blendShape aliases")

        # Duplicate a source-compatible transfer mesh to receive the source pose.
        wrapped = cmds.duplicate(source_transfer_mesh, name=_unique("ofl_source_pose_transfer"))[0]
        driver_bs = cmds.blendShape(mesh_a, wrapped, name=_unique("bs_ofl_transfer"), frontOfChain=True)[0]
        cmds.setAttr(driver_bs + ".w[0]", 1.0)

        # Create wrap: destination transfer mesh deforms based on source pose.
        cmds.select([destination_transfer_mesh, wrapped], replace=True)
        mel.eval("CreateWrap;")

        # Cycle target poses and bake the destination deformed mesh.
        for i, target in enumerate(targets):
            cmds.setAttr("%s.w[%d]" % (source_bs, i), 1.0)
            cmds.refresh(force=True)
            name = target.rsplit("|", 1)[-1]
            duplicated = cmds.duplicate(destination_transfer_mesh,
                                        name=_unique(name + "_transferred"))[0]
            cmds.delete(duplicated, constructionHistory=True)
            cmds.parent(duplicated, output)
            cmds.setAttr("%s.w[%d]" % (source_bs, i), 0.0)

        return output
    finally:
        # Preserve scene and original neutral meshes. Remove only our
        # temporary source blendshape if it was created.
        if source_bs and cmds.objExists(source_bs):
            cmds.delete(source_bs)
        if driver_bs and cmds.objExists(driver_bs):
            cmds.delete(driver_bs)
        if wrapped and cmds.objExists(wrapped):
            cmds.delete(wrapped)
        cmds.select(clear=True)


# Example (edit names to match your Maya scene; do not run unmodified):
# transfer_targets(
#     mesh_a="mesh_source", mesh_b="mesh_target",
#     target_group="grp_trgt",
#     source_transfer_mesh="trgt_source_xfer",
#     destination_transfer_mesh="trgt_target_xfer",
# )
