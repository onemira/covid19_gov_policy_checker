import pickle
import sqlite3
import pandas as pd
import re
from flask import Blueprint, render_template, g
from .ml_model import model, X_test, df

bp = Blueprint('view', __name__)
url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(url)
    return db


countries = ['New Zealand', 'Norway', 'Zimbabwe', 'Suriname', 'Iceland', 'South Korea', 'United Arab Emirates', 'Australia',
             'Italy', 'Kuwait', 'Faeroe Islands', 'Bahamas', 'Denmark', 'Libya', 'Turkmenistan', 'Luxembourg', 'Afghanistan',
             'Namibia', 'Spain', 'Senegal', 'Cambodia', 'United States', 'El Salvador', 'Egypt', 'Malawi', 'Mauritania', 'Panama',
             'Slovenia', 'Andorra', 'Palestine', 'Angola', 'Democratic Republic of Congo', 'Kosovo', 'Bahrain', 'Papua New Guinea',
             'France', 'Lithuania', 'Puerto Rico', 'Portugal', 'Algeria', 'Fiji', 'India', 'Guyana', 'Honduras', 'Madagascar', 'Albania',
             'Paraguay', 'Slovak Republic', 'Vanuatu', 'Bangladesh', 'Botswana', 'Nigeria', 'Qatar', 'Iraq', 'Seychelles', 'Bosnia and Herzegovina',
             'Peru', "Cote d'Ivoire", 'United Kingdom', 'Ethiopia', 'Czech Republic', 'Nepal', 'Belarus', 'Sweden', 'Guinea', 'South Africa',
             'Bolivia', 'Brunei', 'Tanzania', 'Malaysia', 'Uruguay', 'Canada', 'Tonga', 'Chile', 'Finland', 'Jordan', 'Cuba', 'Mozambique',
             'Dominican Republic', 'Venezuela', 'Ireland', 'Estonia', 'Greenland', 'Singapore', 'Ghana', 'Lebanon', 'Georgia', 'Togo', 'Turkey',
             'Zambia', 'Liechtenstein', 'Dominica', 'Cameroon', 'Hong Kong', 'Russia', 'Oman', 'San Marino', 'Burkina Faso', 'Jamaica', 'Kazakhstan',
             'Taiwan', 'Eritrea', 'Kenya', 'Barbados', 'Central African Republic', 'Ecuador', 'Timor-Leste', 'Solomon Islands', 'Cyprus', 'Thailand',
             'Uganda', 'Sierra Leone', 'Benin', 'Mali', 'Sudan', 'Bermuda', 'Indonesia', 'Latvia', 'Bulgaria', 'Philippines', 'Israel', 'Malta',
             'Kyrgyz Republic', 'Chad', 'Pakistan', 'Serbia', 'Syria', 'United States Virgin Islands', 'Congo', 'Belize', 'Laos', 'Colombia', 'Rwanda',
             'Trinidad and Tobago', 'Somalia', 'Guam', 'Mauritius', 'Hungary', 'Mongolia', 'Morocco', 'Tajikistan', 'Iran', 'Eswatini', 'Myanmar', 'Aruba',
             'Argentina', 'Kiribati', 'Mexico', 'Haiti', 'South Sudan', 'Monaco', 'Macao', 'Costa Rica', 'Liberia', 'Poland', 'Azerbaijan', 'Saudi Arabia',
             'Djibouti', 'Vietnam', 'Switzerland', 'Burundi', 'Netherlands', 'Gambia', 'Nicaragua', 'Moldova', 'Sri Lanka', 'Austria', 'Croatia', 'China',
             'Lesotho', 'Romania', 'Tunisia', 'Greece', 'Belgium', 'Guatemala', 'Germany', 'Ukraine', 'Uzbekistan', 'Cape Verde', 'Brazil', 'Bhutan', 'Yemen',
             'Niger', 'Japan', 'Gabon']
countries = sorted(countries)

df = df[~df.isnull().any(axis=1)]
df = df.sort_values('Date').drop_duplicates(['CountryName'], keep='last')
# df2: for initial note column
df2 = pd.read_csv(
    'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_responses.csv')
df2 = df2[df2['EndDate'].isna()]  # select latest policy only
df2 = df2[df2['PolicyType'].str.contains('H1|H2|H6|C1|C2|C3|C4|C5|C6|C7|C8')]


@bp.route('/')
def index():
    return render_template("index.html", countries=countries)


def get_c1(C1):
    if C1 == 0:
        return "no measures"
    elif C1 == 1:
        return 'recommend closing or all schools open with alterations resulting in significant differences compared to non-Covid-19 operations'
    elif C1 == 2:
        return 'require closing (only some levels or categories, eg just high school, or just public schools)'
    elif C1 == 3:
        return 'require closing all levels'
    else:
        return 'no data'


