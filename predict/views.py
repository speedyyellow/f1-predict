import time
import datetime
import threading

from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Sum
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page

from .models import Season,SeasonRound,TeamDriver,RaceResult,ResultPosition,Team,Prediction,PredictionPosition,FinishingPosition
from .forms import PredictionForm, PredictionPositionForm, ResultForm, ResultPositionForm

from graphos.sources.model import SimpleDataSource
from graphos.renderers import gchart

from timeit import default_timer as timer
#-------------------------------------------------------------------------------
#   globals
#-------------------------------------------------------------------------------
global_results = {}
global_champs = {}
global_graphs = {}

#-------------------------------------------------------------------------------
#   Views
#-------------------------------------------------------------------------------

def index(request):
    context = get_context(request)
    return render(request, 'predict/index.html', context)


def season_overview(request, season_id):
    # get the season context
    context = get_context_season(request, season_id)
    # add the extras
    season_results = get_race_results(season_id)
    context['race_list'] = season_results

    # generate all the data
    generate_results_data(season_id,season_results)
    # populate the table into the context
    t = results_table(season_id, season_results)
    if t != None:
        context['season_results'] = t
    # populate the graph data into the context
    data = results_graph(season_id, season_results)
    if data != None:
        Chart = gchart.LineChart(SimpleDataSource(data=data), html_id="line_chart", options={'title': '', 'legend':{'position':'bottom'}, 'pointsVisible':'true'})
        context['chart'] = Chart

    return render(request, 'predict/season_overview.html', context)

def season_overview_bbcode(request, season_id):
    # get the season context
    context = get_context_season(request, season_id)
    # add the extras
    season_results = get_race_results(season_id)
    context['race_list'] = season_results
    t = results_table(season_id, season_results)
    if t != None:
        context['season_results'] = t

    return render(request, 'predict/season_overview_bbcode.html', context)


def driver_championship(request, season_id):
    # get the season context
    context = get_context_season(request, season_id)
    # add the extras
    context['driver_champ'] = get_drivers_champ(season_id)
    return render(request, 'predict/driver_champ.html', context)


def constructor_championship(request, season_id):
    # get the season context
    context = get_context_season(request, season_id)
    # add the extras
    context['team_champ'] = get_constructors_champ(season_id)
    return render(request, 'predict/team_champ.html', context)


def calendar(request, season_id):
    # get the season context
    context = get_context_season(request, season_id)
    # add the extras
    context['race_list'] = get_season_rounds(season_id)
    return render(request, 'predict/calendar.html', context)


def entry_list(request, season_id):
    # get the season context
    context = get_context_season(request, season_id)
    # add the extras
    context['team_list'] = get_entry_list(season_id)
    return render(request, 'predict/entry_list.html', context)



def race_overview(request, season_id, country_id):
    # get the season context
    context = get_context_season(request, season_id)

    # add this seasons data
    race = get_season_round(season_id, country_id)
    context.update(get_context_race(request, race, ""))

    # add last seasons result
    last_season_id = str(int(season_id)-1)
    last_season_race = get_season_round(last_season_id, country_id)
    context.update(get_context_race(request, last_season_race, "last_"))

    result = get_race_result(season_id, country_id)

    table = []

    if result != None:
        result_positions = get_race_result_positions(result)
        pred = get_user_prediction(request.user, result.season_round)
        pred_positions = get_prediction_positions(pred)
        loopcount = 0
        for pos in result_positions:
            row = []
            row.append(pos.position.position)
            row.append(pos.position.points)
            row.append(pos.driver.driver.name)
            row.append(pos.driver.driver.pk)
            row.append(pos.driver.team.name)
            row.append(pos.driver.team.pk)
            if pred_positions != None and loopcount < pred_positions.count():
                row.append(pred_positions[loopcount].driver.driver.name)
                row.append(pred_positions[loopcount].driver.driver.pk)
            else:
                row.append("")
                row.append("")
            loopcount += 1
            table.append( row )
        table.sort()

    context['table'] = table

    return render(request, 'predict/race_overview.html', context)


def team_overview(request, season_id, team_id):
    team = Team.objects.get(pk=team_id)
    drivers = get_team_drivers(season_id, team)
    results = get_team_result_positions(season_id, team)
    context = get_context_season(request, season_id)
    context['driver_list'] = drivers
    context['result_list'] = results
    return render(request, 'predict/team_overview.html', context)


def driver_overview(request, season_id, driver_id):
    driver = get_driver(season_id, driver_id)
    results = get_driver_results(season_id, driver_id)
    context = get_context_season(request, season_id)
    context['driver'] = driver
    context['result_list'] = results
    return render(request, 'predict/driver_overview.html', context)

