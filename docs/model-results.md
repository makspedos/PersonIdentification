# Model Results

The original experiments compared CoAtNet, ConvNeXt, and Swin-style transformer models for facial attribute estimation.

## Summary

| Task | Best reported model | Metric summary |
| --- | --- | --- |
| Age regression | ConvNeXt | MAE 4.95, MSE 51.13 |
| Gender classification | ConvNeXt | Accuracy 0.947, F1 0.948 |
| Emotion classification | ConvNeXt | Accuracy 0.848, F1 0.85 |

## Full Comparison

| Task | CoAtNet |   Swin | ConvNeXt |
| --- |--------:|-------:|---------:|
| Age MAE |    5.37 |   5.64 |     4.95 |
| Age MSE |   57.49 |  64.12 |    51.13 |
| Gender accuracy |    0.93 |  0.934 |    0.947 |
| Gender F1 |   0.933 |  0.939 |    0.948 |
| Emotion accuracy |    0.82 |  0.836 |    0.848 |
| Emotion F1 |    0.83 |   0.84 |     0.85 |

## Notes

- The notebooks were run in Kaggle/Colab-style GPU environments.
- Datasets and trained checkpoints are not committed to this repository.
- The app currently expects exported Keras `.h5` models for local inference.
- A future cleanup step should add a reproducible export path from notebook experiments to runtime inference.