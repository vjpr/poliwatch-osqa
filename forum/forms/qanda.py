import re
from datetime import date
from django import forms
from forum.models import *
from django.utils.translation import ugettext as _
from django.contrib.humanize.templatetags.humanize import apnumber

from django.utils.safestring import mark_safe
from general import NextUrlField, UserNameField, SetPasswordForm
from forum import settings
import logging
from django.forms.extras.widgets import SelectDateWidget
from forum.models.politician import Politician
from forum.models.maker import Maker

class HeadlineField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(HeadlineField, self).__init__(*args, **kwargs)
        self.required = True
        self.widget = forms.TextInput(attrs={'size' : 70, 'autocomplete' : 'off'})
        self.max_length = 255
        self.label  = _('Update Headline')
        self.help_text = _('Provide a headline for the update which will shown next to the promise on the list of promises ')
        self.initial = ''

    def clean(self, value):
        if len(value) < settings.FORM_MIN_QUESTION_TITLE:
            raise forms.ValidationError(_('headline must be must be at least %s characters') % settings.FORM_MIN_QUESTION_TITLE)

        return value

class StatusField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        super(StatusField, self).__init__(*args, **kwargs)
        self.required = True
        self.widget = forms.Select(None, Node.STATUS_CHOICES)
        self.max_length = 255
        self.label  = _('Status')
        self.help_text = _('Please select the current status of this promise')
        self.initial = ''

    def clean(self, value):
        return value

class TitleField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(TitleField, self).__init__(*args, **kwargs)
        self.required = True
        self.widget = forms.TextInput(attrs={'size' : 70, 'autocomplete' : 'off'})
        self.max_length = 255
        self.label  = _('Title')
        self.help_text = _('Please enter a descriptive title for the promise')
        self.initial = ''

    def clean(self, value):
        if len(value) < settings.FORM_MIN_QUESTION_TITLE:
            raise forms.ValidationError(_('title must be must be at least %s characters') % settings.FORM_MIN_QUESTION_TITLE)

        return value

#class MakerField(forms.CharField):
#    def __init__(self, *args, **kwargs):
#        super(MakerField, self).__init__(*args, **kwargs)
#        self.required = True
#        self.widget = forms.TextInput(attrs={'size' : 70, 'autocomplete' : 'off'})
#        self.max_length = 255
#        self.label  = _('Maker')
#        self.help_text = _('Who made the promise? Select from the list as you type or find the right politician in the politician lookup box.')
#        self.initial = ''
#
#    def clean(self, value):
#        if len(value) < settings.FORM_MIN_QUESTION_TITLE:
#            raise forms.ValidationError(_('Promise maker must be must be at least %s characters') % settings.FORM_MIN_QUESTION_TITLE)
#
#        existent = Politician.objects.filter(name=value)
#        unexistent = [n for n in value if not n in existent]
#        if (len(existent)<0):
#            raise forms.ValidationError(_("The following politician does not exist. Contact support to have %s added to the database") %
#                        ', '.join(unexistent))
#        return existent[0]

class EditorField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(EditorField, self).__init__(*args, **kwargs)
        self.widget = forms.Textarea(attrs={'id':'editor'})
        self.label  = _('content')
        self.help_text = u''
        self.initial = ''


class QuestionEditorField(EditorField):
    def __init__(self, *args, **kwargs):
        super(QuestionEditorField, self).__init__(*args, **kwargs)
        self.required = not bool(settings.FORM_EMPTY_QUESTION_BODY)


    def clean(self, value):
        if not bool(settings.FORM_EMPTY_QUESTION_BODY) and (len(re.sub('[ ]{2,}', ' ', value)) < settings.FORM_MIN_QUESTION_BODY):
            raise forms.ValidationError(_('Promise description must be at least %s characters') % settings.FORM_MIN_QUESTION_BODY)

        return value

class AnswerEditorField(EditorField):
    def __init__(self, *args, **kwargs):
        super(AnswerEditorField, self).__init__(*args, **kwargs)
        self.required = True

    def clean(self, value):
        if len(re.sub('[ ]{2,}', ' ', value)) < settings.FORM_MIN_QUESTION_BODY:
            raise forms.ValidationError(_('Update content must be at least %s characters') % settings.FORM_MIN_QUESTION_BODY)

        return value

