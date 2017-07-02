import json
from django.http import HttpResponse

from django.shortcuts import render
from apps.spt.models import Player
from apps.spt.models import Game
from apps.spt.models import Play
from apps.spt.models import Season
from django.views.generic import ListView
from apps.spt.dbutil import query_to_dicts


def stats(request):
    return render(request,'stats.html', {})
               
def index(request):

    seasonnumbertmp = ""
    selectedseason = "select MAX(seasonnumber) from spt_season"
    
    if request.method == "POST":
        seasonnumbertmp = request.POST.get("seasonnumber", "")
        if seasonnumbertmp != "":
            selectedseason = str(int(seasonnumbertmp) - 1)    
     
    currentstanding_list =  list(query_to_dicts("""
                        select
                        pl.firstname,
                        sum(gp.point) as points,
            sum(case when cast(gp.placement as int) >= 0 then 1 else 0 end) as totalgames,
            sum(case when cast(gp.placement as int) = 1 then 1 else 0 end) as firstplaces,
            sum(case when cast(gp.placement as int) = 2 then 1 else 0 end) as secondplaces,
            sum(case when cast(gp.placement as int) = 3 then 1 else 0 end) as thirdplaces,
            sum(case when cast(gp.placement as int) = 4 then 1 else 0 end) as forthplaces,
            sum(case when cast(gp.placement as int) = 0 then 1 else 0 end) as didnotplace,
            se.seasonnumber
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(""" + selectedseason + """) and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
            group by pl.firstname,se.seasonnumber
                        order by points desc,firstplaces desc,secondplaces desc,thirdplaces desc,forthplaces desc, pl.firstname
                        """))

    currentpoolamount_list = list(query_to_dicts("""
            select
                        (sum(gp.buyinamount) / 60 * 10) as poolamount,
                        (sum(gp.buyinamount) / 60 * 10 - plpa.buyintotal) as poolamountadjusted,
                        ((sum(gp.buyinamount) / 60 * 10 - plpa.buyintotal)  * .50) as firstplaceamount,
                        ((sum(gp.buyinamount) / 60 * 10 - plpa.buyintotal)  * .30) as secondplaceamount,
                        ((sum(gp.buyinamount) / 60 * 10 - plpa.buyintotal)  * .20) as thirdplaceamount,
                        plpa.buyintotal,
                        plpa.plleader
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se,
                        (select
                        pl.firstname as plleader,
                        se.seasonnumber,
                        sum(gp.point) as points,
                        (count(*) * 10) as buyintotal,
                        sum(case when cast(gp.placement as int) = 1 then 1 else 0 end) as firstplaces,
                        sum(case when cast(gp.placement as int) = 2 then 1 else 0 end) as secondplaces,
                        sum(case when cast(gp.placement as int) = 3 then 1 else 0 end) as thirdplaces,
                        sum(case when cast(gp.placement as int) = 4 then 1 else 0 end) as forthplaces
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(""" + selectedseason + """) and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
                        group by pl.firstname,se.seasonnumber
                        order by points desc, firstplaces desc, secondplaces desc, thirdplaces desc, forthplaces desc, pl.firstname limit 1) plpa
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(""" + selectedseason + """) and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
                        group by plpa.buyintotal, plpa.plleader
                        """))
    currentgame_list = list(query_to_dicts("""
            select
                        (count(*) / 2) as numberofgames,
            gm.seasons_id as seasonnumber
                        from spt_game gm, spt_season se
                        where
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(select MAX(seasonnumber) from spt_season) and
                        cast(gm.finalseasongame as int) = 0
            group by gm.seasons_id
                        """))
    newsflash_list = list(query_to_dicts("""
                        select newsflash
                        from spt_newsflash nf
                        where
                        nf.id=(select MAX(id) from spt_newsflash)
                        """))

    numberofcancelledgames_list = list(query_to_dicts("""
            select
             (count(*) / 2) as numberofcancelledgames
                        from spt_game gm, spt_season se
                        where
            cast(gm.cancelledgame as int)=1 and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(select MAX(seasonnumber) from spt_season)
             """))
    
    pll_list = list(query_to_dicts("""
            select 
            pl.firstname, 
            sum(gp.payout) - sum(gp.buyinamount) as profit,
            se.seasonnumber
            from spt_player pl, spt_play gp, spt_game gm, spt_season se
            where 
            pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(""" + selectedseason + """)
            group by se.seasonnumber, pl.firstname order by se.seasonnumber desc, profit desc
                        """))
        
        
    return render(request,'index.html',
            {'currentstanding_list' : currentstanding_list,
            'currentpoolamount_list' : currentpoolamount_list,
            'currentgame_list' : currentgame_list,
             'newsflash_list' : newsflash_list,
            'numberofcancelledgames_list' : numberofcancelledgames_list,
            'pll_list' : pll_list})

