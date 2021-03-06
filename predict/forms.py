from django.forms import ModelForm, ModelChoiceField
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from predict.models import Prediction, PredictionPosition, TeamDriver, ResultPosition, RaceResult


class PredictionPositionForm(ModelForm):
    def __init__(self, season_id, *args, **kwargs):
        super(PredictionPositionForm, self).__init__(*args, **kwargs)
        self.fields['driver'] = ModelChoiceField(queryset=TeamDriver.objects.filter(season__name=season_id,active=True))

    class Meta:
        model = PredictionPosition
        fields = {'driver'}
        labels = {'driver' : _(' '),}


class PredictionForm(ModelForm):
    def __init__(self, season_id, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)
        self.fields['pole_position'] = ModelChoiceField(queryset=TeamDriver.objects.filter(season__name=season_id,active=True))
        self.fields['fastest_lap'] = ModelChoiceField(queryset=TeamDriver.objects.filter(season__name=season_id,active=True))

    class Meta:
        model = Prediction
        fields = {'pole_position', 'fastest_lap'}
        labels = {'pole_position' : _('Pole Position'),'fastest_lap' : _('Fastest Lap'),}


class ResultPositionForm(ModelForm):
    def __init__(self, season_id, *args, **kwargs):
        super(ResultPositionForm, self).__init__(*args, **kwargs)
        self.fields['driver'] = ModelChoiceField(queryset=TeamDriver.objects.filter(season__name=season_id,active=True), required=False)

    class Meta:
        model = ResultPosition
        fields = {'driver'}
        labels = {'driver' : _(' '),}


class ResultForm(ModelForm):
    def __init__(self, season_id, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        self.fields['pole_position'] = ModelChoiceField(queryset=TeamDriver.objects.filter(season__name=season_id,active=True))
        self.fields['fastest_lap'] = ModelChoiceField(queryset=TeamDriver.objects.filter(season__name=season_id,active=True))

    class Meta:
        model = RaceResult
        fields = {'pole_position', 'fastest_lap'}
        labels = {'pole_position' : _('Pole Position'),'fastest_lap' : _('Fastest Lap'),}
