from flask_wtf import FlaskForm
from wtforms import SubmitField


class ScrapingForm(FlaskForm):
    submit = SubmitField('Iniciar Scraping')