#Sources
class SourcesEditorField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(SourcesEditorField, self).__init__(*args, **kwargs)
        self.widget = forms.Textarea(attrs={'id':'sources','rows':3})
        self.label  = _('Sources')
        self.help_text = u'Please enter the sources of your information using Harvard referencing style using the ADD SOURCE button'
        self.initial = ''
        

    def clean(self, value):
        if not bool(settings.FORM_EMPTY_QUESTION_BODY) and (len(re.sub('[ ]{2,}', ' ', value)) < settings.FORM_MIN_QUESTION_BODY):
            raise forms.ValidationError(_('Sources must be at least %s characters') % settings.FORM_MIN_QUESTION_BODY)

        return value

class MakerField(forms.CharField):
    def __init__(self, user=None, *args, **kwargs):
        super(MakerField, self).__init__(*args, **kwargs)
        self.required = True
        self.widget = forms.TextInput(attrs={'size' : 70, 'autocomplete' : 'off'})
        self.max_length = 255
        self.label  = _('Maker')
        #self.help_text = _('please use space to separate tags (this enables autocomplete feature)')
        self.help_text = _('Who made the promise? Select from the list as you type or find the right politician in the politician lookup box.')
        self.initial = ''

    def clean(self, value):
        value = super(MakerField, self).clean(value)
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
        
#        for maker in existent:
#            retval.append(maker)

        return existent

class TagNamesField(forms.CharField):
    def __init__(self, user=None, *args, **kwargs):
        super(TagNamesField, self).__init__(*args, **kwargs)
        self.required = True
        self.widget = forms.TextInput(attrs={'size' : 50, 'autocomplete' : 'off'})
        self.max_length = 255
        self.label  = _('Tags')
        #self.help_text = _('please use space to separate tags (this enables autocomplete feature)')
        self.help_text = _('Tags are short keywords, with no spaces within. At least %(min)s and up to %(max)s tags can be used.') % {
            'min': settings.FORM_MIN_NUMBER_OF_TAGS, 'max': settings.FORM_MAX_NUMBER_OF_TAGS    
        }
        self.initial = ''
        self.user = user

    def clean(self, value):
        value = super(TagNamesField, self).clean(value)
        data = value.strip().lower()

        split_re = re.compile(r'[ ,]+')
        list = {}
        for tag in split_re.split(data):
            list[tag] = tag

        if len(list) > settings.FORM_MAX_NUMBER_OF_TAGS or len(list) < settings.FORM_MIN_NUMBER_OF_TAGS:
            raise forms.ValidationError(_('please use between %(min)s and %(max)s tags') % { 'min': settings.FORM_MIN_NUMBER_OF_TAGS, 'max': settings.FORM_MAX_NUMBER_OF_TAGS})

        list_temp = []
        tagname_re = re.compile(r'^[\w+\.-]+$', re.UNICODE)
        for key,tag in list.items():
            if len(tag) > settings.FORM_MAX_LENGTH_OF_TAG or len(tag) < settings.FORM_MIN_LENGTH_OF_TAG:
                raise forms.ValidationError(_('please use between %(min)s and %(max)s characters in you tags') % { 'min': settings.FORM_MIN_LENGTH_OF_TAG, 'max': settings.FORM_MAX_LENGTH_OF_TAG})
            if not tagname_re.match(tag):
                raise forms.ValidationError(_('please use following characters in tags: letters , numbers, and characters \'.-_\''))
            # only keep one same tag
            if tag not in list_temp and len(tag.strip()) > 0:
                list_temp.append(tag)

        if settings.LIMIT_TAG_CREATION and not self.user.can_create_tags():
            existent = Tag.objects.filter(name__in=list_temp).values_list('name', flat=True)

            if len(existent) < len(list_temp):
                unexistent = [n for n in list_temp if not n in existent]
                raise forms.ValidationError(_("You don't have enough reputation to create new tags. The following tags do not exist yet: %s") %
                        ', '.join(unexistent))


        return u' '.join(list_temp)

class WikiField(forms.BooleanField):
    def __init__(self, disabled=False, *args, **kwargs):
        super(WikiField, self).__init__(*args, **kwargs)
        self.required = False
        self.label  = _('community wiki')
        self.help_text = _('if you choose community wiki option, the question and answer do not generate points and name of author will not be shown')
        if disabled:
            self.widget=forms.CheckboxInput(attrs={'disabled': "disabled"})
    def clean(self,value):
        return value