def pastsptwinners(request):
    psw_list = list(query_to_dicts("""
            select 
            pl.firstname as seasonwinner, 
            se.SeasonNumber as seasonnumber
            from spt_player pl, spt_play gp, spt_game gm, spt_season se
            where 
            pl.firstname = gp.players_id and 
            gp.games_id=gm.id and
            gm.seasons_id=se.seasonnumber and
            cast(gm.finalseasongame as int) = 1 and
            cast(gp.placement as int) = 1
            group by pl.firstname,se.seasonnumber order by se.seasonnumber desc                     
                        """))

    return render(request,'pastsptwinners.html',
                        {'psw_list' : psw_list})

def gamedetails(request):
        gd_list = list(query_to_dicts("""
            select 
            pl.firstname, 
            gp.buyinamount,
            gm.gamedate,
            gm.gamenumber, 
            gp.point,
            case when cast(gp.buyinamount as int) > 60 then (gp.buyinamount - 60) / 60 else 0 end as rebuys,
            CASE WHEN cast(gp.placement as int) = 0 THEN ' ' ELSE gp.placement END as placement,
            gp.payout,
            CASE WHEN cast(gp.sptmember as int) <> 0 THEN 'Yes' ELSE 'No' END As sptmember,
            CASE WHEN cast(gm.finalseasongame as int) <> 0 THEN 'Yes' ELSE 'No' END As finalseasongame,
            se.seasonnumber,
            se.seasonyear
            from spt_player pl, spt_play gp, spt_game gm, spt_season se
            where 
            pl.firstname = gp.players_id and 
            gp.games_id=gm.id and
            gm.seasons_id=se.seasonnumber
            order by se.seasonnumber desc, gm.gamedate desc, gm.gamenumber, cast(replace(gp.placement, '0', '9') as int) 
            """))
        return render(request,'gamedetails.html',
                        {'gd_list' : gd_list})

def profitloss(request):
        pl_list = list(query_to_dicts("""
            select 
            pl.firstname, 
            sum(gp.payout) - sum(gp.buyinamount) as profit,
            se.seasonnumber
            from spt_player pl, spt_play gp, spt_game gm, spt_season se
            where 
            pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber
            group by se.seasonnumber, pl.firstname order by se.seasonnumber desc, profit desc
                        """))
        return render(request,'profitloss.html',
                        {'pl_list' : pl_list})


def get_profit(request):
    
    data = list(query_to_dicts("""
            select * from (
                        select
                        pl.firstname,
                        count(*) as numberofgamesplayed,
                        sum(gp.payout) - sum(gp.buyinamount) as profit
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        cast(gp.sptmember as int) = 1
                        group by pl.firstname
                        order by profit desc) a
            where a.numberofgamesplayed > 9
                        """))

       
    return HttpResponse(json.dumps(data), content_type='application/json')           

