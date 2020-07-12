from flask import Blueprint, render_template, request
from bikeshare.statistics import CITY_DATA, MONTH_NAMES_ABBR, DAY_NAMES_ABBR, webapp_main

bp = Blueprint(name=__name__, import_name=__name__, template_folder='templates')


@bp.route('/', methods=['POST', 'GET'])
def main():
    return render_template('index.html', methods=['POST', 'GET'])


@bp.route('/input', methods=['POST', 'GET'])
def get_input():

    city_input = ''
    month_input = ''
    day_input = ''
    error_message = ''
    output = ''
    output_filename = ''

    city_list = list(CITY_DATA.keys())
    month_list = MONTH_NAMES_ABBR
    day_list = DAY_NAMES_ABBR

    if request.method == 'POST':

        # Even though not possible to make user input mistakes with current web design front-end, validate input fields
        # anyhow to catch misalignment between front-end and back-end features offered.
        if request.form.get('city_input'):
            try:
                city_input = request.form['city_input'].title()
                month_input = request.form['month_input'].title()
                day_input = request.form['day_input'].title()

                if city_input and city_input not in city_list:
                    raise ValueError('Please try again, only enter a city from the list below')
                if month_input and month_input not in month_list:
                    raise ValueError('Please try again, only enter a month from the list below')
                if day_input and day_input not in day_list:
                    raise ValueError('Please try again, only enter a day from the list below')

                # No errors were found, if button was pressed, run statistics, read output file and print it's content
                if request.form.get("results") == "results_button":
                    try:
                        output_filename = webapp_main(city_input, month_input, day_input)
                    except Exception:
                        error_message = "Error occurred: Not possible to run statistics"
                    if output_filename:
                        with open(output_filename, 'r') as f:
                            output += f.read()
                    return render_template('results.html', output=output, error_message=error_message)

            except ValueError as e:
                error_message = e

    return render_template('get_input.html',
                           city_input=city_input,
                           month_input=month_input,
                           day_input=day_input,
                           error_message=error_message)

