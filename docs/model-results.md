# Model Results

The original experiments compared CoAtNet, ConvNeXt, and Swin-style transformer models for facial attribute estimation.

## Summary

| Task | Best reported model | Metric summary |
| --- | --- | --- |
| Age regression | ConvNeXt | MAE 4.95, MSE 51.13 |
| Gender classification | ConvNeXt | Accuracy 0.9475, F1 0.9489 |
| Emotion classification | ConvNeXt | Accuracy 0.848, F1 0.85 |

## Full Comparison

| Task | CoAtNet | Swin | ConvNeXt |
| --- | ---: | ---: | ---: |
| Age MAE | 5.37 | 5.64 | 4.95 |
| Age MSE | 57.49 | 64.12 | 51.13 |
| Gender accuracy | 0.9300 | 0.9348 | 0.9475 |
| Gender F1 | 0.9330 | 0.9390 | 0.9489 |
| Emotion accuracy | 0.8210 | 0.8360 | 0.8480 |
| Emotion F1 | 0.8300 | 0.8400 | 0.8500 |

## Notes

- The notebooks were run in Kaggle/Colab-style GPU environments.
- Datasets and trained checkpoints are not committed to this repository.
- The app currently expects exported Keras `.h5` models for local inference.
- A future cleanup step should add a reproducible export path from notebook experiments to runtime inference.