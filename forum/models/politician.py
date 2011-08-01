'''
All models related to politician promise maker

Created on 19/12/2010

@author: Vaughan
'''
from base import *
from maker import Maker
from datetime import date
from datetime import datetime
from forum.models import *
from forum.models.tag import *

STATE_CHOICES = (
                      ('nsw', 'New South Wales'),
                      ('qld', 'Queensland'),
                      ('vic', 'Victoria'),
                      ('act', 'Australian Captial Territory'),
                      ('tas', 'Tasmania'),
                      )

GENDER_CHOICES = (
                       ('m','Male'),
                       ('f','Female'),
                       )

# remove null=true, this is just for testing importing
class Party(BaseModel):
    name = models.CharField(max_length=128,)
    short_name = models.CharField(max_length=128,blank=True, null=True)
    abbreviated_name = models.CharField(max_length=10)
    level = models.CharField(max_length=128,blank=True, null=True)
    region = models.CharField(max_length=128,blank=True, null=True)

    def __unicode__(self):
        return self.name

class Electorate(BaseModel):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=10, choices=STATE_CHOICES)

class Politician(Maker):
    party = models.ForeignKey(Party) # current party
    surname = models.CharField(max_length=128)
    firstname = models.CharField(max_length=128)
    constituency = models.ForeignKey(Electorate)
    promises = models.ManyToManyField('forum.Node', through='PromiseMaker')
    #add gender choice field

    @property
    def current_party(self):
        return Politician.party
    def all_promises(self):
        return self.node_set
    '''TODO: Must check that it is a questions'''
    @property
    def promise_count(self):
        return self.node_set.filter().count()
    @property
    def get_name(self):
        return self.name
    def __unicode__(self):
        return self.name

class PromiseMaker(BaseModel):
    #promise = models.ForeignKey('forum.NodeContent')
    revision = models.ForeignKey('forum.NodeRevision',null=True)
    promise = models.ForeignKey('forum.Node')
    maker = models.ForeignKey(Politician)

# maps portfolios to tags - use RegEx
class Portfolio(BaseModel):
    name = models.CharField(max_length=400)
    tags = models.ManyToManyField(Tag)

class PartyMember(BaseModel):
    politician = models.ForeignKey(Politician)
    party = models.ForeignKey(Party)
    date_joined = models.DateField(blank=True, null=True)
    date_left = models.DateField(blank=True, null=True)
    is_current = models.BooleanField()
    is_sitting = models.BooleanField()

    def __unicode__(self):
        return self.party.name + " " + self.politician.name

# maps party-members to parlimentary titles
class PartyMemberTitle(BaseModel):
    party_member = models.ForeignKey(PartyMember)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    portfolios = models.ManyToManyField(Portfolio)
    name = models.CharField(max_length=400)
    position = models.CharField(max_length=200,blank=True, null=True) # Minister,Special Minister
    
    def __unicode__(self):
        return self.name
    

class Election(BaseModel):
    name = models.CharField(max_length=128) #australian federal election'
    announced_date= models.DateField(blank=True, null=True)
    election_date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class Contest(BaseModel):
    name = models.ForeignKey(Electorate) #warringah'
    participants = models.ManyToManyField(Politician, through='ContestParticipant')
    election = models.ForeignKey(Election)

    def __unicode__(self):
        return self.name

class ContestParticipant(BaseModel):
    CONTEST_STATUS = (
        (u'won', u'Won'),
        (u'lost', u'Lost'),
        (u'contesting', u'Contesting'),
    )
    politician = models.ForeignKey(Politician)
    contest = models.ForeignKey(Contest)
    party = models.ForeignKey(Party) # name of the party you are representing in this election
    contest_status = models.CharField(max_length=10, choices=CONTEST_STATUS)

    def __unicode__(self):
        return self.name

