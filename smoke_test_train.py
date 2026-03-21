import os
import tensorflow as tf
from src.train import stage1_train, stage2_finetune, bce_dice_loss
from src.model import build_dual_head_model

def smoke_test_training():
    print("Starting smoke test for training pipeline...")
    
    # We can't really run fit() without data and tensorflow, 
    # but we can test model creation and compilation.
    
    try:
        # 1. Test Stage 1 model creation and compilation
        model = build_dual_head_model(freeze_base=True)
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
            loss={
                "cls_output": "categorical_crossentropy",
                "seg_output": bce_dice_loss
            },
            loss_weights={"cls_output": 1.0, "seg_output": 2.0},
            metrics={"cls_output": "accuracy", "seg_output": "accuracy"}
        )
        print("Stage 1 model compiled successfully.")
        
        # 2. Test saving and loading (simulating Stage 2)
        model_path = "tmp_stage1.keras"
        model.save(model_path)
        print(f"Model saved to {model_path}")
        
        loaded_model = tf.keras.models.load_model(model_path, custom_objects={"bce_dice_loss": bce_dice_loss})
        print("Model loaded successfully.")
        
        # 3. Test unfreezing
        from src.model import unfreeze_top_layers
        unfrozen_model = unfreeze_top_layers(loaded_model, num_layers=30)
        unfrozen_model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss={
                "cls_output": "categorical_crossentropy",
                "seg_output": bce_dice_loss
            },
            loss_weights={"cls_output": 1.0, "seg_output": 2.0},
            metrics={"cls_output": "accuracy", "seg_output": "accuracy"}
        )
        print("Stage 2 model compiled successfully.")
        
    finally:
        if os.path.exists("tmp_stage1.keras"):
            os.remove("tmp_stage1.keras")

if __name__ == "__main__":
    smoke_test_training()
