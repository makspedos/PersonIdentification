import logging
from pathlib import Path

import requests
from django.conf import settings
from django.shortcuts import redirect, render

from config.custom_storage import CustomFileSystemStorage
from web.clean import clean_temp
from web.forms import FaceForm
from web.models import Identification, ImageFaces
from web.saved_img_mover import moving_files


logger = logging.getLogger(__name__)
_prediction_model = None

PARAM_AGE = "age"
PARAM_GENDER = "gender"
PARAM_EMOTION = "emotion"

EMOTION_LABELS = [
    ("anger", "Anger"),
    ("happy", "Happy"),
    ("neutral", "Neutral"),
    ("sad", "Sad"),
    ("surprise", "Surprise"),
]


def get_prediction_model():
    """Lazily create the prediction wrapper so startup does not require ML deps."""
    global _prediction_model
    if _prediction_model is None:
        from ml.prediction_model import PredictionModel

        _prediction_model = PredictionModel()
    return _prediction_model


def requested_params(post_data):
    """Extract selected prediction targets from the submitted form data."""
    return {
        PARAM_AGE: post_data.get(PARAM_AGE),
        PARAM_GENDER: post_data.get(PARAM_GENDER),
        PARAM_EMOTION: post_data.get(PARAM_EMOTION),
    }


def home(request):
    """Render the application landing page."""
    return render(request, "html/all/home.html")


def help_page(request):
    """Render usage guidance for the image analysis workflow."""
    return render(request, "html/all/help.html")


def form_page(request):
    """Collect an uploaded image or URL and store it in the session."""
    form = FaceForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            clean_temp()
            request.session["params"] = requested_params(request.POST)
            upload_dir = Path(settings.MEDIA_ROOT) / "faces"
            upload_dir.mkdir(parents=True, exist_ok=True)

            if "img" in request.FILES:
                img = request.FILES["img"]
                fs = CustomFileSystemStorage(location=upload_dir)
                filename = fs.save("face_original.png", img)
                request.session["img"] = {
                    "image_path": str(upload_dir / filename),
                    "image_url": f"{settings.MEDIA_URL}faces/{filename}",
                }

            image_url = form.cleaned_data.get("image_url")
            if image_url:
                destination = upload_dir / "face_original.png"
                if not download_image(image_url, destination):
                    return redirect("web:form_page")
                request.session["img"] = {
                    "image_path": str(destination),
                    "image_url": f"{settings.MEDIA_URL}faces/face_original.png",
                }

            return redirect("web:work_page")

    return render(request, "html/all/form.html", {"form": form})


def download_image(url, save_path):
    """Download a remote image into the temporary media folder."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            file.write(response.content)
        logger.info("Image downloaded successfully from %s", url)
        return True
    except requests.RequestException as exc:
        logger.warning("Could not download image from %s: %s", url, exc)
        return False


def work_page(request):
    """Run face analysis and optionally persist results for signed-in users."""
    params = request.session.get("params")
    img = request.session.get("img")

    if not params or not img:
        return redirect("web:form_page")

    result = get_prediction_model().face_detection(params, img)
    if result is False:
        return render(request, "html/all/work_page.html", {"image": False})

    result_list, col_list = result
    context = {
        "image": f"{settings.MEDIA_URL}faces/face.png",
        "result_list": result_list,
        "col_list": col_list,
        "list_emotions": False,
    }

    if PARAM_EMOTION in col_list:
        context["list_emotions"] = [label for _, label in EMOTION_LABELS]

    if "save_identification" in request.POST:
        image_face = ImageFaces.objects.create(user=request.user, img=moving_files())
        for count, result_item in enumerate(result_list, start=1):
            emotion = "not_selected"
            emotion_value = result_item.get(PARAM_EMOTION)
            if isinstance(emotion_value, list):
                try:
                    emotion_scores = [float(score) for score in emotion_value]
                except (TypeError, ValueError):
                    emotion_scores = []
                if emotion_scores:
                    max_value = max(emotion_scores)
                    emotion = EMOTION_LABELS[emotion_scores.index(max_value)][0]

            age_value = result_item.get(PARAM_AGE)
            if not isinstance(age_value, int):
                age_value = None

            gender_value = result_item.get(PARAM_GENDER, "not_selected")
            if gender_value not in {"male", "female", "not_selected"}:
                gender_value = "not_selected"

            Identification.objects.create(
                image_face=image_face,
                age=age_value,
                gender=gender_value,
                emotion=emotion,
                face_number=count,
            )

        return redirect("web:form_page")

    return render(request, "html/all/work_page.html", context)