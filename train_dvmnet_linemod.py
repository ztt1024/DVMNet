from types import SimpleNamespace
import yaml
import os
from lightning.pytorch.callbacks import ModelCheckpoint, StochasticWeightAveraging
import lightning.pytorch as pl
from modules.dvmnet_objaverse import training_lm, Estimator

def main(cfg):
    cfg["RUN_NAME"] = 'Objaverse_DVMNet'
    cfg["DATA"]["ACC_THR"] = 15
    cfg["TRAIN"]["BS"] = 64
    cfg["TRAIN"]["LR"] = 1e-4
    cfg["TRAIN"]["MAX_EPOCH"] = 1
    cfg["TRAIN"]["STEP_SIZE"] = 1
    cfg["DATA"]["BG"] = True
    cfg["TRAIN"]["BG_RATIO"] = 0.5
    cfg["TRAIN"]["FREEZE"] = False
    cfg["TRAIN"]["PRETRAIN"] = True
    cfg["NETWORK"]["MASK"] = "both"
    cfg["NETWORK"]["LOSS"] = "both"

    print(cfg)

    checkpoint_callback = ModelCheckpoint(monitor='train_loss', mode='min', dirpath=os.path.join("./models", cfg["RUN_NAME"]), filename="checkpoint_lm")

    trainer = pl.Trainer(accelerator="auto", devices="auto", strategy="ddp_find_unused_parameters_true", accumulate_grad_batches=1,
        max_epochs=cfg["TRAIN"]["MAX_EPOCH"], sync_batchnorm=True, limit_train_batches=cfg["TRAIN"]["SAMPLE_RATE"],
        callbacks=[checkpoint_callback])

    training_lm(cfg, trainer)

if __name__ == '__main__':
    with open("./config.yaml", 'r') as load_f:
        cfg = yaml.load(load_f, Loader=yaml.FullLoader)
    load_f.close()

    main(cfg)