def get_placement(request):
    
    data = list(query_to_dicts("""
            select * from (
                        select
                        pl.firstname,
                        count(*) as numberofgamesplayed,
                        sum(case when cast(gp.payout as float) > 0  OR cast(gp.placement as float) > 0 then 1 else 0 end) / cast(count(*) as float)  * 100 as percent
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        cast(gp.sptmember as int) = 1
                        group by pl.firstname
                        order by percent desc) a
            where a.numberofgamesplayed > 9
                        """))

        
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_placementwins(request):
    
    data = list(query_to_dicts("""
            select * from (
                        select
                        pl.firstname,
                        count(*) as numberofgamesplayed,
                        sum(case when cast(gp.placement as int) = 1 then 1 else 0 end) as firstplaces,
                        sum(case when cast(gp.placement as int) = 2 then 1 else 0 end) as secondplaces,
                        sum(case when cast(gp.placement as int) = 3 then 1 else 0 end) as thirdplaces,
                        sum(case when cast(gp.placement as int) = 4 then 1 else 0 end) as forthplaces,
                        sum(case when cast(gp.payout as float) > 0  OR cast(gp.placement as float) > 0 then 1 else 0 end) / cast(count(*) as float)  * 100 as percent,
                        sum(case when cast(gp.payout as float) > 0  OR cast(gp.placement as float) > 0 then 1 else 0 end) as top4
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        cast(gp.sptmember as int) = 1
                        group by pl.firstname
                        order by firstplaces desc,secondplaces desc,thirdplaces desc,forthplaces desc) a
             where a.numberofgamesplayed > 9
                        """))

       
    return HttpResponse(json.dumps(data), content_type='application/json')                      

def get_plfinaltablewins(request):

    stats_finaltablewins_list = list(query_to_dicts("""
                select
                        pl.firstname,
                        0 as plleader,
                        sum(case when cast(gm.finalseasongame as int) = 1 and cast(gp.placement as int) = 1 then 1 else 0 end) as finaltablewins
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber
                        group by pl.firstname
                order by finaltablewins desc
                        """))
    stats_seasonleader_sqllist = list(query_to_dicts("""
            select * from (
                select
                        pl.firstname,
                        count(*) as numberofgamesplayed,
                        sum(case when cast(gp.placement as int) = 1 then 1 else 0 end) as firstplaces,
                        sum(case when cast(gp.placement as int) = 2 then 1 else 0 end) as secondplaces,
                        sum(case when cast(gp.placement as int) = 3 then 1 else 0 end) as thirdplaces,
                        sum(case when cast(gp.placement as int) = 4 then 1 else 0 end) as forthplaces,
                        se.seasonnumber,
                        sum(gp.point) as points
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
                        group by pl.firstname,se.seasonnumber
                        order by se.seasonnumber, points desc,
                        firstplaces desc,secondplaces desc,thirdplaces desc,forthplaces desc) a
            where a.numberofgamesplayed > 9
            """))


    seasonnumber = 0
    seasonnumberprev = 0
    stats_seasonleader_list = {}
    for i in range(len(stats_seasonleader_sqllist)):
        seasonnumber = stats_seasonleader_sqllist[i]['seasonnumber']
        if seasonnumberprev != seasonnumber:
            stats_seasonleader_list[stats_seasonleader_sqllist[i]['firstname']] = stats_seasonleader_list.get(stats_seasonleader_sqllist[i]['firstname'],0) + 1
            seasonnumberprev = stats_seasonleader_sqllist[i]['seasonnumber']


    i = 0
    for i in range(len(stats_finaltablewins_list)):
        if stats_finaltablewins_list[i]['firstname'] in stats_seasonleader_list:
            stats_finaltablewins_list[i]['plleader'] = stats_seasonleader_list.get(stats_finaltablewins_list[i]['firstname'],0)

    
    return HttpResponse(json.dumps(stats_finaltablewins_list), content_type='application/json')       

def get_profitbyseason(request):

    data = list(query_to_dicts("""
                select * from (
                    select
                        se.seasonnumber,
                        pl.firstname,
                        count(*) as numberofgamesplayed,
                        sum(gp.payout) - sum(gp.buyinamount) as profit
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        cast(gp.sptmember as int) = 1
                        group by se.seasonnumber,pl.firstname
                        order by se.seasonnumber) a
                where a.numberofgamesplayed > 1
                """))
    
        
    return HttpResponse(json.dumps(data), content_type='application/json')                      
                           