class EmailNotifyField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        super(EmailNotifyField, self).__init__(*args, **kwargs)
        self.required = False
        self.widget.attrs['class'] = 'nomargin'

class SummaryField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(SummaryField, self).__init__(*args, **kwargs)
        self.required = False
        self.widget = forms.TextInput(attrs={'size' : 50, 'autocomplete' : 'off'})
        self.max_length = 300
        self.label  = _('update summary:')
        self.help_text = _('enter a brief summary of your revision (e.g. fixed spelling, grammar, improved style, this field is optional)')


class FeedbackForm(forms.Form):
    message = forms.CharField(label=_('Your message:'), max_length=800,widget=forms.Textarea(attrs={'cols':60}))
    next = NextUrlField()

    def __init__(self, user, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        if not user.is_authenticated():
            self.fields['name'] = forms.CharField(label=_('Your name:'), required=False)
            self.fields['email'] = forms.EmailField(label=_('Email (not shared with anyone):'), required=True)

class DatePromisedField(forms.DateField):
    def __init__(self, *args, **kwargs):
        super(DatePromisedField, self).__init__(*args, **kwargs)
        self.required = True
        self.input_formats = ['%d/%m/%Y','%d-%m-%Y',]
        self.widget = forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'vDateField',            
            'size':'15'
        })
        self.label  = _('Date Promised')
        self.help_text = _('When was the promise made')
        #self.initial = datetime.date.today        

# TODO(vaughan): reduce duplication
class DateUpdatedField(forms.DateField):
    def __init__(self, *args, **kwargs):
        super(DateUpdatedField, self).__init__(*args, **kwargs)
        self.required = True
        self.input_formats = ['%d/%m/%Y','%d-%m-%Y',]
        self.widget = forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'vDateField',            
            'size':'15'
        })
        self.label  = _('Date Updated')
        self.help_text = _('When was the promise update made')
        #self.initial = datetime.date.today

class AskForm(forms.Form):
    title  = TitleField()
    text   = QuestionEditorField()
        
    # Added
    sources = SourcesEditorField()
    date_promised = DatePromisedField()
    maker = MakerField()

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(AskForm, self).__init__(data, *args, **kwargs)

        self.fields['tags']   = TagNamesField(user)

        if settings.WIKI_ON:
            self.fields['wiki'] = WikiField()

