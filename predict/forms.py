from django.forms import ModelForm
from django.forms import inlineformset_factory

from predict.models import Prediction, PredictionPosition


class PredictionPositionForm(ModelForm):
    class Meta:
        model = PredictionPosition
        fields = {'driver'}


class PredictionForm(ModelForm):
    class Meta:
        model = Prediction
        fields = {'pole_position', 'fastest_lap'}


