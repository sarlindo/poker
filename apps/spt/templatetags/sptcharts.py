from django import template


register = template.Library()
@register.simple_tag
def placements(dicStats):
	names = ""
	firstplaces = ""
	secondplaces = ""
	thirdplaces = ""
	forthplaces = ""
	for i in range(len(dicStats)):
		if dicStats[i]['numberofgamesplayed'] > 10:
        		names = names + dicStats[i]['firstname'] + "|"
			firstplaces = firstplaces + str(float(dicStats[i]['firstplaces']) / 40 * 100) + ","
			secondplaces = secondplaces + str(float(dicStats[i]['secondplaces']) / 40 * 100) + ","
			thirdplaces = thirdplaces + str(float(dicStats[i]['thirdplaces']) / 40 * 100) + ","
			forthplaces = forthplaces + str(float(dicStats[i]['forthplaces']) / 40 * 100) + ","

	names = "|" + names
	firstplaces = firstplaces[:-1]
	secondplaces = secondplaces[:-1]
	thirdplaces = thirdplaces[:-1]
	forthplaces = forthplaces[:-1]

	finishes = firstplaces + "|" + secondplaces + "|" + thirdplaces + "|" + forthplaces
 	
	barchart = """
	http://chart.apis.google.com/chart
	?chtt=1st+2nd+3rd+4th+Placement
	&chts=cc0000,16
	&chs=750x200
	&chf=c,lg,45,FFFFFF,0,F5F5F5,0.750
	&chxt=x,y
	&chxl=0:""" + names + """1:|0|10|20|30|40
	&cht=bvg
	&chd=t:""" + finishes + """
	&chco=636363,99ffff,ccff00,33ff00
	&chbh=10
	"""

    	return barchart

@register.simple_tag
def profitloss(dicStats):
        names = ""
        profit = ""
        for i in range(len(dicStats)):
		if dicStats[i]['numberofgamesplayed'] > 10:
                	profit = profit + str(dicStats[i]['profit']) + ","
			names = names + dicStats[i]['firstname'] + "(" + str(dicStats[i]['profit']) + ")|"

        names = "|" + names
        profit = profit[:-1]

        barchart = """
        http://chart.apis.google.com/chart
        ?chtt=Cumalative+Profit
        &chts=cc0000,16
        &chs=750x200
        &chf=c,lg,45,FFFFFF,0,F5F5F5,0.750
        &chxt=x,y
        &chxl=0:""" + names + """1:|-3000|-2500|-2000|-1500|-1000|-500|0|500|1000|1500|2000|2500|3000
	&chd=t:""" + profit + """
        &cht=bvg
	&chbh=51
	&chco=636363
	&chds=-3000,3000
        """
        return barchart

@register.simple_tag
def top4(dicStats):
        names = ""
	totpercent = ""
	for i in range(len(dicStats)):
		if dicStats[i]['numberofgamesplayed'] > 10:
                	totpercent = totpercent + str(int(dicStats[i]['percent'])) + "," 
			names = names + dicStats[i]['firstname'] + "(" + str(int(dicStats[i]['percent'])) + ")|"
	names = "|" + names
 
        totpercent = totpercent[:-1]

 	barchart = """
        http://chart.apis.google.com/chart
        ?chtt=Top+4+Placement+Percentage
        &chts=cc0000,16
        &chs=750x200
        &chf=c,lg,45,FFFFFF,0,F5F5F5,0.750
        &chxt=x,y
        &chxl=0:""" + names + """1:|0|10|20|30|40|50|60|70|80|90|100
        &cht=bvg
        &chd=t:""" + totpercent + """
        &chco=636363
        &chbh=51
        """
        
	return barchart

@register.simple_tag
def sptchamps(dicStats):
        names = ""
        totpercent = ""
        for i in range(len(dicStats)):
		if dicStats[i]['numberofgamesplayed'] > 0 and dicStats[i]['finaltablewins'] > 0:
                	totpercent = totpercent + str(dicStats[i]['finaltablewins']) + ","
                	names = names + dicStats[i]['firstname'] + "(" + str(dicStats[i]['finaltablewins']) + ")|"

        names = "|" + names

        totpercent = totpercent[:-1]

        barchart = """
        http://chart.apis.google.com/chart
        ?chtt=SPT+Championships
        &chts=cc0000,16
        &chs=750x200
        &chf=c,lg,45,FFFFFF,0,F5F5F5,0.750
        &chxt=x,y
        &chxl=0:""" + names + """1:|0|1|2|3|4|5|6|7|8|9|10
        &cht=bvg
        &chd=t:""" + totpercent + """
        &chco=636363
        &chbh=50
	&chds=0,9
        """
 	return barchart

@register.simple_tag
def sptseasonpointleaders(dicStats):

  	names = ""
        totpercent = ""

	for key, value in dicStats.iteritems() :
        	totpercent = totpercent + str(value) + ","
                names = names + key + "(" + str(value) + ")|"

        names = "|" + names

        totpercent = totpercent[:-1]

   	barchart = """
        http://chart.apis.google.com/chart
        ?chtt=SPT+Season+Point+Leader
        &chts=cc0000,16
        &chs=750x200
        &chf=c,lg,45,FFFFFF,0,F5F5F5,0.750
        &chxt=x,y
        &chxl=0:""" + names + """1:|0|1|2|3|4|5|6|7|8|9|10
        &cht=bvg
        &chd=t:""" + totpercent + """
        &chco=636363
        &chbh=50
        &chds=0,9
        """
        return barchart