class AnswerForm(forms.Form):
    
    text   = AnswerEditorField()
    wiki   = WikiField()
    
    # Added
    sources = SourcesEditorField()
    title  = HeadlineField()
    status = StatusField()
    date_promised = DateUpdatedField()

    def __init__(self, question, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        if settings.WIKI_ON:
            self.fields['wiki'] = WikiField()

            #if question.nis.wiki:
            #    self.fields['wiki'].initial = True


class RetagQuestionForm(forms.Form):
    tags   = TagNamesField()
    # initialize the default values
    def __init__(self, question, *args, **kwargs):
        super(RetagQuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].initial = question.tagnames

class RevisionForm(forms.Form):
    """
    Lists revisions of a Question or Answer
    """
    revision = forms.ChoiceField(widget=forms.Select(attrs={'style' : 'width:520px'}))

    def __init__(self, post, *args, **kwargs):
        super(RevisionForm, self).__init__(*args, **kwargs)

        revisions = post.revisions.all().values_list('revision', 'author__username', 'revised_at', 'summary').order_by('-revised_at')

        date_format = '%c'
        self.fields['revision'].choices = [
            (r[0], u'%s - %s (%s) %s' % (r[0], r[1], r[2].strftime(date_format), r[3]))
            for r in revisions]

        self.fields['revision'].initial = post.active_revision.revision

class EditQuestionForm(forms.Form):
    title  = TitleField()
    text   = QuestionEditorField()
    sources = SourcesEditorField()
    summary = SummaryField()
    # Added
    date_promised = DatePromisedField()
    maker = MakerField()

    def __init__(self, question, user, revision=None, *args, **kwargs):
        super(EditQuestionForm, self).__init__(*args, **kwargs)

        if revision is None:
            revision = question.active_revision

        self.fields['title'].initial = revision.title
        self.fields['text'].initial = revision.body
        self.fields['sources'].initial = revision.sources
        self.fields['date_promised'].initial = revision.date_promised
        
        #TODO(vaughan): Make this work more like maker.
        for value in question.maker.values_list('name',flat=True):
            self.fields['maker'].initial += value + ','
        
        self.fields['tags'] = TagNamesField(user)
        self.fields['tags'].initial = revision.tagnames

        if settings.WIKI_ON:
            self.fields['wiki'] = WikiField(disabled=(question.nis.wiki and not user.can_cancel_wiki(question)), initial=question.nis.wiki)

class EditAnswerForm(forms.Form):
    text = AnswerEditorField()
    sources = SourcesEditorField()
    summary = SummaryField()
    title  = HeadlineField()
    #Added
    status = StatusField()
    date_promised = DateUpdatedField()

    def __init__(self, answer, user, revision=None, *args, **kwargs):
        super(EditAnswerForm, self).__init__(*args, **kwargs)

        if revision is None:
            revision = answer.active_revision

        self.fields['text'].initial = revision.body
        self.fields['sources'].initial = revision.sources
        self.fields['title'].initial = revision.title
        self.fields['status'].initial = revision.status
        self.fields['date_promised'].initial = revision.date_promised

        if settings.WIKI_ON:
            self.fields['wiki'] = WikiField(disabled=(answer.nis.wiki and not user.can_cancel_wiki(answer)), initial=answer.nis.wiki)

class EditUserForm(forms.Form):
    email = forms.EmailField(label=u'Email', help_text=_('this email does not have to be linked to gravatar'), required=True, max_length=75, widget=forms.TextInput(attrs={'size' : 35}))
    realname = forms.CharField(label=_('Real name'), required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    website = forms.URLField(label=_('Website'), required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    city = forms.CharField(label=_('Location'), required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    birthday = forms.DateField(label=_('Date of birth'), help_text=_('will not be shown, used to calculate age, format: YYYY-MM-DD'), required=False, widget=forms.TextInput(attrs={'size' : 35}))
    about = forms.CharField(label=_('Profile'), required=False, widget=forms.Textarea(attrs={'cols' : 60}))

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        if settings.EDITABLE_SCREEN_NAME:
            self.fields['username'] = UserNameField(label=_('Screen name'))
            self.fields['username'].initial = user.username
            self.fields['username'].user_instance = user
        self.fields['email'].initial = user.email
        self.fields['realname'].initial = user.real_name
        self.fields['website'].initial = user.website
        self.fields['city'].initial = user.location

        if user.date_of_birth is not None:
            self.fields['birthday'].initial = user.date_of_birth
        else:
            self.fields['birthday'].initial = '1990-01-01'
        self.fields['about'].initial = user.about
        self.user = user

    def clean_email(self):
        if self.user.email != self.cleaned_data['email']:
            if settings.EMAIL_UNIQUE == True:
                if 'email' in self.cleaned_data:
                    from forum.models import User
                    try:
                        User.objects.get(email = self.cleaned_data['email'])
                    except User.DoesNotExist:
                        return self.cleaned_data['email']
                    except User.MultipleObjectsReturned:
                        logging.error("Found multiple users sharing the same email: %s" % self.cleaned_data['email'])
                        
                    raise forms.ValidationError(_('this email has already been registered, please use another one'))
        return self.cleaned_data['email']
        

NOTIFICATION_CHOICES = (
    ('i', _('Instantly')),
    #('d', _('Daily')),
    #('w', _('Weekly')),
    ('n', _('No notifications')),
)

class SubscriptionSettingsForm(forms.ModelForm):
    enable_notifications = forms.BooleanField(widget=forms.HiddenInput, required=False)
    member_joins = forms.ChoiceField(widget=forms.RadioSelect, choices=NOTIFICATION_CHOICES)
    new_question = forms.ChoiceField(widget=forms.RadioSelect, choices=NOTIFICATION_CHOICES)
    new_question_watched_tags = forms.ChoiceField(widget=forms.RadioSelect, choices=NOTIFICATION_CHOICES)
    subscribed_questions = forms.ChoiceField(widget=forms.RadioSelect, choices=NOTIFICATION_CHOICES)

    class Meta:
        model = SubscriptionSettings

class UserPreferencesForm(forms.Form):
    sticky_sorts = forms.BooleanField(required=False, initial=False)
