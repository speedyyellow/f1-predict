from django.forms import ModelForm
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from predict.models import Prediction, PredictionPosition


class PredictionPositionForm(ModelForm):
    class Meta:
        model = PredictionPosition
        fields = {'driver'}
        labels = {'driver' : _(' '),}


class PredictionForm(ModelForm):
    class Meta:
        model = Prediction
        fields = {'pole_position', 'fastest_lap'}
        labels = {'pole_position' : _('Pole Position'),'fastest_lap' : _('Fastest Lap'),}