@login_required
def user_profile(request, user_id):
    season_id = get_year()
    context = get_context_season(request, season_id)

    prediction = get_latest_user_prediction(request.user, season_id)
    predictions = get_prediction_positions(prediction)

    if request.method == "POST":
        form = PredictionForm(season_id, request.POST)
        pforms = [PredictionPositionForm(season_id, request.POST, prefix=str(x), instance=PredictionPosition(), label_suffix=" "+str(x)) for x in range(1,11)]
        if form.is_valid() and all([pf.is_valid() for pf in pforms]):
            pred = form.save(commit=False)
            pred.user = request.user
            pred.created = timezone.now()
            pred.save()
            pos = 1
            for pf in pforms:
                new_pos = pf.save(commit=False)
                new_pos.prediction = pred
                new_pos.position = FinishingPosition.objects.get(position=pos)
                pos +=1
                new_pos.save()

    else:
        if prediction == None:
            form = PredictionForm(season_id, instance=Prediction(), label_suffix='')
            pforms = [PredictionPositionForm(season_id, prefix=str(x), instance=PredictionPosition(), label_suffix=" "+str(x)) for x in range(1,11)]
        else:
            form = PredictionForm(season_id, instance=prediction, label_suffix='')
            pforms = [PredictionPositionForm(season_id, prefix=str(p.position.position), instance=p, label_suffix=" "+str(p.position.position)) for p in predictions]

    context['form'] = form
    context['pforms'] = pforms
    return render(request, 'predict/user_profile.html', context)


@login_required
def add_result(request, season_id, country_id):
    context = get_context_season(request, season_id)
    sround = get_season_round(season_id, country_id)
    context.update(get_context_race(request, sround, ""))

    result = get_race_result(season_id, country_id)
    result_positions = get_race_result_positions(result)

    if request.method == "POST":
        # process the form
        form = ResultForm(season_id, request.POST)
        pforms = [ResultPositionForm(season_id, request.POST, prefix=str(x), instance=ResultPosition(), label_suffix=" "+str(x)) for x in range(1,23)]
        if form.is_valid() and all([pf.is_valid() for pf in pforms]):
            result = form.save(commit=False)
            result.season_round = sround
            result.save()
            pos = 1
            for pf in pforms:
                try:
                    new_pos = pf.save(commit=False)
                    new_pos.result = result
                    new_pos.position = FinishingPosition.objects.get(position=pos)
                    pos +=1
                    if new_pos.driver != None:
                        new_pos.save()
                except Exception, e:
                    print e
            # added a new result, regenerate the results & championship tables
            rebuild_results(season_id)
            rebuild_championships(season_id)

    else:
        if result == None:
            form = ResultForm(season_id, instance=RaceResult(), label_suffix='')
            pforms = [ResultPositionForm(season_id, prefix=str(x), instance=ResultPosition(), label_suffix=" "+str(x)) for x in range(1,23)]
        else:
            form = ResultForm(season_id, instance=result, label_suffix='')
            pforms = [ResultPositionForm(season_id, prefix=str(r.position.position), instance=r, label_suffix=" "+str(r.position.position)) for r in result_positions]

    context['form'] = form
    context['pforms'] = pforms
    return render(request, 'predict/result.html', context)


def get_year():
    return timezone.now().strftime("%Y")

#-------------------------------------------------------------------------------
#   Score calculations
#-------------------------------------------------------------------------------

def score_season(user, season_id):
    score = 0
    # get the season results
    results = get_race_results(season_id)
    if results != None:
        for res in results:
            # get the user's prediction for this round
            pred = get_user_prediction(user, res.season_round)
            score += score_round(pred, res)

    return score;

def score_results(user, results):
    score = 0
    if results != None:
        for res in results:
            # get the user's prediction for this round
            pred = get_user_prediction(user, res.season_round)
            score += score_round(pred, res)

    return score;

def score_round(prediction, race_result, top_ten=None):
    score = 0
    if prediction == None:
        return score
    if race_result == None:
        return score

    # pole & fastest lap get 5 points each
    if prediction.pole_position == race_result.pole_position:
        score += 5
    if prediction.fastest_lap == race_result.fastest_lap:
        score += 5

    # get the prediction positions & race positions
    prediction_pos = get_prediction_positions(prediction)
    if top_ten == None:
        top_ten = get_race_result_top_ten(race_result)

    # now check for position matches
    for ppos in prediction_pos:
        for rpos in top_ten:
            if ppos.driver == rpos.driver:
                # the prediction has a driver in the top 10
                score += 1
                if ppos.position == rpos.position:
                    # the prediction has the driver in the correct position
                    score += 4
                    if ppos.position.position == 1:
                        # and got the winner right
                        score += 5

    return score