def get_c2(C2):
    if C2 == 0:
        return 'no measures'
    elif C2 == 1:
        return 'recommend closing (or recommend work from home) or all businesses open with alterations resulting in significant differences compared to non-Covid-19 operation'
    elif C2 == 2:
        return 'require closing (or work from home) for some sectors or categories of workers'
    elif C2 == 3:
        return 'require closing (or work from home) for all-but-essential workplaces (eg grocery stores, doctors)'
    else:
        return 'no data'


def get_c3(C3):
    if C3 == 0:
        return 'no measures'
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


def get_c6(C6):
    if C6 == 0:
        return "no measures"
    elif C6 == 1:
        return 'recommend not leaving house'
    elif C6 == 2:
        return "require not leaving house with exceptions for daily exercise, grocery shopping, and 'essential' trips"
    elif C6 == 3:
        return 'require not leaving house with minimal exceptions (eg allowed to leave once a week, or only one person can leave at a time, etc))'
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


def get_h2(H2):
    if H2 == 0:
        return "no testing policy"
    elif H2 == 1:
        return 'only those who both (a) have symptoms AND (b) meet specific criteria (eg key workers, admitted to hospital, came into contact with a known case, returned from overseas)'
    elif H2 == 2:
        return 'testing of anyone showing Covid-19 symptoms'
    elif H2 == 3:
        return 'open public testing (eg "drive through" testing available to asymptomatic people)'
    else:
        'no data'


def get_h6(H6):
    if H6 == 0:
        return "No policy"
    elif H6 == 1:
        return 'Recommended'
    elif H6 == 2:
        return 'Required in some specified shared/public spaces outside the home with other people present, or some situations when social distancing not possible'
    elif H6 == 3:
        return 'Required in all shared/public spaces outside the home with other people present or all situations when social distancing not possible'
    else:
        'Required outside the home at all times regardless of location or presence of other people'


def get_index(index):
    if index <= 25:
        return f'Travel Status: recommended (AI Recommendation System Index: {index}/100)'
    elif index <= 50:
        return f'Travel Status: Warning (AI Recommendation System Index: {index}/100)'
    else:
        return f'Travel Status: not recommended (AI Recommendation System Index: {index}/100)'


@bp.route('/query', methods=['POST'])
def country_select_query():
    from flask import request

    selected_country = request.form['country']
    row = df[df["CountryName"] == selected_country]
    row2 = df2[df2["CountryName"] == selected_country]

    c1 = get_c1(row['C1_School closing'].item())
    c2 = get_c2(row['C2_Workplace closing'].item())
    c3 = get_c3(row['C3_Cancel public events'].item())
    c4 = get_c4(row['C4_Restrictions on gatherings'].item())
    c5 = get_c5(row['C5_Close public transport'].item())
    c6 = get_c6(row['C6_Stay at home requirements'].item())
    c7 = get_c7(row['C7_Restrictions on internal movement'].item())
    c8 = get_c8(row['C8_International travel controls'].item())
    h1 = get_h1(row['H1_Public information campaigns'].item())
    h2 = get_h2(row['H2_Testing policy'].item())
    h6 = get_h6(row['H6_Facial Coverings'].item())

    def get_note(column):
        # check if data exists -if not, return 'no data'
        if row2[row2['PolicyType'].str.contains(column)]['InitialNote'].any():
            # add ', ' before 'http' as a string
            # to-do: use <a> tag for hyperlinks
            pat = re.compile(r"(http)")
            value = pat.sub(
                ", \\1", row2[row2['PolicyType'].str.contains(column)]['InitialNote'].item())
            return value
        else:
            return 'No data'

    # policy details
    c1_note = get_note('C1')
    c2_note = get_note('C2')
    c3_note = get_note('C3')
    c4_note = get_note('C4')
    c5_note = get_note('C5')
    c6_note = get_note('C6')
    c7_note = get_note('C7')
    c8_note = get_note('C8')
    h1_note = get_note('H1')
    h2_note = get_note('H2')
    h6_note = get_note('H6')

    travel_status = get_index(row['StringencyIndexForDisplay'].item())
    date = row['Date'].item()
    index = row['StringencyIndexForDisplay'].item()
    data_set = [
        (c1, c1_note, 'School closing', 'c1'),
        (c2, c2_note, 'Workplace closing', 'c2'),
        (c3, c3_note, 'Cancel public events', 'c3'),
        (c4, c4_note, 'Restrictions on gatherings', 'c4'),
        (c5, c5_note, 'Close public transport', 'c5'),
        (c6, c6_note, 'Stay at home requirements', 'c6'),
        (c7, c7_note, 'Restrictions on internal movement', 'c7'),
        (c8, c8_note, 'International travel controls', 'c8'),
        (h1, h1_note, 'Public information campaigns', 'h1'),
        (h2, h2_note, 'Testing policy', 'h2'),
        (h6, h6_note, 'Facial Coverings', 'h6')
    ]

    return render_template("country_info.html", data_set=data_set, index=index, country=selected_country, travel_status=travel_status, date=date)
