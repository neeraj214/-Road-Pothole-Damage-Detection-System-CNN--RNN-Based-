"""
src/evaluate.py
===============
Full evaluation script for the Road Pothole & Damage Detection Model.

Generates:
  results/confusion_matrix.png            — raw counts + percentages heatmap
  results/confusion_matrix_normalized.png — row-normalised (recall) heatmap
  results/classification_report.txt       — sklearn text report
  results/model_summary.txt               — human-readable summary metrics

Run with:
  python -m src.evaluate
"""

import os
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")           # headless — no display needed
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
)

from src import config
from src.utils import bce_dice_loss
from src.data_loader import build_generators

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────
MODEL_PATH  = os.path.join(config.MODELS_DIR, "best_model_dual_v6_deeper_tf")
RESULTS_DIR = config.RESULTS_DIR
CLASSES     = ["Normal", "Crack", "Pothole"]
IMG_SIZE    = 160
BATCH_SIZE  = 8
VAL_SPLIT   = 0.2


# ─────────────────────────────────────────────────────────────────────────────
# Step 1 — GPU memory growth
# ─────────────────────────────────────────────────────────────────────────────
def configure_gpu() -> None:
    gpus = tf.config.list_physical_devices("GPU")
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logger.info(f"GPU memory growth enabled on {len(gpus)} device(s).")
    else:
        logger.info("No GPU detected — running on CPU.")


# ─────────────────────────────────────────────────────────────────────────────
# Step 2 — Load model
# ─────────────────────────────────────────────────────────────────────────────
def load_model() -> tf.keras.Model:
    logger.info(f"Loading model from: {MODEL_PATH}")
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at '{MODEL_PATH}'.\n"
            "Ensure models/best_model_dual_v6_deeper_tf exists."
        )
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects={"bce_dice_loss": bce_dice_loss},
        compile=False,
    )
    logger.info("Model loaded successfully.")
    return model


# ─────────────────────────────────────────────────────────────────────────────
# Step 3 — Build validation dataset (same random_state=42 as training)
# ─────────────────────────────────────────────────────────────────────────────
def get_val_dataset():
    data_dir = config.TRAIN_DIR   # build_generators scans train/ and splits
    mask_dir = config.MASK_DIR
    logger.info(f"Building validation split from: {data_dir}")
    _, val_ds = build_generators(
        data_dir=data_dir,
        mask_dir=mask_dir,
        batch_size=BATCH_SIZE,
        val_split=VAL_SPLIT,
        img_size=IMG_SIZE,
    )
    return val_ds


# ─────────────────────────────────────────────────────────────────────────────
# Step 4 — Run inference: collect y_true, y_pred
# ─────────────────────────────────────────────────────────────────────────────
def collect_predictions(model: tf.keras.Model, val_ds) -> tuple:
    """
    Iterate the full validation tf.data.Dataset.
    Each batch yields (X, {"cls_output": one_hot, "seg_output": masks}).
    Model outputs: [cls_logits (B,3), seg_map (B,H,W,4)].
    Returns (y_true, y_pred) as integer-label numpy arrays.
    """
    y_true_all: list[int] = []
    y_pred_all: list[int] = []
    batch_idx = 0

    logger.info("Running inference on validation set — please wait…")

    for batch_X, batch_Y in val_ds:
        true_cls = np.argmax(batch_Y["cls_output"].numpy(), axis=1)

        outputs   = model(batch_X, training=False)
        pred_cls  = np.argmax(outputs[0].numpy(), axis=1)

        y_true_all.extend(true_cls.tolist())
        y_pred_all.extend(pred_cls.tolist())
        batch_idx += 1

        if batch_idx % 20 == 0:
            logger.info(f"  … {batch_idx} batches  |  {len(y_true_all)} samples")

    y_true = np.array(y_true_all, dtype=np.int32)
    y_pred = np.array(y_pred_all, dtype=np.int32)
    logger.info(f"Inference complete — {len(y_true)} samples evaluated.")
    return y_true, y_pred


# ─────────────────────────────────────────────────────────────────────────────
# Steps 5 & 8 — Plot confusion matrix
# ─────────────────────────────────────────────────────────────────────────────
def _cell_label(count: int, pct: float) -> str:
    return f"{count}\n({pct:.1f}%)"


