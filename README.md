# MSA²: Multi-task Framework with Structure-aware and Style-adaptive Character Representation
<p align="center">
  <img src="imgs/teaser.pdf" width="70%" alt="MSA2 pipeline">
</p>

> Official implementation of **“MSA²: Multi-task Framework with Structure-aware and Style-adaptive Character Representation for Open-set Chinese Text Recognition”** (ICCV 2025).  
> **Yangfu Li, Hongjian Zhan, Qi Liu, Li Sun, Yu-Jie Xiong, Yue Lu**.

[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.9%2B-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-orange)
![Status](https://img.shields.io/badge/status-ongoing-yellow)

---

## ✨ Highlights
* **Multi-task recognition** that **jointly** decodes linguistic components and glyph prototypes, eliminating costly fine-tuning for unseen characters.  
* **SACE (Structure-Aware Component Encoding)** — a binary-tree coding scheme that allocates **larger bit-width** to *primary* structures, mirroring human perception.  
* **SAGE (Style-Adaptive Glyph Embedding)** — glyph-centric contrastive learning that distills a **robust glyph lexicon** across 10 font families and 70+ style variants.  
* **State-of-the-art** results on **BCTR**, **ICDAR 2013**, **CTW** under both closed-set and open-set protocols (see paper for full tables).  

For an intuitive overview please check our paper and the diagram above.  

---

## 🔧 Installation
```bash
# 1. create environment
conda create -n msa2 python=3.9
conda activate msa2

# 2. install PyTorch & TorchVision (choose your CUDA version)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118    # example for CUDA 11.8

# 3. install other dependencies
pip install -r requirements.txt
```

> **Note** : We strongly recommend **PyTorch 2.x** + **CUDA 11.8/12.x**; other combinations may work but are not fully tested.

---

## 📂 Directory Structure
```
MSA-2/
├── lexicon_building/        # SACE / SAGE codes to build linguistic & glyph lexicons
│   ├── sace/                # structure-aware component encoder
│   ├── sage/                # glyph-centric contrastive learning
│   └── utils/
├── recognition/             # multi-task recognizer (training / inference / eval)
│   ├── models/
│   ├── trainer/
│   ├── decoder/
│   └── benchmarks/          # configs for BCTR, ICDAR-line/char, CTW …
├── docs/                    # paper figures, dataset links, model-zoo (coming)
└── requirements.txt
```

*(Some folders may appear empty until the corresponding TODO items are completed.)*

---

## 🏃‍♂️ Quick Start

### 1. Build Representation Lexicons
```bash
# linguistic component lexicon (SACE)
python lexicon_building/sace/build_sace_lexicon.py \
       --charset data/charsets/gb18030.txt \
       --output  outputs/lexicons/sace.json

# glyph lexicon (SAGE) – requires CLIP-ViT backbone
python lexicon_building/sage/build_sage_lexicon.py \
       --charset data/charsets/gb18030.txt \
       --glyph_root data/glyphs \
       --output  outputs/lexicons/sage.pt
```

### 2. Training
```bash
CUDA_VISIBLE_DEVICES=0,1 python recognition/train.py \
    --config configs/bctr_resnet34.yaml \
    --sace_lexicon outputs/lexicons/sace.json \
    --sage_lexicon outputs/lexicons/sage.pt
```

### 3. Evaluation & Inference
```bash
# evaluate on BCTR Scene subset
python recognition/eval.py --resume checkpoints/bctr_scene.pth \
    --dataset bctr_scene --eval_open_set

# single-image demo
python recognition/infer.py --img demo/word.jpg \
    --checkpoint checkpoints/bctr_scene.pth
```

More **dataset preparation scripts** are provided under `recognition/benchmarks/`.

---

## 📊 Pre-trained Models
Pre-trained weights will be released after paper acceptance. Stay tuned!

| Backbone | Training data | Closed-set Acc. | Open-set Acc. | Download |
|----------|---------------|-----------------|---------------|----------|
| ResNet-34 + 2×BiLSTM | BCTR full | 77.1 | 75.4 | _TBA_ |

---

## TODO 🗂️
<!-- 以下列表覆盖了 **MSA²** 项目的所有主要组成部分。**已开源**的部分已勾选，你可在完成后自行把 `[ ]` 改为 `[x]`。 -->

- [x] **lexicon_building/sace** — Structure-Aware Component Encoding  
- [ ] **lexicon_building/sage** — Style-Adaptive Glyph Embedding  
- [ ] **recognition/** — multi-task recognizer (training / inference)  
- [ ] **dataset scripts** — BCTR / ICDAR / CTW download & preprocessing  
- [ ] **open-set evaluation pipeline** (+ metrics aggregation)  
- [ ] **pre-trained checkpoints** for all backbones  
- [ ] **model-zoo & leaderboard** (`docs/model_zoo.md`)  
- [ ] **demo notebook / Gradio web demo**  
- [ ] **Dockerfile & Conda-env.yaml** for one-click setup  
- [ ] **continuous integration** (unit-tests & style-check via GitHub Actions)  
- [ ] **comprehensive documentation site** (Sphinx / mkdocs)  
- [ ] **license upd.** (add third-party notices)  
- [ ] **BibTeX citation** (after camera-ready)  

Feel free to ping us via issues if you’d like to contribute to any unchecked item!

---

## 📜 Citation
```bibtex
@inproceedings{li2025msa2,
  title     = {MSA\textsuperscript{2}: Multi-task Framework with Structure-aware and Style-adaptive Character Representation for Open-set Chinese Text Recognition},
  author    = {Li, Yangfu and Zhan, Hongjian and Liu, Qi and Sun, Li and Xiong, Yu-Jie and Lu, Yue},
  booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
  year      = {2025}
}
```

---

## 🤝 Acknowledgements
This repo builds upon [CLIP](https://github.com/openai/CLIP), [PyTorch](https://pytorch.org) and the **BCTR** benchmark.  
If you find this project useful, please consider citing our work and those dependencies.

---

## 📧 Contact
For questions or collaboration feel free to create an issue or contact **yangfuli(at)ecnu.edu.cn**.

---

*This README is under active development and may change as we release more components.*
