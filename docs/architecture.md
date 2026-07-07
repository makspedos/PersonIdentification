# Architecture

## Overview

The project has two main parts:

- `django_app/`: a Django application for image upload, face detection, inference, and saved user results.
- `notebooks/`: experiment notebooks used to train and compare facial attribute models.

## Runtime Flow

1. A user uploads an image or provides an image URL.
2. The app stores the image under Django `MEDIA_ROOT`.
3. OpenCV detects faces using a Haar cascade.
4. Each detected face is resized to `224x224`.
5. Local Keras models or optional Azure ML inference return selected attributes.
6. The processed image and prediction table are rendered in the Django UI.
7. Authenticated users can save results to the database.

## Main Django Modules

- `config/`: Django settings, URL routing, ASGI/WSGI entrypoints, and custom storage.
- `web/`: upload form, prediction views, result persistence, static CSS/JS, and templates.
- `accounts/`: account/profile views and saved-result pages.
- `ml/`: runtime prediction wrapper and face-detection assets.
- `azure_deploy/`: Azure ML deployment scripts kept as optional reference material.

## Boundaries

Training notebooks are treated as research artifacts. The app should depend on exported model files, not notebook state.