def rebuild_results(season_id):
    if season_id in global_results:
        del global_results[season_id]
    if season_id in global_graphs:
        del global_graphs[season_id]

    generate_results_data(season_id)

def score_prediction(lock, user_scores, prediction, result, top_ten, previous_rounds):
    lock.acquire()
    try:
        score = score_round(prediction,result,top_ten)
        if prediction.user in user_scores:
            #print("appending score to " + prediction.user.username +"\n")
            user_scores[prediction.user].append(score)
        else:
            # add 0's for the previous rounds where this user didnt have a prediction
            #print("inserting new score for " + prediction.user.username +"\n")
            if previous_rounds > 0:
                user_scores[prediction.user] = [0] * previous_rounds
                user_scores[prediction.user].append(score)
            else:
                user_scores[prediction.user] = [score]
    finally:
        lock.release()

def generate_user_scores(season_id, results=None):
    #start = timer()
    # get all the race reults for this season
    if results == None:
        results = get_race_results(season_id)

    if results != None:
        # calculate scores for all users & races
        user_scores = {}
        previous_rounds = 0
        for r in results:
#            start_loop = timer()
            top_ten = get_race_result_top_ten(r)
            preds = get_race_predictions(r.season_round)
            threads = []
            lock = threading.Lock()
            for p in preds:
                #score_prediction(lock, user_scores, p, r, top_ten, previous_rounds)
                t = threading.Thread(target=score_prediction, args=(lock, user_scores, p, r, top_ten, previous_rounds))
                threads.append(t)
                t.start()

            # wait for our threads to finish
            for t in threads:
                t.join()

            previous_rounds += 1
#            end_loop = timer()
#            print("processed result: "+str(end_loop - start_loop))

        #end = timer()
        #print("user_scores: "+str(end - start))
        return user_scores


def generate_results_data(season_id, results=None, user_scores=None):
    # get all the race reults for this season
    if results == None:
        results = get_race_results(season_id)

    if results != None:
        # calculate scores for all users & races
        if user_scores == None:
            user_scores = generate_user_scores(season_id, results)

        # construct the results table
        table = []
        for user, scores in user_scores.iteritems():
            season_score = 0
            for s in scores:
                season_score += s

            table.append( (season_score, user, scores) )

        table.sort()
        table.reverse()

        # construct the data table for the graph
        # Round | User1 | user 2
        # AU    | 25    | 34
        graph_data = []
        for r in results:
            graph_data.append([r.season_round.circuit.country_code])
        header = ['Round',]
        for user, scores in user_scores.iteritems():
            header.append(user.username)
            total = 0
            for i, score in enumerate(scores):
                total += score
                graph_data[i].append(total)
        graph_data.insert(0, header)

        # cache the data for later use
        global_results[season_id] = table
        global_graphs[season_id] = graph_data

def results_table(season_id, results=None):
    # rebuild the data
    #if season_id not in global_results:
    #generate_results_data(season_id,results)

    # return the data
    if season_id in global_results:
        return global_results[season_id]
    else:
        return None

def results_graph(season_id, results=None):
    # rebuild the data
    #if season_id not in global_graphs:
    #generate_results_data(season_id,results)

    # return the data
    if season_id in global_graphs:
        return global_graphs[season_id]
    else:
        return None

#-------------------------------------------------------------------------------
#   Championship calculations
#-------------------------------------------------------------------------------
def rebuild_championships(season_id):
    if season_id+"driver" in global_champs:
        del global_champs[season_id+"driver"]
    if season_id+"constructor" in global_champs:
        del global_champs[season_id+"constructor"]

    get_drivers_champ(season_id)
    get_constructors_champ(season_id)

def get_drivers_champ(season_id):
    key = season_id+"driver"
    if key not in global_champs:
        results = ResultPosition.objects.filter(result__season_round__season__name=season_id).values('driver__driver__name','driver__driver__pk','result__season_round__season__name').annotate(score = Sum('position__points')).order_by('-score')
        global_champs[key] = get_champ(results, 'driver__driver__name', 'driver__driver__pk')

    return global_champs[key]

def get_constructors_champ(season_id):
    key = season_id+"constructor"
    if key not in global_champs:
        results = ResultPosition.objects.filter(result__season_round__season__name=season_id).values('driver__team__name','driver__team__pk','result__season_round__season__name').annotate(score = Sum('position__points')).order_by('-score')
        global_champs[key] = get_champ(results, 'driver__team__name', 'driver__team__pk')

    return global_champs[key]

