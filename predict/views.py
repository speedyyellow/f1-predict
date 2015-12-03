from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Season,SeasonRound,TeamDriver,RaceResult,ResultPosition,Team,Prediction,PredictionPosition

# Create your views here.
@login_required
def index(request):
    season_list = Season.objects.order_by('name')
    context = {'season_list': season_list}
    return render(request, 'predict/index.html', context)

@login_required
def season_overview(request, season_id):
    season = Season.objects.filter(name=season_id)
    race_list = SeasonRound.objects.filter(season__name=season_id).order_by('date')
    team_list = TeamDriver.objects.filter(season__name=season_id).order_by('team__name', 'driver__name')
    driver_champ = ResultPosition.objects.filter(result__season_round__season__name=season_id).values('driver__driver__name','driver__driver__pk','result__season_round__season__name').annotate(score = Sum('position__points')).order_by('-score')
    team_champ = ResultPosition.objects.filter(result__season_round__season__name=season_id).values('driver__team__name','driver__team__pk','result__season_round__season__name').annotate(score = Sum('position__points')).order_by('-score')
    score = score_season(request.user, season[0])
    context = {'season': season,
                'race_list': race_list,
                'team_list' : team_list,
                'driver_champ' : driver_champ,
                'driver_count' : driver_champ.count,
                'team_champ' : team_champ,
                'score' : score }
    return render(request, 'predict/season_overview.html', context)

@login_required
def race_overview(request, season_id, country_id):
	race = SeasonRound.objects.filter(season__name=season_id, circuit__country=country_id)[:1]
	pred = Prediction.objects.filter(user__pk=request.user.pk, created__lte=race[0].date).order_by('created')[:1]
	res = RaceResult.objects.filter(season_round__season__name=season_id, season_round__circuit__country=country_id)[:1]
	score = 0;
	for r in res:
		for p in pred:
			score += score_round(p, r)

	results = ResultPosition.objects.filter(result__season_round__season__name=season_id, result__season_round__circuit__country=country_id)
	context = {'race' : race,
				'results' : results,
				'score' : score }
	return render(request, 'predict/race_overview.html', context)

@login_required
def team_overview(request, season_id, team_id):
    team = Team.objects.get(pk=team_id)
    drivers = TeamDriver.objects.filter(season__name=season_id, team__pk=team_id)
    results = ResultPosition.objects.filter(result__season_round__season__name=season_id).filter(driver__team__pk=team_id).order_by('result__season_round__date','position__position')
    context = {'team' : team,
               'driver_list' : drivers,
               'result_list' : results }
    return render(request, 'predict/team_overview.html', context)

@login_required
def driver_overview(request, season_id, driver_id):
    drivers = TeamDriver.objects.filter(season__name=season_id, driver__pk=driver_id)
    results = ResultPosition.objects.filter(result__season_round__season__name=season_id,driver__driver__pk=driver_id)
    context = {'driver_list' : drivers,
               'result_list' : results }
    return render(request, 'predict/driver_overview.html', context)

def get_user_prediction(user, season_round):
    prediction = Prediction.objects.filter(user__pk=user.pk, created__lte=season_round.date).order_by('created')[:1]
    return prediction

def score_season(user, season):
	score = 0
	# get the season results
	results = RaceResult.objects.filter(season_round__season__name=season.name).order_by('season_round__date')
	for res in results:
		# get the user's prediction for this round
		preds = get_user_prediction(user, res.season_round) #Prediction.objects.filter(user__pk=user.pk, created__lte=res.season_round.date).order_by('created')[:1]
		score += score_round(preds[0], res)

	return score;



def score_round(prediction, race_result):
 	score = 0

 	# pole & fastest lap get 5 points each
 	if prediction.pole_position == race_result.pole_position:
 		score += 5
 	if prediction.fastest_lap == race_result.fastest_lap:
 		score += 5

 	# get the prediction positions & race positions
 	prediction_pos = PredictionPosition.objects.filter(prediction__pk=prediction.pk).order_by('position__position')[:10]
 	result_pos = ResultPosition.objects.filter(result__season_round__season__pk=race_result.season_round.season.pk, result__pk=race_result.pk).order_by('position__position')[:10]

 	# now check for exact matches
 	for ppos in prediction_pos:
 		for rpos in result_pos:
			if ppos.driver == rpos.driver:
				score += 1
 				if ppos.position == rpos.position:
 					score += 4

 	return score
