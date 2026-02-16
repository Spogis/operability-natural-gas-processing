# 🔥 Operability Index and Constrained Optimization of a Natural Gas Processing Plant via DWSIM and Latin Hypercube Sampling

**A simulation-based framework using DWSIM and Latin Hypercube Sampling**

<div align="center">

[![DWSIM](https://img.shields.io/badge/DWSIM-v9.0.5-blue)](https://dwsim.org)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![DOI](https://img.shields.io/badge/Target-Digital%20Chemical%20Engineering-red)](https://www.sciencedirect.com/journal/digital-chemical-engineering)

</div>

---

## 📋 Overview

This repository contains the simulation model, datasets, analysis scripts, and manuscript for the operability analysis of a multi-column natural gas processing plant. The study applies the **Georgakis operability framework** to quantify the feasible operating envelope under Brazilian regulatory constraints (ANP Resolutions 16/2008 and 825/2020).

### Key Findings

| Metric | Value |
|--------|-------|
| **Operability Index (OI)** | 14.1% (281/2,000 feasible) |
| **Dominant bottleneck** | Reid Vapor Pressure ≤ 76 kPa (48.5% individual satisfaction) |
| **Critical coupling** | GVC5 vs. PVR inverse correlation (*r* = −0.65) |
| **Revenue driver** | Cold separator temperature (*r* = 0.984 with Sales Price) |
| **Best feasible revenue** | 663.85 $/h |

---

## 📁 Repository Structure

```
operability-natural-gas-processing/
│
├── datasets/
│   ├── dataset_clean.csv            # 2,000 LHS scenarios (10 columns)
│   └── dataset_full.csv             # Full simulation output
│
├── DWSIM/
│   └── NaturalGasProcessing.dwxmz   # DWSIM v9.0.5 flowsheet model
│
├── operability/
│   ├── figures/                      # Publication-quality figures (PNG + PDF)
│   ├── tables/                       # Analysis results (CSV)
│   └── operability_analysis.py       # Main analysis & visualisation script
│
├── paper/
│   ├── paper_gas_operability.docx    # Manuscript (Digital Chemical Engineering)
│   ├── references_gas_operability.bib# BibTeX references (35+ entries)
│   └── Artigo Tayná.pdf             # Reference paper (Souza et al., 2023)
│
└── Optimize Natural Gas Processing.ipynb  # DWSIM + Python optimisation notebook
```

---

## 🏭 Process Description

The DWSIM model represents a conventional natural gas processing train:

```
Raw Gas → Flash Separation → Deethaniser → Depropaniser → Debutaniser
              (V-123102)      (T-123701)    (T-123702)     (T-123703)
                  ↓                ↓             ↓              ↓
            Gas-Liquid Split   Sales Gas       LPG         C5+ Condensate
```

**16 components** (N₂, CO₂, C₁–C₁₂) · **Peng–Robinson EOS** · **10 separators** · **3 distillation columns** · **3 compressors**

---

## 🎯 Operability Framework

The analysis maps the **Available Input Set (AIS)** through the DWSIM model to obtain the **Achievable Output Set (AOS)**, and quantifies overlap with the **Desired Output Set (DOS)**:

### Decision Variables (AIS)

| Variable | Description | Range |
|----------|-------------|-------|
| u₁ | Cold separator temperature (V-123102) | −33 to −17 °C |
| u₂ | Deethaniser reboiler (T-123701) | 60 to 77 °C |
| u₃ | Depropaniser condenser (T-123702) | 0.7 to 4.5 °C |
| u₄ | Depropaniser reboiler (T-123702) | 9 to 27 °C |
| u₅ | Debutaniser reboiler (T-123703) | 45 to 64 °C |

### Product-Quality Constraints (DOS)

| Constraint | Meaning | Limit | Regulation |
|------------|---------|-------|------------|
| g₁ | Methane in sales gas | ≥ 80 mol% | ANP 16/2008 |
| g₂ | Ethane in LPG | ≤ 12 mol% | ANP 825/2020 |
| g₃ | C₅+ in LPG | ≤ 2 mol% | ANP 825/2020 |
| g₄ | Reid Vapour Pressure | ≤ 76 kPa | ANP 825/2020 |

---

## ⚡ Quick Start

### Requirements

```bash
pip install pandas numpy matplotlib scipy seaborn
```

### Run the Analysis

```bash
cd operability/
python operability_analysis.py
```

This generates all 10 figures and 4 tables in the `figures/` and `tables/` subdirectories.

### Open the DWSIM Model

1. Download [DWSIM v9.0.5+](https://dwsim.org)
2. Open `DWSIM/NaturalGasProcessing.dwxmz`
3. Run the Jupyter notebook for LHS sampling and optimisation

---

## 📊 Selected Results

### Constraint Relaxation Analysis

| Removed Constraint | OI (%) | ΔOI (pp) |
|-------------------|--------|----------|
| None (baseline) | 14.1 | — |
| g₁: GVC1 ≥ 80 | 14.1 | +0.0 |
| g₂: GVC2 ≤ 12 | 23.1 | +9.0 |
| g₃: GVC5 ≤ 2 | 34.8 | +20.7 |
| **g₄: PVR ≤ 76** | **35.5** | **+21.4** |

---

## 📖 Citation

If you use this work, please cite:

```bibtex
@article{Spogis2026operability,
  author  = {Spogis, Nicolas and Carpio, Roymel R. and Freitas, Gabriel},
  title   = {Operability Analysis of a Natural Gas Processing Plant:
             A Simulation-Based Framework Using {DWSIM} and
             {L}atin Hypercube Sampling},
  journal = {Digital Chemical Engineering},
  year    = {2026},
  note    = {Manuscript submitted for publication}
}
```

---

## 👥 Authors

<div align="center">

**Prof. Nicolas Spogis, Ph.D.**<br>
**Prof. Roymel Rodríguez Carpio, Ph.D.**<br>
**Gabriel Freitas**

</div>

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [DWSIM](https://dwsim.org) — Open-source chemical process simulator by Daniel Medeiros
- [Opyrability](https://github.com/victoralves/opyrability) — Process operability Python package
- [AI4Tech](https://ai4tech.ai/) — Computational infrastructure
