# Cosmic Molecule Lab — Pure Python Desktop Edition

A native desktop rewrite of the supplied Cosmic MoleculeLab web project. The application is written in Python and uses Tkinter for its interface and RDKit for local cheminformatics. It does not use HTML, CSS, JavaScript, a browser, a CDN, or a JavaScript chemistry engine.

DEMO LINK 🌐 : https://chemquest-virtualuniverse.netlify.app/

## Features
- Native Python/Tkinter desktop interface with cosmic-themed tabs
- 250-item searchable organic compound catalog
- SMILES parsing and validation using RDKit
- Molecular formula, molecular weight, exact mass, LogP, TPSA, H-bond donors/acceptors, rotatable bonds, heavy atoms, formal charge and ring count
- Interactive 3D ball-and-stick-style viewer: drag to rotate, mouse wheel to zoom, auto-spin and reset
- 2D molecular structure drawing
- PubChem name lookup (optional internet connection)
- Copy canonical SMILES and export a text report
- Chemistry guide and SMILES quiz

## Requirements
- Python 3.10 or newer
- Tkinter (included with most standard Python installations)
- Packages in `requirements.txt`

## Run
```bash
python -m pip install -r requirements.txt
python main.py
```

On some Linux distributions, Tkinter may need to be installed separately (for example, `sudo apt install python3-tk`).

## Notes
All SMILES analysis and descriptors are calculated locally by RDKit. PubChem lookup is an optional online feature. This version's 3D view generates coordinates locally using RDKit; it does not fetch 3D structures from PubChem. Calculated descriptors are estimates, not experimental measurements. Verify compound identity before academic or laboratory use.