def get_champ(results, name_field, key_field):
    champ = []
    rank = 0
    counter = 0
    high_score = 0
    last_score = 1000
    for res in results:
        counter += 1
        if res['score'] > 0:
            if res['score'] < last_score:
                rank = counter
            if high_score == 0:
                high_score = res['score']

            entry = {'rank' : rank,
                     'name' : res[name_field],
                     'key'  : res[key_field],
                     'score' : res['score'],
                     'season' : res['result__season_round__season__name'],
                     'gap' : high_score - res['score']}
            champ.append(entry)
            last_score = res['score']

    return champ

def get_context(request):
    context = {'user': request.user, 'season_list': get_season_list()}
    return context

def get_context_season(request, season_id):
    context = get_context(request)
    season = Season.objects.filter(name=season_id)
    if season.count > 0:
        context['season'] = season
    return context

def get_context_race(request, season_round, prefix):
    context = {prefix+'round_score' : 0}
    if season_round != None:
        context[prefix+'race'] = season_round
        result = get_race_result(season_round.season.name, season_round.circuit.country)
        if result != None:
            result_positions = get_race_result_positions(result)
            pred = get_user_prediction(request.user, result.season_round)
            pred_positions = get_prediction_positions(pred)
            score = score_round(pred, result)
            context[prefix+'result'] = result
            context[prefix+'results'] = result_positions
            context[prefix+'prediction'] = pred
            context[prefix+'predictions'] = pred_positions
            context[prefix+'round_score'] = score
    return context


def get_season_list():
    return Season.objects.order_by('-name')

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

def get_team_result_positions(season_id, team):
    results = ResultPosition.objects.filter(result__season_round__season__name=season_id).filter(driver__team__pk=team.pk).order_by('result__season_round__race_date','position__position')
    return results

def get_race_results(season_id):
    results = RaceResult.objects.filter(season_round__season__name=season_id).order_by('season_round__race_date')
    if results.count() > 0:
        return results
    else:
        return None

def get_last_three_race_results(season_id):
    results = RaceResult.objects.filter(season_round__season__name=season_id).order_by('season_round__race_date')
    if results.count() > 0:
        return results[results.count()-3:]
    else:
        return None

def get_race_result(season_id, country_id):
    results = RaceResult.objects.filter(season_round__season__name=season_id, season_round__circuit__country=country_id)[:1]
    if results.count() >= 1:
        return results[0]
    else:
        return None

def get_season_round(season_id, country_id):
    races = SeasonRound.objects.filter(season__name=season_id, circuit__country=country_id)[:1]
    if races.count() >= 1:
        return races[0]
    else:
        return None

def get_season_rounds(season_id):
    return SeasonRound.objects.filter(season__name=season_id).order_by('race_date')

def get_race_result_positions(result):
    if result != None:
        positions = ResultPosition.objects.filter(result__pk=result.pk).order_by('position__position')
        return positions
    else:
        return None

def get_race_result_top_ten(result):
    return get_race_result_positions(result)[:10]

def get_user_prediction(user, season_round):
    try:
        prediction = Prediction.objects.filter(user__pk=user.pk, created__lt=season_round.event_date).latest('pk')
        return prediction
    except Exception, e:
        return None

def get_race_predictions(season_round):
    try:
        begin = season_round.season.name+"-01-01"
        predictions = Prediction.objects.filter(created__gte=begin, created__lt=season_round.event_date).values('user').annotate(pred_key=Max('pk')).values('pred_key')

        ids = []
        for p in predictions:
            ids.append(p['pred_key'])

        predictions = Prediction.objects.filter(pk__in=ids).order_by('user')
        #print pred_positions.query
        return predictions
    except Exception, e:
        return None

def get_latest_user_prediction(user, season_id):
    try:
        # create year bounds for the query
        print season_id
        begin   = season_id+"-01-01"
        end     = season_id+"-12-31"
        prediction = Prediction.objects.filter(user__pk=user.pk,created__gte=begin, created__lte=end).latest('pk')
        return prediction
    except Exception, e:
        print e
        return None

def get_prediction_positions(prediction):
    try:
        pred_positions = PredictionPosition.objects.filter(prediction__pk=prediction.pk).order_by('position__position')[:10]
        return pred_positions
    except Exception, e:
        return None

def get_prediction_positions_for_keys(prediction_keys):
    try:
        pred_positions = PredictionPosition.objects.filter(prediction__pk__in=prediction_keys).order_by('prediction__user__username','position__position')
        return pred_positions
    except Exception, e:
        return None

def get_active_users(season_id):
    begin   = season_id+"-01-01"
    end     = season_id+"-12-31"
    predictions = Prediction.objects.filter(created__gte=begin, created__lte=end)
    userset = []
    for p in predictions:
        userset.append(p.user)
    return set(userset)
