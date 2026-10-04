# Licensing and attribution

Effective October 4, 2026. This file identifies the material covered by each
license. The MIT license at the repository root covers the authors' software and
accompanying software documentation; the research data use a separate license.

## Software — MIT

Copyright (c) 2026 Giovanni Cocca-Guardia and contributors.

The authors' Python source files (`solver_fem_2d.py`, `mesh_generator.py`,
`exp_1.py`, `exp_2.py`, `exp_3.py` and `calibration_sensitivity.py`), installation
requirements, `.gitignore`, README and the Markdown documentation under `docs/`
are licensed under [MIT](LICENSE). Standard license texts retain their own terms.

## Data — CC BY 4.0

Copyright (c) 2026 Giovanni Cocca-Guardia.

The author's rights in the following research data are licensed under the
[Creative Commons Attribution 4.0 International license](LICENSE-DATA):

- Meshes: `gmsh_meshes/*.npz`.
- Calibration sensitivity results: `docs/calibration_leave_one_LED_out.csv` and
  `docs/calibration_summary.json`.

CC BY 4.0 permits sharing and adaptation, including commercial reuse, with
attribution, a license link, and an indication of changes. It grants only rights
the licensor holds and does not create exclusive rights over facts or other
unprotected material. The canonical license is
<https://creativecommons.org/licenses/by/4.0/>.

For attribution, retain the credit **Giovanni Cocca-Guardia**, the
repository/release URL, and the CC BY 4.0 notice. An academic citation of the
associated research is welcome; this request adds no condition to either license.

The five original LED distance/voltage pairs embedded in the experiment source
and reproduced in the documentation are also available under CC BY 4.0, to the
extent any relevant rights apply. The source code remains MIT-licensed.

## Exclusions and dependencies

The article text, LaTeX/PDF and prepared publication figure compositions are not
covered by these licenses. They are not included in this repository. Any
publication agreement for the article is separate from these grants; the
underlying meshes and numerical data identified above retain their data license.

Third-party dependencies keep their original licenses; they are installed
separately and are not relicensed here. See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). References to external visual
models in the adapter guide grant no rights to those models. This FEM repository
does not include AI implementation, video frames or pretrained weights.

## Applicability to archived releases

These grants also apply, with the same scope and exclusions, to the covered
files in the original `clagtee-2026-v1.0` release, from the effective date above.
That tag and its scientific files are unchanged. The `clagtee-2026-v1.0.1`
release packages the licenses with the same FEM code, meshes and calibration
results. No experiment has been modified by this licensing release.
