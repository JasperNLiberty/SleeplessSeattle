import logging
import json

from flask import render_template
from flask_wtf import Form
from wtforms import fields
from wtforms.validators import Required

import pandas as pd

from . import app, estimator, target_names
from violent_fe import feature_engineer



logger = logging.getLogger('app')

class PredictForm(Form):
    """Fields for Predict"""
    month_list = [(1, "January"), (2, "February"), (3, "March"), (4, "April"), (5, "May"), (6, "June"), (7, "July"), 
    (8, "August"), (9, "September"), (10, "October"), (11, "November"), (12, "December")]
    month = fields.SelectField("Months", choices=month_list, coerce = int)
    day_list=[(1,"Monday"), (2, "Tuesday"), (3, "Wednesday"), (4, "Thursday"), (5, "Friday"), (6, "Saturday"), 
    (7, "Sunday")]
    day = fields.SelectField("Days", choices=day_list, coerce = int)
    time_list = [(6,'Day'), (17,'Evening'), (2,'LateNight')]
    time=fields.SelectField("Times", choices=time_list, coerce = int)
    loc_list = [('D2','D2'), ('R3','R3'), ('J2','J2'), ('B2','B2'), ('C1','C1'), ('N1','N1'), ('K1','K1'), ('Q3','Q3'),
     ('M3','M3'), ('U3','U3'), ('M2', 'M2'), ('N3', 'N3'), ('E1', 'E1'), ('J3','J3'), ('B3','B3'), ('D1','D1'), ('Q1','Q1'), ('C2','C2'), 
    ('F1','F1'), ('L2','L2'), ('E3', 'E3'), ('G3','G3'), ('D3','D3'), ('W1', 'W1'), ('O2','O2'), ('Q2','Q2'), 
    ('S2','S2'), ('F2','F2'), ('K3','K3'), ('W3','W3'), ('N2','N2'), ('F3','F3'), ('U2','U2'), ('B1','B1'), ('R1','R1'),
    ('J1','J1'), ('O1','O1'), ('L1','L1'), ('K2','K2'), ('M1','M1'),('S1','S1'), ('O3','O3'), ('E2','E2'), ('S3','S3'),
    ('G1','G1'), ('C3','C3'), ('W2','W2'), ('G2','G2'), ('L3','L3'), ('U1','U1'), ('R2','R2'), ('W','W'), ('DS','DS'), 
    ('99','99'), ('E','E'), ('BS','BS'), ('S','S'), ('WP','WP'), ('US','US'), ('MS','MS'), ('FS','FS'), ('KS','KS'), 
    ('WS','WS'), ('OS','OS'), ('N','N'), ('CTY','CTY'),('KCIO07','KCIO07'), ('SS','SS'), ('CS','CS'), ('DET','DET'),
    ('TRF','TRF'), ('JS','JS'), ('EP','EP'), ('LS','LS'), ('H3','H3'), ('RS','RS'),('NP','NP'), ('INV','INV'), 
    ('EDD','EDD'),('COMM','COMM'), ('ES','ES'), ('GS','GS'), ('CCD','CCD'), ('SCTR1','SCTR1'), ('NS','NS'), ('QS','QS')]
    loc=fields.SelectField("Locations", choices=loc_list)

    # HR = fields.DecimalField('HR:', places=2, validators=[Required()])
    # sepal_width = fields.DecimalField('D:', places=2, validators=[Required()])
    # petal_length = fields.DecimalField('R:', places=2, validators=[Required()])
    # petal_width = fields.DecimalField('J:', places=2, validators=[Required()])

    submit = fields.SubmitField('Submit')


@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = PredictForm()
    predicted_crime = None

    if form.validate_on_submit():
        # store the submitted values
        submitted_data = form.data
        #import pdb;pdb.set_trace()

        # Retrieve values from form
        month = float(submitted_data['month'])
        day = float(submitted_data['day'])
        time = float(submitted_data['time'])
        loc = (submitted_data['loc'])

        # Create array from values
        d={'Scene_Month':[month], 'Scene_DayofWeek':[day], 'Hour':[time], 'Zone/Beat':[loc]}

        call_instance = pd.DataFrame(d)

        X_test=feature_engineer(call_instance)
        

        my_prediction = estimator.predict(X_test.values)
        # Return only the Predicted iris species
        predicted_crime = target_names[my_prediction]
    else:
        print form.errors

    return render_template('index.html',
        form=form,
        prediction=predicted_crime)