def plot_confusion_matrix(cm: np.ndarray, save_path: str,
                          title: str, normalised: bool = False) -> None:
    n        = len(CLASSES)
    row_sums = cm.sum(axis=1, keepdims=True).astype(float)
    cm_pct   = np.where(row_sums > 0, cm / row_sums * 100.0, 0.0)

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")

    if normalised:
        cm_norm = np.where(row_sums > 0, cm / row_sums, 0.0)
        annot   = np.array([[f"{cm_norm[i, j]:.2f}" for j in range(n)]
                            for i in range(n)])
        sns.heatmap(
            cm_norm, annot=annot, fmt="", cmap="Blues",
            xticklabels=CLASSES, yticklabels=CLASSES,
            linewidths=0.5, linecolor="white",
            vmin=0.0, vmax=1.0, ax=ax,
            annot_kws={"size": 13, "weight": "bold"},
        )
    else:
        annot = np.array([[_cell_label(cm[i, j], cm_pct[i, j])
                           for j in range(n)]
                          for i in range(n)])
        sns.heatmap(
            cm, annot=annot, fmt="", cmap="Blues",
            xticklabels=CLASSES, yticklabels=CLASSES,
            linewidths=0.5, linecolor="white",
            ax=ax,
            annot_kws={"size": 12, "weight": "bold"},
        )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=16)
    ax.set_xlabel("Predicted Class", fontsize=12, labelpad=10)
    ax.set_ylabel("True Class",      fontsize=12, labelpad=10)
    ax.tick_params(axis="both", labelsize=11)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved → {save_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Step 6 — Classification report
# ─────────────────────────────────────────────────────────────────────────────
def save_classification_report(y_true: np.ndarray, y_pred: np.ndarray,
                                save_path: str) -> None:
    report = classification_report(
        y_true, y_pred,
        target_names=CLASSES,
        digits=4,
    )
    border = "=" * 60
    header = f"\n{border}\nCLASSIFICATION REPORT\n{border}\n"
    print(header + report)

    with open(save_path, "w") as fh:
        fh.write("CLASSIFICATION REPORT — Road Pothole Detection Model\n")
        fh.write(border + "\n\n")
        fh.write(report)
    logger.info(f"Saved → {save_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Step 7 — Model summary metrics
# ─────────────────────────────────────────────────────────────────────────────
def save_model_summary_metrics(cm: np.ndarray, y_true: np.ndarray,
                                y_pred: np.ndarray, save_path: str) -> None:
    total         = int(len(y_true))
    overall_acc   = accuracy_score(y_true, y_pred) * 100.0
    row_sums      = cm.sum(axis=1).astype(float)
    per_class_acc = {
        cls: (cm[i, i] / row_sums[i] * 100.0 if row_sums[i] > 0 else 0.0)
        for i, cls in enumerate(CLASSES)
    }

    # Most confused pair (largest off-diagonal cell)
    cm_off   = cm.copy()
    np.fill_diagonal(cm_off, 0)
    max_idx        = np.unravel_index(np.argmax(cm_off), cm_off.shape)
    confused_true  = CLASSES[max_idx[0]]
    confused_pred  = CLASSES[max_idx[1]]
    confused_count = int(cm_off[max_idx])

    sep = "-" * 50
    lines = [
        "MODEL EVALUATION SUMMARY — Road Pothole Detection",
        "=" * 55,
        f"  Model      : models/best_model_dual_v6_deeper_tf",
        f"  Dataset    : data/raw/train  (20% val split, seed=42)",
        f"  Val samples: {total}",
        f"  Image size : {IMG_SIZE}×{IMG_SIZE}",
        f"  Batch size : {BATCH_SIZE}",
        "",
        "OVERALL ACCURACY",
        sep,
        f"  {overall_acc:.2f}%",
        "",
        "PER-CLASS ACCURACY (diagonal recall)",
        sep,
    ]
    for cls, acc in per_class_acc.items():
        n_cls = int(row_sums[CLASSES.index(cls)])
        lines.append(f"  {cls:<10}  {acc:>6.2f}%   (n={n_cls})")

    lines += [
        "",
        "RAW CONFUSION MATRIX",
        sep,
        "               " + "  ".join(f"{c:<10}" for c in CLASSES),
    ]
    for i, cls in enumerate(CLASSES):
        row_vals = "  ".join(f"{cm[i, j]:<10}" for j in range(len(CLASSES)))
        lines.append(f"  {cls:<12}  {row_vals}")

    lines += [
        "",
        "MOST CONFUSED PAIR",
        sep,
        f"  True: {confused_true}  →  Predicted as: {confused_pred}"
        f"  ({confused_count} samples)",
        "",
        "NOTES",
        sep,
        "  Seg head predicts pixel-level damage density.",
        "  RPS (Repair Priority Score) is derived from seg coverage.",
    ]

    text = "\n".join(lines)
    print("\n" + text + "\n")
    with open(save_path, "w") as fh:
        fh.write(text + "\n")
    logger.info(f"Saved → {save_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    logger.info("═" * 60)
    logger.info("  Road Pothole Detection — Full Evaluation Pipeline")
    logger.info("═" * 60)

    os.makedirs(RESULTS_DIR, exist_ok=True)

    configure_gpu()
    model  = load_model()
    val_ds = get_val_dataset()

    y_true, y_pred = collect_predictions(model, val_ds)

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    logger.info(f"Confusion matrix:\n{cm}")

    # Raw counts + percentages
    plot_confusion_matrix(
        cm,
        save_path=os.path.join(RESULTS_DIR, "confusion_matrix.png"),
        title="Confusion Matrix — Road Pothole Detection Model",
        normalised=False,
    )

    # Row-normalised (recall per class)
    plot_confusion_matrix(
        cm,
        save_path=os.path.join(RESULTS_DIR, "confusion_matrix_normalized.png"),
        title="Normalised Confusion Matrix (Recall per Class)",
        normalised=True,
    )

    save_classification_report(
        y_true, y_pred,
        save_path=os.path.join(RESULTS_DIR, "classification_report.txt"),
    )

    save_model_summary_metrics(
        cm, y_true, y_pred,
        save_path=os.path.join(RESULTS_DIR, "model_summary.txt"),
    )

    logger.info("═" * 60)
    logger.info(f"  Done. All results saved to: {RESULTS_DIR}")
    logger.info("═" * 60)


if __name__ == "__main__":
    main()
