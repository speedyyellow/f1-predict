from django.contrib import admin

# Register your models here.
from .models import Circuit
from .models import Driver
from .models import Team
from .models import Season
from .models import SeasonRound
from .models import TeamDriver
from .models import RaceResult
from .models import ResultPosition
from .models import FinishingPosition
from .models import Prediction
from .models import PredictionPosition

# season stuff
class RoundInline(admin.TabularInline ):
    model = SeasonRound
    extra = 3

class TeamDriverInline(admin.TabularInline ):
    model = TeamDriver
    fields = ['team', 'driver']
    extra = 3

class SeasonAdmin(admin.ModelAdmin):
    inlines = [RoundInline,TeamDriverInline]


# results page
class ResultPositionInline(admin.TabularInline ):
    model = ResultPosition
    extra = 20

class ResultAdmin(admin.ModelAdmin):
    inlines = [ResultPositionInline]

# prediction page
class PredictionPositionInline(admin.TabularInline ):
    model = PredictionPosition
    extra = 10

class PredictionAdmin(admin.ModelAdmin):
    inlines = [PredictionPositionInline]


admin.site.register(Circuit)
admin.site.register(Driver)
admin.site.register(Team)
admin.site.register(FinishingPosition)
admin.site.register(Season, SeasonAdmin)
admin.site.register(RaceResult, ResultAdmin)
admin.site.register(Prediction, PredictionAdmin)

