from django.core.management.base import NoArgsCommand
from forum.models import *
from forum.actions import *
from forum.forms import *
from datetime import datetime

class Command(NoArgsCommand):
    def get_maker(self, value):
        existent = Politician.objects.filter(name=value)
        unexistent = [n for n in value if not n in existent]
        if (len(existent)<=0):
            politician = Politician.objects.create(name=value)
            return politician
            #raise forms.ValidationError(_("The following politician does not exist. Contact support to have %s added to the database") %
            #            ', '.join(unexistent))
            
        return existent[0]
    
    def get_maker_m2m(self,value):
        
        data = value.strip().lower()

        split_re = re.compile(r'[,]+')
        list = {}
        for maker in split_re.split(data):
            list[maker] = maker

        if len(list) < 1:
            raise forms.ValidationError(_('Must include at least one promise maker'))

        list_temp = []
        #retval = []
        for key,maker in list.items():
            # only keep one same tag
            if maker not in list_temp and len(maker.strip()) > 0:
                list_temp.append(maker)

        existent = Politician.objects.filter(name__in=list_temp)
        if len(existent) < len(list_temp):
            unexistent = [n for n in list_temp if not n in existent]
            raise forms.ValidationError(_("The following politicians do not exist yet: %s") %
                    ', '.join(unexistent))
        
        return existent
    
    def handle_noargs(self, **options):
        #objs = Comment.objects.all()

        self.user = User.objects.get(id=1)

        # TODO get csv directly from google docs and then skip two rows
        # http://stackoverflow.com/questions/3287651/download-a-spreadsheet-from-google-docs-using-python

        # read csv
        import csv
        reader = csv.reader(open("C:/workspace/poliwatch/promise_data.csv"), dialect='excel')
        
        reader.next() # skip first row

        # could use DictReader to remove index values which may change
        for row in reader:
            promise_data = dict(
                title = row[0],
                #maker = Command.get_maker(self,value=row[1]) if row[1] != '' else 'Unknown',
                maker = Command.get_maker_m2m(self,row[1]),
                text = row[2],
                sources = row[3],
                tags = row[4],
                date_promised = datetime.strptime(row[5], "%d/%m/%Y").date().isoformat() if row[5] != '' else datetime.now().date().isoformat(),
            )

            print promise_data['title'] + " (" + promise_data['date_promised'] + ")"

            # save the promise
            promise = AskAction(user=self.user).save(data=promise_data)
            
            update_data = dict(
                question = Question.objects.get(id=promise.node.id),
                title = row[6],
                status = row[7],
                text = row[8],
                sources = row[9],
                )
            
            AnswerAction(user=self.user).save(data=update_data)

        # get user from database
        print user