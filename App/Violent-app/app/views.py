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
    ('F1','F1'), ('L2','L2'), ('E3', 'E3'), ('G3','G3'), ('D3','D3'), ('W1', 'W1'), ('O2','O2'), ('Q2','Q2')] 
    #(27,'S2'), (28,'F2'), (29,'K3'), (30,'W3'),
    #(31,'N2'), (32,'F3'), (33,'U2'), (34,'B1'), (35,'R1'), (36,'J1'), (37,'O1'), (38,'L1'), (39,'K2'), (40,'M1'), 
    #(41,'S1'), (42,'O3'), (43,'E2'), (44,'S3'), (45,'G1'), (46,'C3'), (47,'W2'), (48,'G2'), (49,'L3'), (50,'U1'), 
    #(51,'R2'), (52,'W'), (53,'DS'), (54,'99'), (55,'E'), (56,'BS'), (57,'S'), (58,'WP'), (59,'US'), (60,'MS'), 
    #(61,'FS'), (62,'KS'), (63,'WS'), (64,'OS'), (65,'N'), (66,'CTY'),(67,'KCIO07'), (68,'SS'), (69,'CS'), (70,'DET'),
    #(71,'TRF'), (86,'JS'), (72,'EP'), (73,'LS'), (74,'H3'), (75,'RS'),(76,'NP'), (77,'INV'), (78,'EDD'),
    #(79,'COMM'), (80,'ES'), (81,'GS'), (82,'CCD'), (83,'SCTR1'), (84,'NS'), (85,'QS')]
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
