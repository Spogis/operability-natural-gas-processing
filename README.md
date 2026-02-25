# 🔥 Operability Index and Constrained Optimization of a Natural Gas Processing Plant via DWSIM and Latin Hypercube Sampling

**A simulation-based framework using DWSIM and Latin Hypercube Sampling**

<div align="center">

[![DWSIM](https://img.shields.io/badge/DWSIM-v9.0.5-blue)](https://dwsim.org)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Journal](https://img.shields.io/badge/Submitted-Computers%20%26%20Chemical%20Engineering-red)](https://www.sciencedirect.com/journal/computers-and-chemical-engineering)

</div>

---

## 📋 Overview

This repository contains the simulation model, datasets, and analysis scripts for the operability analysis of a multi-column natural gas processing plant. The study applies the **Georgakis process operability framework** to quantify the feasible operating envelope under Brazilian regulatory constraints (ANP Resolutions 16/2008 and 825/2020).

The work was submitted to *Computers and Chemical Engineering* (Manuscript CACE-D-26-00317).

### Key Findings

| Metric | Value |
|--------|-------|
| **Operability Index (OI)** | 14.1% (281/2,000 feasible) |
| **Dominant bottleneck** | Reid Vapour Pressure ≤ 76 kPa (48.5% individual satisfaction) |
| **Critical coupling** | LPG_C5 vs. NG_RVP inverse correlation (*r* = −0.650) |
| **Revenue driver** | Cold separator temperature (*r* = −0.984 with Revenue) |
| **Best feasible revenue (SLSQP)** | 663.85 $/h |
| **Best LHS revenue** | 662.83 $/h |

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
├── .gitignore
├── LICENSE.txt
├── README.md
└── Optimize Natural Gas Processing.ipynb  # DWSIM + Python optimisation notebook
```

---

## 🏭 Process Description

The DWSIM model represents a conventional natural gas processing plant with two tightly coupled units: a **Dew Point Unit (DPU)** and a **Liquid Fractionation Unit (LFU)**.

```
                        DPU                                    LFU
Raw Gas → Gas-Liquid Separation → Deethaniser → Debutaniser → Stabiliser
              (V-02)                (T-01)        (T-02)        (T-03)
                ↓                     ↓             ↓             ↓
          Gas-Liquid Split        Sales Gas        LPG        Natural Gasoline
```

**16 components** (N₂, CO₂, C₁–C₁₂) · **Peng–Robinson EOS (COSTALD)** · **10 separators** · **3 distillation columns** · **3 compressors**

### Distillation Column Specifications

| Column | Function | Stages | ΔP (kPa) |
|--------|----------|--------|----------|
| T-01 | Deethaniser | 11 | 261 |
| T-02 | Debutaniser | 21 | 100 |
| T-03 | Stabiliser | 6 | 9 |

---

## 🎯 Operability Framework

The analysis maps the **Available Input Set (AIS)** through the DWSIM model to obtain the **Achievable Output Set (AOS)**, and quantifies overlap with the **Desired Output Set (DOS)**:

$$\text{OI} = \frac{\mu(\text{AOS} \cap \text{DOS})}{\mu(\text{DOS})}$$

### Decision Variables (AIS)

| Variable | Symbol | Description | Lower | Upper | Unit |
|----------|--------|-------------|-------|-------|------|
| u₁ | V_02_Temp | Cold separator temperature | −33 | −17 | °C |
| u₂ | T_01_Reb | Deethaniser reboiler temperature | 51 | 94 | °C |
| u₃ | T_02_RR | Debutaniser reflux ratio | 0.7 | 4.5 | — |
| u₄ | T_02_Reb | Debutaniser reboiler temperature | 107 | 183 | °C |
| u₅ | T_03_Reb | Stabiliser reboiler temperature | 152 | 206 | °C |

### Product-Quality Constraints (DOS)

| Constraint | Symbol | Description | Limit | Regulation |
|------------|--------|-------------|-------|------------|
| g₁ | SG_C1 | Methane in Sales Gas | ≥ 80 mol% | ANP 16/2008 |
| g₂ | LPG_C2 | Ethane in LPG | ≤ 12 mol% | ANP 825/2020 |
| g₃ | LPG_C5 | C₅₊ in LPG | ≤ 2 mol% | ANP 825/2020 |
| g₄ | NG_RVP | Reid Vapour Pressure of NG | ≤ 76 kPa | ANP 825/2020 |

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

This generates all figures and tables in the `figures/` and `tables/` subdirectories.

### Open the DWSIM Model

1. Download [DWSIM v9.0.5+](https://dwsim.org)
2. Open `DWSIM/NaturalGasProcessing.dwxmz`
3. Run the Jupyter notebook for LHS sampling and optimisation

---

## 📊 Selected Results

### Individual and Joint Constraint Satisfaction

| Constraint | Satisfaction | % |
|------------|-------------|---|
| g₁: SG_C1 ≥ 80 | 2,000 / 2,000 | 100.0% (non-binding) |
| g₂: LPG_C2 ≤ 12 | 1,125 / 2,000 | 56.2% |
| g₃: LPG_C5 ≤ 2 | 1,493 / 2,000 | 74.7% |
| g₄: NG_RVP ≤ 76 | 970 / 2,000 | 48.5% (dominant bottleneck) |
| **All constraints** | **281 / 2,000** | **14.1% (OI)** |

### Constraint Relaxation Analysis

| Removed Constraint | OI (%) | ΔOI (pp) | Interpretation |
|-------------------|--------|----------|----------------|
| None (baseline) | 14.1 | — | Full constraint set |
| g₁: SG_C1 ≥ 80 | 14.1 | +0.0 | Non-binding |
| g₂: LPG_C2 ≤ 12 | 23.1 | +9.0 | Moderate impact |
| g₃: LPG_C5 ≤ 2 | 34.8 | +20.7 | Strong impact |
| **g₄: NG_RVP ≤ 76** | **35.5** | **+21.4** | **Dominant bottleneck** |

### Dominant Variable Correlations

| Variable 1 | Variable 2 | Pearson *r* | Physical Mechanism |
|------------|------------|-------------|-------------------|
| V-02_Temp | Revenue | −0.984 | Colder separator → more liquid recovery → higher revenue |
| T-01_Reb | LPG_C2 | −0.970 | Hotter deethaniser → less ethane in LPG |
| T-02_Reb | NG_RVP | −0.976 | Hotter debutaniser → lower RVP |
| LPG_C5 | NG_RVP | −0.650 | More C₅₊ in LPG → fewer lights in NG → lower RVP |

### Optimal Operating Point (SLSQP)

| Variable | Value | Constraint Status |
|----------|-------|------------------|
| V-02_Temp | −33.00 °C | Lower bound |
| T-01_Reb | 66.29 °C | — |
| T-02_RR | 4.31 | — |
| T-02_Reb | 140.11 °C | — |
| T-03_Reb | 197.24 °C | — |
| **Revenue** | **663.85 $/h** | |
| LPG_C2 | 12.00 mol% | ✓ Active |
| NG_RVP | 76.00 kPa | ✓ Active |

---

## 📖 Citation

If you use this work, please cite:

```bibtex
@article{Ferraz2026operability,
  author  = {Ferraz, Gabriel F. and Carpio, Roymel R. and Spogis, Nicolas},
  title   = {Operability Index and Constrained Optimization of a Natural Gas
             Processing Plant via {DWSIM} and {L}atin Hypercube Sampling},
  journal = {Computers and Chemical Engineering},
  year    = {2026},
  note    = {Manuscript CACE-D-26-00317, submitted for publication}
}
```

---

## 👥 Authors

<div align="center">

**Gabriel F. Ferraz**<br>
School of Chemistry, Universidade Federal do Rio de Janeiro (UFRJ)<br><br>
**Prof. Roymel R. Carpio, Ph.D.** *(Corresponding Author)*<br>
School of Chemistry, Universidade Federal do Rio de Janeiro (UFRJ)<br>
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--9633--291X-green)](https://orcid.org/0000-0002-9633-291X)<br><br>
**Prof. Nicolas Spogis, Ph.D.**<br>
AI4Tech & School of Chemical Engineering, University of Campinas (UNICAMP)<br>
[![ORCID](https://img.shields.io/badge/ORCID-0000--0003--2094--5178-green)](https://orcid.org/0000-0003-2094-5178)

</div>

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [DWSIM](https://dwsim.org) — Open-source chemical process simulator by Daniel Medeiros
- [Opyrability](https://github.com/victoralves/opyrability) — Process operability Python package
- [AI4Tech](https://ai4tech.ai/) — Computational infrastructure
- FAPERJ — Fundação Carlos Chagas Filho de Amparo à Pesquisa do Estado do Rio de Janeiro
- CAPES — Coordination for the Improvement of Higher Education Personnel
