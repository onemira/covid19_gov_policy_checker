import pickle
from flask import Blueprint, render_template, g, request
import sqlite3
import pandas as pd
from .ml_model import model, X_test, df

# created a pickled model
# with open('model.pkl', 'wb') as files:
#    pickle.dump(model, files)

# load saved model
# with open('model.pkl', 'rb') as f:
#    model = pickle.load(f)

# y_pred = model.predict(X_test)
# print(y_pred)

bp = Blueprint('view', __name__)
url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(url)
    return db

# @bp.teardown_appcontext
# def close_connection(exception):
#    db = getattr(g, '_database', None)
#    if db is not None:
#        db.close()

# @bp.route('/<country_code>', defaults={'country_code': 'KOR'})


# myData = df.values
# countries = list(set(df['CountryName']))
countries = ['New Zealand', 'Norway', 'Zimbabwe', 'Suriname', 'Iceland', 'South Korea', 'United Arab Emirates', 'Australia',
             'Italy', 'Kuwait', 'Faeroe Islands', 'Bahamas', 'Denmark', 'Libya', 'Turkmenistan', 'Luxembourg', 'Afghanistan',
             'Namibia', 'Spain', 'Senegal', 'Cambodia', 'United States', 'El Salvador', 'Egypt', 'Malawi', 'Mauritania', 'Panama', 'Slovenia', 'Andorra', 'Palestine', 'Angola', 'Democratic Republic of Congo', 'Kosovo', 'Bahrain', 'Papua New Guinea', 'France', 'Lithuania', 'Puerto Rico', 'Portugal', 'Algeria', 'Fiji', 'India', 'Guyana', 'Honduras', 'Madagascar', 'Albania', 'Paraguay', 'Slovak Republic', 'Vanuatu', 'Bangladesh', 'Botswana', 'Nigeria', 'Qatar', 'Iraq', 'Seychelles', 'Bosnia and Herzegovina', 'Peru', "Cote d'Ivoire", 'United Kingdom', 'Ethiopia', 'Czech Republic', 'Nepal', 'Belarus', 'Sweden', 'Guinea', 'South Africa', 'Bolivia', 'Brunei', 'Tanzania', 'Malaysia', 'Uruguay', 'Canada', 'Tonga', 'Chile', 'Finland', 'Jordan', 'Cuba', 'Mozambique', 'Dominican Republic', 'Venezuela', 'Ireland', 'Estonia', 'Greenland', 'Singapore', 'Ghana', 'Lebanon', 'Georgia', 'Togo', 'Turkey', 'Zambia', 'Liechtenstein', 'Dominica', 'Cameroon', 'Hong Kong', 'Russia', 'Oman', 'San Marino', 'Burkina Faso', 'Jamaica', 'Kazakhstan', 'Taiwan', 'Eritrea', 'Kenya', 'Barbados', 'Central African Republic', 'Ecuador', 'Timor-Leste', 'Solomon Islands', 'Cyprus', 'Thailand', 'Uganda', 'Sierra Leone', 'Benin', 'Mali', 'Sudan', 'Bermuda', 'Indonesia', 'Latvia', 'Bulgaria', 'Philippines', 'Israel', 'Malta', 'Kyrgyz Republic', 'Chad', 'Pakistan', 'Serbia', 'Syria', 'United States Virgin Islands', 'Congo', 'Belize', 'Laos', 'Colombia', 'Rwanda', 'Trinidad and Tobago', 'Somalia', 'Guam', 'Mauritius', 'Hungary', 'Mongolia', 'Morocco', 'Tajikistan', 'Iran', 'Eswatini', 'Myanmar', 'Aruba', 'Argentina', 'Kiribati', 'Mexico', 'Haiti', 'South Sudan', 'Monaco', 'Macao', 'Costa Rica', 'Liberia', 'Poland', 'Azerbaijan', 'Saudi Arabia', 'Djibouti', 'Vietnam', 'Switzerland', 'Burundi', 'Netherlands', 'Gambia', 'Nicaragua', 'Moldova', 'Sri Lanka', 'Austria', 'Croatia', 'China', 'Lesotho', 'Romania', 'Tunisia', 'Greece', 'Belgium', 'Guatemala', 'Germany', 'Ukraine', 'Uzbekistan', 'Cape Verde', 'Brazil', 'Bhutan', 'Yemen', 'Niger', 'Japan', 'Gabon']
countries = sorted(countries)

df = df[~df.isnull().any(axis=1)]
df = df.sort_values('Date').drop_duplicates(['CountryName'], keep='last')


@bp.route('/')
def index():
    return render_template("index.html", countries=countries)


# index()
def get_c3(C3):
    if C3 == 0:
        return "no measures"
    elif C3 == 1:
        return 'recommend cancelling'
    elif C3 == 2:
        return 'require cancelling'
    else:
        return 'no data'


def get_c4(C4):
    if C4 == 0:
        return "no restrictions"
    elif C4 == 1:
        return 'restrictions on very large gatherings (the limit is above 1000 people)'
    elif C4 == 2:
        return 'restrictions on gatherings between 101-1000 people'
    elif C4 == 3:
        return 'restrictions on gatherings between 11-100 people'
    elif C4 == 4:
        return 'restrictions on gatherings of 10 people or less'
    else:
        return 'no data'


def get_c5(C5):
    if C5 == 0:
        return "no measures"
    elif C5 == 1:
        return 'recommend closing (or significantly reduce volume/route/means of transport available)'
    elif C5 == 2:
        return 'require closing (or prohibit most citizens from using it)'
    else:
        return 'no data'


def get_c7(C7):
    if C7 == 0:
        return "no measures"
    elif C7 == 1:
        return 'recommend not to travel between regions/cities'
    elif C7 == 2:
        return 'internal movement restrictions in place'
    else:
        return 'no data'


def get_c8(C8):
    if C8 == 0:
        return "no restrictions"
    elif C8 == 1:
        return 'screening arrivals'
    elif C8 == 2:
        return 'quarantine arrivals from some or all regions'
    elif C8 == 3:
        return 'ban arrivals from some regions'
    elif C8 == 4:
        return 'ban on all regions or total border closure'
    else:
        return 'no data'


def get_h1(H1):
    if H1 == 0:
        return "No Covid-19 public information campaign"
    elif H1 == 1:
        return 'public officials urging caution about Covid-19'
    elif H1 == 2:
        return 'coordinated public information campaign (eg across traditional and social media)'
    else:
        'no data'


def get_index(index):
    if index <= 30:
        return 'travel status: sure, why not?'
    else:
        return 'travel status: not recommended'


@bp.route('/query', methods=['POST'])
def country_select_query():
    selected_country = request.form['country']
    row = df[df["CountryName"] == selected_country]
    print(row)
    c3 = get_c3(row['C3_Cancel public events'].item())
    c4 = get_c4(row['C4_Restrictions on gatherings'].item())
    c5 = get_c5(row['C5_Close public transport'].item())
    # c7 = get_c7(row['C7_Restrictions on internal movements'].item())
    c8 = get_c8(row['C8_International travel controls'].item())
    h1 = get_h1(row['H1_Public information campaigns'].item())
    travel_status = get_index(row['StringencyIndexForDisplay'].item())
    date = row['Date'].item()

    return render_template("country_info.html", country=selected_country, c3=c3, c4=c4, c5=c5, c8=c8, h1=h1, travel_status=travel_status, date=date)
