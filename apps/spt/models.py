from django.db import models

class NewsFlash(models.Model):
    newsflash = models.CharField(max_length=350)
    newsflashdatetime = models.DateTimeField(auto_now=True)

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return unicode(self.newsflashdatetime)

class Season(models.Model):
    seasonnumber = models.PositiveSmallIntegerField(primary_key=True)
    seasonyear = models.PositiveSmallIntegerField()

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return unicode('%d-%d' % (self.seasonnumber,self.seasonyear))

class Player(models.Model):
    firstname = models.CharField(primary_key=True,max_length=50,verbose_name='First Name')
    emailaddress = models.EmailField(max_length=75,verbose_name='E-mail')

    class Meta:
      	ordering = ['firstname']

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return unicode(self.firstname)

class Game(models.Model):
    NUMBEROFGAMES = (
        ('1', 'Game 1'),
        ('2', 'Game 2'),
    )
    seasons = models.ForeignKey(Season)
    members = models.ManyToManyField(Player, through='Play')
    gamenumber = models.CharField(max_length=1, choices=NUMBEROFGAMES,verbose_name='Game Number') 
    gamedate = models.DateField(verbose_name='Game Date')
    finalseasongame = models.BooleanField(default=False,verbose_name='Final Season Game')
    cancelledgame = models.BooleanField(default=False,verbose_name='Cancelled Game')
    class Meta:
	unique_together = (("gamenumber", "gamedate"),)    
    
    def __unicode__(self):
        return unicode('%s-%s' % (self.gamedate, self.gamenumber))

class Play(models.Model):
    PLACEMENT = (
        ('1', '1st Place'),
        ('2', '2nd Place'),
	('3', '3rd Place'),
        ('4', '4th Place'),
	('0', 'Did Not Place In Top 4'),
    )
    players = models.ForeignKey(Player)
    games = models.ForeignKey(Game)
    buyinamount = models.PositiveSmallIntegerField(default=60,verbose_name='Buy In Amount')
    placement = models.CharField(max_length=1, choices=PLACEMENT, default='0', verbose_name='Placement')
    point = models.PositiveSmallIntegerField(default=0)
    payout = models.PositiveSmallIntegerField(default=0,verbose_name='Payout')
    sptmember = models.BooleanField(default=True,verbose_name='SPT Member')
    
    def __unicode__(self):
        return unicode('%s-%s-%s' % (self.games.gamedate,self.games.gamenumber,self.players.firstname))
