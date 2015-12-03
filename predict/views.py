from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Season,SeasonRound,TeamDriver,RaceResult,ResultPosition,Team,Prediction,PredictionPosition

#-------------------------------------------------------------------------------
#   Views
#-------------------------------------------------------------------------------

@login_required
def index(request):
    season_list = Season.objects.order_by('name')
    context = {'season_list': season_list}
    return render(request, 'predict/index.html', context)

@login_required
def season_overview(request, season_id):
    season = Season.objects.filter(name=season_id)
    race_list = get_races(season_id)
    team_list = get_entry_list(season_id)
    dc = get_drivers_champ(season_id)
    cc = get_constructors_champ(season_id)
    score = score_season(request.user, season[0])
    context = {'season': season,
                'race_list': race_list,
                'team_list' : team_list,
                'driver_champ' : dc,
                'team_champ' : cc,
                'score' : score }
    return render(request, 'predict/season_overview.html', context)

@login_required
def race_overview(request, season_id, country_id):
    race = get_race(season_id, country_id)
    result = get_race_result(season_id, country_id)
    pred = get_user_prediction(request.user, race)
    result_positions = get_race_result_positions(result)
    score = score_round(pred, result)
    context = {'race' : race,
                'results' : result_positions,
                'score' : score }
    return render(request, 'predict/race_overview.html', context)

@login_required
def team_overview(request, season_id, team_id):
    team = Team.objects.get(pk=team_id)
    drivers = get_team_drivers(season_id, team)
    results = get_team_results(season_id, team)
    context = {'team' : team,
               'driver_list' : drivers,
               'result_list' : results }
    return render(request, 'predict/team_overview.html', context)

@login_required
def driver_overview(request, season_id, driver_id):
    driver = get_driver(season_id, driver_id)
    results = get_driver_results(season_id, driver_id)
    context = {'driver' : driver,
               'result_list' : results }
    return render(request, 'predict/driver_overview.html', context)

#-------------------------------------------------------------------------------
#   Query wrappers
#-------------------------------------------------------------------------------
def get_entry_list(season_id):
    team_list = TeamDriver.objects.filter(season__name=season_id).order_by('team__name', 'driver__name')
    return team_list

def get_driver(season_id, driver_id):
    drivers = TeamDriver.objects.filter(season__name=season_id, driver__pk=driver_id)
    return drivers[0]

def get_driver_results(season_id, driver_id):
    results = ResultPosition.objects.filter(result__season_round__season__name=season_id,driver__driver__pk=driver_id)
    return results

def get_team_drivers(season_id, team):
    drivers = TeamDriver.objects.filter(season__name=season_id, team__pk=team.pk)
    return drivers

def get_team_results(season_id, team):
    results = ResultPosition.objects.filter(result__season_round__season__name=season_id).filter(driver__team__pk=team.pk).order_by('result__season_round__date','position__position')
    return results

def get_race_results(season):
    results = RaceResult.objects.filter(season_round__season__name=season.name).order_by('season_round__date')
    return results

def get_race_result(season_id, country_id):
    results = RaceResult.objects.filter(season_round__season__name=season_id, season_round__circuit__country=country_id)[:1]
    return results[0]

def get_race(season_id, country_id):
    races = SeasonRound.objects.filter(season__name=season_id, circuit__country=country_id)[:1]
    return races[0]

def get_races(season_id):
    return SeasonRound.objects.filter(season__name=season_id).order_by('date')

def get_race_result_positions(result):
    positions = ResultPosition.objects.filter(result__season_round__season__pk=result.season_round.season.pk, result__pk=result.pk).order_by('position__position')[:10]
    return positions

def get_user_prediction(user, season_round):
    try:
        prediction = Prediction.objects.filter(user__pk=user.pk, created__lte=season_round.date).latest('created')
        return prediction
    except Exception, e:
        return Prediction()

def get_prediction_positions(prediction):
    pred_positions = PredictionPosition.objects.filter(prediction__pk=prediction.pk).order_by('position__position')[:10]
    return pred_positions

#-------------------------------------------------------------------------------
#   Score calculations
#-------------------------------------------------------------------------------

def score_season(user, season):
    score = 0
    # get the season results
    results = get_race_results(season)
    for res in results:
        # get the user's prediction for this round
        pred = get_user_prediction(user, res.season_round)
        score += score_round(pred, res)

    return score;

def score_round(prediction, race_result):
    score = 0

    # pole & fastest lap get 5 points each
    if prediction.pole_position == race_result.pole_position:
        score += 5
    if prediction.fastest_lap == race_result.fastest_lap:
        score += 5

    # get the prediction positions & race positions
    prediction_pos = get_prediction_positions(prediction)
    result_pos = get_race_result_positions(race_result)

    # now check for position matches
    for ppos in prediction_pos:
        for rpos in result_pos:
            if ppos.driver == rpos.driver:
                # the prediction has a driver in the top 10
                score += 1
                if ppos.position == rpos.position:
                    # the prediction has the driver in the correct position
                    score += 4

    return score

#-------------------------------------------------------------------------------
#   Championship calculations
#-------------------------------------------------------------------------------
def get_drivers_champ(season_id):
    results = ResultPosition.objects.filter(result__season_round__season__name=season_id).values('driver__driver__name','driver__driver__pk','result__season_round__season__name').annotate(score = Sum('position__points')).order_by('-score')
    return get_champ(results, 'driver__driver__name', 'driver__driver__pk')

def get_constructors_champ(season_id):
    results = ResultPosition.objects.filter(result__season_round__season__name=season_id).values('driver__team__name','driver__team__pk','result__season_round__season__name').annotate(score = Sum('position__points')).order_by('-score')
    return get_champ(results, 'driver__team__name', 'driver__team__pk')

def get_champ(results, name_field, key_field):
    champ = []
    rank = 0
    last_score = 1000
    for res in results:
        if res['score'] > 0:
            if res['score'] < last_score:
                rank += 1
            entry = {'rank' : rank,
                     'name' : res[name_field],
                     'key'  : res[key_field],
                     'score' : res['score'],
                     'season' : res['result__season_round__season__name']}
            champ.append(entry)
            last_score = res['score']

    return champ
