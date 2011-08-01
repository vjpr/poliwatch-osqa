from django.core.management.base import NoArgsCommand
from forum.models import *
#TODO: move most models out of politician file
from forum.models.politician import *
from forum.actions import *
from forum.forms import *
from datetime import datetime

class Command(NoArgsCommand):
    def get_maker(self, value):
        existent = Politician.objects.filter(name=value)
        unexistent = [n for n in value if not n in existent]
        if (len(existent)<=0):
            raise forms.ValidationError(_("The following politician does not exist. Contact support to have %s added to the database") %
                        ', '.join(unexistent))
        return existent[0]
    
    def handle_noargs(self, **options):
        #objs = Comment.objects.all()

        #self.user = User.objects.get(id=1)

        # TODO get csv directly from google docs and then skip two rows
        # http://stackoverflow.com/questions/3287651/download-a-spreadsheet-from-google-docs-using-python

        # read csv
        import csv
        f = open("C:/workspace/poliwatch/politician_data.csv")
        w = csv.DictReader(f)

        election = Election.objects.filter(name='Australian Federal Election 2010')
        if (len(election)<=0):
            election = Election.objects.create(name='Australian Federal Election 2010')
        else:
            election = election[0]

        for row in w:
            
            # TODO: change way of referring to politician and check for duplicates
            politician = Politician.objects.filter(name=row['First Name'] + ' ' + row['Surname'])
            
            print row['First Name'] + ' ' + row['Surname']
            
            party = Party.objects.filter(abbreviated_name=row['Political Party'])
            if (len(party)==0):
                party = Party.objects.create(abbreviated_name=row['Political Party'],
                                             name=row['Political Party'],
                                             )
            else:
                party = party[0];
            
            electorate = Electorate.objects.filter(name=row['Electorate'])
            if (len(electorate)==0):
                electorate = Electorate.objects.create(name=row['Electorate'],region=row['State'])
            else:
                electorate = electorate[0]
            
            if (len(politician)==0):
                politician = Politician.objects.create(name=row['First Name'] + ' ' + row['Surname'],
                                          surname=row['Surname'],
                                          firstname=row['First Name'],
                                          party=party,
                                          constituency=electorate,
                                          )
            else:
                politician = politician[0];

            party_member = PartyMember(politician=politician, party=party, is_current=True, is_sitting=True)
            party_member.save()
            
            party_member_title = PartyMemberTitle(party_member=party_member,name=row['Parliamentary Titles'])
            party_member_title.save()
            
            contest = Contest.objects.filter(name=electorate)
            if (len(contest)<=0):
                contest = Contest.objects.create(name=electorate, election=election)
            else:
                contest = contest[0]
                
            contest_participant = ContestParticipant(politician=politician,contest=contest,party=party,contest_status=u'won')
            contest_participant.save()
            