# OpenFacialLab

**Status: early prototype / work in progress.**

OpenFacialLab is an experimental, open-source facial animation toolkit intended for digital characters in games and film. The long-term goal is to investigate expressive facial controls, blendshape combinations, rigging workflows, and eventual DCC / game-engine integration. High-end facial systems such as Weta's APFS are an *aspiration for the problem domain*, not an implementation or affiliation claim.

## What works today

- Store named facial blendshape weights in a normalized 0–1 range.
- Combine poses by additive, clamped weights.
- Interpolate poses for basic smoothing.
- Run small, dependency-free Python examples and unit tests.

This is **not** yet a production facial rig, solver, FACS implementation, Unreal/MetaHuman integration, or APFS equivalent.

## Quick start

Requires Python 3.9+; no external packages.

```bash
python -m pip install -e .
python examples/demo.py
python -m unittest discover -s tests
```

## Roadmap (planned, not implemented)

1. Define a documented facial pose and channel naming format.
2. Explore asymmetric controls and pose-space corrective shapes.
3. Build Blender and Unreal Engine import/export prototypes.
4. Explore FACS-inspired action units and facial performance retargeting.
5. Add examples, validation tools, benchmarks, and tutorials.

## Contributing

Issues, design feedback, and pull requests are welcome. Please open an issue before proposing major architectural changes.

## License

MIT — see LICENSE.
