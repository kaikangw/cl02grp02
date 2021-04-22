from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, TextAreaField, StringField
from wtforms.validators import DataRequired
from app.generalFunctions import getTenants


#form for the audit
class AuditForm(FlaskForm):
    professionalism1 = RadioField('professionalism1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    professionalism2 = RadioField('professionalism2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    professionalism3 = RadioField('professionalism3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')

    staffhygiene1 = RadioField('staffhygiene1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    staffhygiene2 = RadioField('staffhygiene2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    staffhygiene3 = RadioField('staffhygiene3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    staffhygiene4 = RadioField('staffhygiene4', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    staffhygiene5 = RadioField('staffhygiene5', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    staffhygiene6 = RadioField('staffhygiene6', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    staffhygiene7 = RadioField('staffhygiene7', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    staffhygiene8 = RadioField('staffhygiene8', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    staffhygiene9 = RadioField('staffhygiene9', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    staffhygiene10 = RadioField('staffhygiene10', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')

    generalenv1 = RadioField('generalenv1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv2 = RadioField('generalenv2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv3 = RadioField('generalenv3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv4 = RadioField('generalenv4', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv5 = RadioField('generalenv5', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv6 = RadioField('generalenv6', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv7 = RadioField('generalenv7', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv8 = RadioField('generalenv8', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv9 = RadioField('generalenv9', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv10 = RadioField('generalenv10', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv11 = RadioField('generalenv11', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv12 = RadioField('generalenv12', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv13 = RadioField('generalenv13', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv14 = RadioField('generalenv14', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalenv15 = RadioField('generalenv15', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')


    handhygiene1 = RadioField('handhygiene1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    handhygiene2 = RadioField('handhygiene2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')

    storageprep1 = RadioField('storageprep1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep2 = RadioField('storageprep2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep3 = RadioField('storageprep3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep4 = RadioField('storageprep4', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep5 = RadioField('storageprep5', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep6 = RadioField('storageprep6', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep7 = RadioField('storageprep7', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep8 = RadioField('storageprep8', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep9 = RadioField('storageprep9', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep10 = RadioField('storageprep10', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep11 = RadioField('storageprep11', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep12 = RadioField('storageprep12', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep13 = RadioField('storageprep13', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep14 = RadioField('storageprep14', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep15 = RadioField('storageprep15', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storageprep16 = RadioField('storageprep16', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep17 = RadioField('storageprep17', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep18 = RadioField('storageprep18', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep19 = RadioField('storageprep19', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep20 = RadioField('storageprep20', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep21 = RadioField('storageprep21', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep22 = RadioField('storageprep22', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep23 = RadioField('storageprep23', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep24 = RadioField('storageprep24', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep25 = RadioField('storageprep25', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')   
    storageprep26 = RadioField('storageprep26', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')    
    
    storagefood1 = RadioField('storagefood1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood2 = RadioField('storagefood2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood3 = RadioField('storagefood3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood4 = RadioField('storagefood4', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood5 = RadioField('storagefood5', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood6 = RadioField('storagefood6', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood7 = RadioField('storagefood7', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood8 = RadioField('storagefood8', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood9 = RadioField('storagefood9', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood10 = RadioField('storagefood10', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    storagefood11 = RadioField('storagefood11', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')

    food1 = RadioField('food1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    food2 = RadioField('food2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    food3 = RadioField('food3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    food4 = RadioField('food4', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    food5 = RadioField('food5', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    food6 = RadioField('food6', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    food7 = RadioField('food7', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')

    beverage1 = RadioField('beverage1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    beverage2 = RadioField('beverage2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    beverage3 = RadioField('beverage3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    beverage4 = RadioField('beverage4', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')

    generalsafety1 = RadioField('generalsafety1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety2 = RadioField('generalsafety2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety3 = RadioField('generalsafety3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety4 = RadioField('generalsafety4', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety5 = RadioField('generalsafety5', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety6 = RadioField('generalsafety6', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety7 = RadioField('generalsafety7', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety8 = RadioField('generalsafety8', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety9 = RadioField('generalsafety9', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety10 = RadioField('generalsafety10', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    generalsafety11 = RadioField('generalsafety11', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')

    fire1 = RadioField('fire1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    fire2 = RadioField('fire2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    fire3 = RadioField('fire3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')

    elect1 = RadioField('elect1', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    elect2 = RadioField('elect2', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    elect3 = RadioField('elect3', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')
    elect4 = RadioField('elect4', choices=[('1','1'),('0','0'),('N/A','N/A')], default = '1')

    submit = SubmitField('submit')  

    remarks = TextAreaField('remarks')

    rectification = SelectField('Rectification time:', 
                            choices=[(3, '3 Days'),
                                    (7,'7 Days')])

    
class ResultForm(FlaskForm):
    option = SelectField('option:',
                           choices=[('tenant', 'Worst performing tenants'),('individual', 'Worst performing individual scores'),('institution', 'Worst performing institutions ')])
    submit = SubmitField('submit')

class NewForm(FlaskForm):
    auditor = StringField('Auditor:', 
                        choices=[('auditorA', 'Auditor A')])
    submit = SubmitField('submit')

class ShopForm(FlaskForm):
    institution = SelectField('institution:', 
                            choices=[('CGH', 'CGH')])
    submit = SubmitField('submit')


class GraphForm(FlaskForm):
    auditee = SelectField('Auditee:', 
                            choices=[('kopitiam', 'Kopitiam')])
    submit = SubmitField('submit')
