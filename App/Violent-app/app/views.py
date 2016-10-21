import logging
import json

from flask import render_template
from flask_wtf import Form
from wtforms import fields
from wtforms.validators import Required

from . import app, estimator, target_names


logger = logging.getLogger('app')

class PredictForm(Form):
    """Fields for Predict"""
    month_list = [(1, "January"), (2, "February"), (3, "March"), (4, "April"), (5, "May"), (6, "June"), (7, "July"), 
    (8, "August"), (9, "September"), (10, "October"), (11, "November"), (12, "December")]
    month = fields.SelectField("Months", choices=month_list)
    day_list=[(1,"Monday"), (2, "Tuesday"), (3, "Wednesday"), (4, "Thursday"), (5, "Friday"), (6, "Saturday"), 
    (7, "Sunday")]
    day = fields.SelectField("Days", choices=day_list)
    time_list = [(1,'Day'), (2,'Evening'), (3,'LateNight')]
    time=fields.SelectField("Times", choices=time_list)
    loc_list = [(1,'D2'), (2,'R3'), (3,'J2'), (4,'B2'), (5,'C1'), (6,'N1'), (7,'K1'), (8,'Q3'), (9,'M3'), (10,'U3'), 
    (11, 'M2'), (12, 'N3'), (13, 'E1'), (14,'J3'), (15,'B3'), (16,'D1'), (17,'Q1'), (18,'C2'), (19,'F1'), (20,'L2'),
    (21, 'E3'), (22,'G3'), (23,'D3'), (24, 'W1'), (25,'O2'), (26,'Q2'), (27,'S2'), (28,'F2'), (29,'K3'), (30,'W3'),
    (31,'N2'), (32,'F3'), (33,'U2'), (34,'B1'), (35,'R1'), (36,'J1'), (37,'O1'), (38,'L1'), (39,'K2'), (40,'M1'), 
    (41,'S1'), (42,'O3'), (43,'E2'), (44,'S3'), (45,'G1'), (46,'C3'), (47,'W2'), (48,'G2'), (49,'L3'), (50,'U1'), 
    (51,'R2'), (52,'W'), (53,'DS'), (54,'99'), (55,'E'), (56,'BS'), (57,'S'), (58,'WP'), (59,'US'), (60,'MS'), 
    (61,'FS'), (62,'KS'), (63,'WS'), (64,'OS'), (65,'N'), (66,'CTY'),(67,'KCIO07'), (68,'SS'), (69,'CS'), (70,'DET'),
    (71,'TRF'), (86,'JS'), (72,'EP'), (73,'LS'), (74,'H3'), (75,'RS'),(76,'NP'), (77,'INV'), (78,'EDD'),
    (79,'COMM'), (80,'ES'), (81,'GS'), (82,'CCD'), (83,'SCTR1'), (84,'NS'), (85,'QS')]
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
    predicted_iris = None

    if form.validate_on_submit():
        # store the submitted values
        submitted_data = form.data

        # Retrieve values from form
        month = float(submitted_data['month'])
        day = float(submitted_data['day'])
        time = float(submitted_data['time'])
        loc = float(submitted_data['loc'])

        # Create array from values
        call_instance = [month, day, time, loc]

        my_prediction = estimator.predict(call_instance)
        # Return only the Predicted iris species
        predicted_crime = target_names[my_prediction]

    return render_template('index.html',
        form=form,
        prediction=predicted_iris)
