from django.shortcuts import render
from apps.spt.models import Player
from apps.spt.models import Game
from apps.spt.models import Play
from apps.spt.models import Season
from django.views.generic import ListView
from apps.spt.dbutil import query_to_dicts

def index(request):

	currentstanding_list =  list(query_to_dicts("""
                        select
                        pl.firstname,
                        sum(gp.point) as points
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(select MAX(seasonnumber) from spt_season) and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
			group by pl.firstname
                        order by points desc
                        """))

 	previousseasonstanding_list =  list(query_to_dicts("""
                        select
                        pl.firstname,
                        sum(gp.point) as points
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(select MAX(seasonnumber) - 1 from spt_season) and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
			group by pl.firstname
                        order by points desc
                        """))

	currentpoolamount_list = list(query_to_dicts("""
                        select
			(count(*) * 10) as poolamount,
                        (count(*) * 10 - plpa.buyintotal) as poolamountadjusted,
                        ((count(*) * 10 - plpa.buyintotal) * .50) as firstplaceamount,
                        ((count(*) * 10 - plpa.buyintotal) * .30) as secondplaceamount,
                        ((count(*) * 10 - plpa.buyintotal) * .20) as thirdplaceamount,
			plpa.buyintotal,
			plpa.plleader
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se,
			(select
                        pl.firstname as plleader,
                        se.seasonnumber,
                        sum(gp.point) as points,
                        (count(*) * 10) as buyintotal
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
			pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(select MAX(seasonnumber) from spt_season) and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
			group by pl.firstname,se.seasonnumber
                        order by points desc limit 1) plpa               
			where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(select MAX(seasonnumber) from spt_season) and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
                        """))
	previousseasonpoolamount_list = list(query_to_dicts("""
                        select
                        (count(*) * 10) as poolamount,
                        (count(*) * 10 - plpa.buyintotal) as poolamountadjusted,
                        ((count(*) * 10 - plpa.buyintotal) * .50) as firstplaceamount,
                        ((count(*) * 10 - plpa.buyintotal) * .30) as secondplaceamount,
                        ((count(*) * 10 - plpa.buyintotal) * .20) as thirdplaceamount,
                        plpa.buyintotal,
			plpa.plleader
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se,
                        (select
                        pl.firstname as plleader,
                        se.seasonnumber,
                        sum(gp.point) as points,
                        (count(*) * 10) as buyintotal
                        from spt_player pl, spt_play gp, spt_game gm, spt_season se
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(select MAX(seasonnumber) - 1 from spt_season) and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
  			group by pl.firstname,se.seasonnumber
                        order by points desc limit 1) plpa
                        where
                        pl.firstname = gp.players_id and
                        gp.games_id=gm.id and
                        gm.seasons_id=se.seasonnumber and
                        gm.seasons_id=(select MAX(seasonnumber) - 1 from spt_season) and
                        cast(gm.finalseasongame as int) = 0 and
                        cast(gp.sptmember as int) = 1
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
                        """))
	newsflash_list = list(query_to_dicts("""
                        select newsflash
                        from spt_newsflash nf
                        where
                        nf.id=(select MAX(id) from spt_newsflash)
                        """))
	
	return render(request,'index.html',
			{'currentstanding_list' : currentstanding_list,
			'previousseasonstanding_list' : previousseasonstanding_list,
			'currentpoolamount_list' : currentpoolamount_list,
			'previousseasonpoolamount_list' : previousseasonpoolamount_list,
			'currentgame_list' : currentgame_list,
 			'newsflash_list' : newsflash_list})

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

