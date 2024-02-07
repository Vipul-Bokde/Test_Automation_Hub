import calendar
import random
import datetime as dt
from datetime import datetime, timedelta
from libraries import forms, mouse
from sparc_pages.constants import *
import allure
from datetime import datetime, date



# common dates

def get_current_quarter():
    now = datetime.now()
    current_quarter = ((now.month - 1) // 3 + 1)
    return current_quarter


def get_random_quarter():
    quarter = get_current_quarter()
    quarter_op = quarter - 1
    if quarter_op == 0:
        quarter_op = 4
    q_options = [quarter, quarter_op]
    q_selected = str(random.choice(q_options))
    return q_selected


def get_current_util_quarter():
    now = datetime.now()
    current_year = now.year
    quarter = get_current_quarter()
    util_quarter = str(current_year) + 'q' + str(quarter)
    return util_quarter


def get_current_and_last_quarters():
    now = datetime.now()
    current_year = now.year
    quarter = get_current_quarter()
    last_quarter = quarter - 1
    if last_quarter == 0:
        last_quarter = 4
        current_year = current_year - 1
    current_util_quarter = str(current_year) + 'q' + str(quarter)
    last_util_quarter = str(current_year) + 'q' + str(last_quarter)
    return [last_util_quarter, current_util_quarter]


def validate_quarter_by_year(year):
    now = datetime.now()
    quarter = get_random_quarter()
    current_year = now.year
    if quarter == "1" and year == str(current_year - 1):
        quarter = 4
        return quarter


def get_start_and_end_dates_by_quarter(quarter):
    now = datetime.now()
    limit_date = [value for q_item, value in QUARTER_RANGE.items() if q_item == quarter][0]
    end_date = datetime.strptime(str(limit_date) + '/' + str(now.year), '%d/%m/%Y').date()
    if quarter == "1":
        start_date = datetime.strptime("01/01" + '/' + str(now.year), '%d/%m/%Y').date()
    elif quarter == "2":
        start_date = datetime.strptime("01/04" + '/' + str(now.year), '%d/%m/%Y').date()
    elif quarter == "3":
        start_date = datetime.strptime("01/07" + '/' + str(now.year), '%d/%m/%Y').date()
    else:
        start_date = datetime.strptime("01/10" + '/' + str(now.year), '%d/%m/%Y').date()
    return start_date, end_date


def get_random_date_by_start_and_end_dates(start_date, end_date):
    start_date = str(start_date.year) + ', ' + str(start_date.month) + ', ' + str(start_date.day)
    start_date = datetime.strptime(start_date, '%Y, %m, %d').date()
    end_date = str(end_date.year) + ', ' + str(end_date.month) + ', ' + str(end_date.day)
    end_date = datetime.strptime(end_date, '%Y, %m, %d').date()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    current_day = str(datetime.now().year) + ', ' + str(datetime.now().month) + ', ' + str(datetime.now().day)
    current_day = datetime.strptime(current_day, '%Y, %m, %d').date()
    compare_date = random_date + timedelta(days=4)
    if compare_date > current_day:
        random_date = current_day - timedelta(days=5)
    return random_date


def get_random_dates():
    start_date, end_date = get_contract_start_and_end_dates()
    start_date = datetime.strptime(start_date, '%m/%d/%Y').date()
    eff_date = calculate_date_by_days(start_date).strftime('%m/%d/%Y')
    start_date = start_date.strftime('%m/%d/%Y')
    return start_date, eff_date


def get_random_year_by_date(target_date=None):
    now = datetime.now()
    year = random.choice([str(now.year - 1), str(now.year)])
    if target_date:
        if year in target_date:
            return year
        else:
            target_date = string_to_sparc_date(target_date)
            return str(target_date.year)
    else:
        return year


def string_to_sparc_date(string_date):
    if '-' in string_date:
        string_date = datetime.strptime(string_date, '%Y-%m-%d').date().strftime('%m/%d/%Y')
    if string_date == "":
        return string_date
    return datetime.strptime(string_date, '%m/%d/%Y').date()


def format_sparc_date(date_dict):
    output = "{}/{}/{}".format(date_dict["month"], date_dict["day"], date_dict["year"])
    return output


def validate_year_between_start_end_dates(start_date, end_date, years):
    t_years = []
    start_date = string_to_sparc_date(start_date)
    end_date = string_to_sparc_date(end_date)
    for year in years:
        if str(start_date.year) <= year <= str(end_date.year):
            t_years.append(year)
    return t_years


def validate_empty_date(target_date):
    if target_date != "":
        new_date = datetime.strptime(target_date, '%Y-%m-%d').date().strftime('%m/%d/%Y')
    else:
        new_date = target_date
    return new_date


def add_days_to_date(t_date, days_to_add):
    format_date = string_to_sparc_date(t_date)
    new_date = format_date + timedelta(days=days_to_add)
    return new_date


def add_months_to_date(t_date, months):
    month = t_date.month - 1 + months
    year = t_date.year + month // 12
    month = month % 12 + 1
    day = min(t_date.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def start_end_dates_without_overlapping(json_list, max_date: str = "2099-12-30", days_to_add: int = 182):
    parsed_array = contract_format_array(json_list)
    sorted_array = sort_array_by_start_date(parsed_array)
    return find_date_gap(sorted_array, max_date, days_to_add)


# Medicaid dates

def get_random_postmark_and_received_dates(quarter):
    start_date, end_date = get_start_and_end_dates_by_quarter(quarter)
    random_date = get_random_date_by_start_and_end_dates(start_date, end_date)
    postmark_date = random_date.strftime('%m/%d/%Y')
    received_date = calculate_received_date(random_date)
    received_date = received_date.strftime('%m/%d/%Y')
    return postmark_date, received_date


def calculate_received_date(start_date):
    received_date = start_date + timedelta(days=4)
    return received_date


def calculate_invalid_received_date(received_date_to_edit):
    received_date = datetime.strptime(received_date_to_edit, '%m/%d/%Y').date() - timedelta(days=10)
    return received_date.strftime('%m/%d/%Y')


def postmark_received_dates_equals(list_1, list_2, file_type):
    l1_d_1 = string_to_sparc_date(list_1[-1])
    l1_d_2 = string_to_sparc_date(list_1[-2])
    l2_d_1 = string_to_sparc_date(list_2[-1])
    l2_d_2 = string_to_sparc_date(list_2[-2])
    if file_type == UPDATED:
        if l1_d_1 == l2_d_1 or l1_d_2 == l2_d_2:
            return True
    else:
        if l1_d_1 == l2_d_1 and l1_d_2 == l2_d_2:
            return True
    return False


def validate_postmark_received_dates_changed(action_type, list_1, list_2, file_type):
    if action_type == APPROVE:
        if not postmark_received_dates_equals(list_1, list_2, file_type):
            return True
        return False
    if action_type == REJECT:
        if postmark_received_dates_equals(list_1, list_2, file_type):
            return True
        return False


def format_postmark_received_dates(postmark_list):
    new_list = [postmark_list[0], postmark_list[1], postmark_list[2]]
    if postmark_list[3] == "":
        p_date = ""
    elif '/' in postmark_list[3]:
        p_date = postmark_list[3]
    else:
        p_date = datetime.strptime(postmark_list[3], '%Y-%m-%d').date().strftime('%m/%d/%Y')
    new_list.append(p_date)
    if len(postmark_list) == 5:
        if postmark_list[4] == "":
            r_date = ""
        elif '/' in postmark_list[4]:
            r_date = postmark_list[4]
        else:
            r_date = datetime.strptime(postmark_list[4], '%Y-%m-%d').date().strftime('%m/%d/%Y')
        new_list.append(r_date)
    return new_list


def get_periods_for_file(year):
    periods = []
    for i in range(0, 4):
        period = year + "q" + str(i + 1)
        periods.append(period)
    return periods


# UBR dates

def get_contract_start_and_end_dates():
    now = datetime.now()
    year = now.year
    start_date = "{}/{}/{}".format("01", "01", str(year))
    end_date = "{}/{}/{}".format("12", "31", str(year))
    return start_date, end_date


def calculate_date_by_days(initial_date):
    target_date = initial_date + timedelta(days=10)
    return target_date


def generate_period_year_combinations(start_date, end_date, periods, years):
    py_combination = []
    t_years = validate_year_between_start_end_dates(start_date, end_date, years)
    for period in periods:
        for year in t_years:
            py_combination.append({"year": year, "period": period})
    return py_combination


def fdate(str_date):
    """
    ---------------------------------------------------------------------------
    This 'format-date' function converts a str_date to datetime_date.

    --Using Example:
        my_date = "1995-01-01"
     >> fdate(my_date)

    --Output example:
        datetime.datetime(1995, 1, 1, 0, 0)
    ---------------------------------------------------------------------------
    """
    return datetime.strptime(str_date, "%Y-%m-%d")


def fstrtime(datetime):
    """
    ---------------------------------------------------------------------------
    This function converts a datetime_date to str_date '%m%d%Y' format.

    --Using Example:
        my_date = datetime.datetime(1899, 12, 30, 0, 0)
     >> fstrtime(my_date)

    --Output example:
        '12301899'
    ---------------------------------------------------------------------------
    """
    return datetime.strftime('%m%d%Y')


def format_array_to_datetime(plists_array):
    """
    ---------------------------------------------------------------------------
    This function converts a string dates array to datetime dates array (Trading Partners only).

    --Using Example:
        string_dates_array = [{"start": "1995-01-01", "end": "1995-10-25"}, {}]
     >> format_array_to_datetime(string_dates_array)

    --Output example:
        [{"start": datetime.datetime(1995, 1, 1, 0, 0), ...}, {}]
    ---------------------------------------------------------------------------
    """
    new_array = []
    for plist in plists_array:
        new_array.append({"start": fdate(plist["list_start_date"]), "end": fdate(plist["list_end_date"])})
    return new_array


def contract_format_array(list_array):
    """
    ---------------------------------------------------------------------------
    This function converts a string dates array to datetime dates array (Contracts Only).

    --Using Example:
        string_dates_array = [{"start": "1995-01-01", "end": "1995-10-25"}, {}]
     >> format_array_to_datetime(string_dates_array)

    --Output example:
        [{"start": datetime.datetime(1995, 1, 1, 0, 0), ...}, {}]
    ---------------------------------------------------------------------------
    """
    new_array = []
    for single_list in list_array:
        if "contract_start_date" in single_list:
            new_start_date = "{}-{}-{}".format(single_list["contract_start_date"]["date"]["year"],
                                               single_list["contract_start_date"]["date"]["month"],
                                               single_list["contract_start_date"]["date"]["day"])
            new_end_date = "{}-{}-{}".format(single_list["contract_end_date"]["date"]["year"],
                                             single_list["contract_end_date"]["date"]["month"],
                                             single_list["contract_end_date"]["date"]["day"])
        elif "start_date" in single_list:
            if "date" in single_list["start_date"]:
                single_list["start_date"] = format_sparc_date(single_list["start_date"]["date"])
                single_list["end_date"] = format_sparc_date(single_list["end_date"]["date"])
            new_start_date = datetime.strptime(single_list["start_date"], '%m/%d/%Y').date().strftime('%Y-%m-%d')
            new_end_date = datetime.strptime(single_list["end_date"], '%m/%d/%Y').date().strftime('%Y-%m-%d')
        new_array.append({"start": datetime.strptime(new_start_date, "%Y-%m-%d"),
                          "end": datetime.strptime(new_end_date, "%Y-%m-%d")})
    return new_array


def sort_array_by_start_date(array):
    """
    ---------------------------------------------------------------------------
    This function sorts a datetime dates objects array by start_date.

    --Using Example:
        unsorted_datetime_array = [{"start": datetime.datetime(1899, 12, 30, 0, 0), ...}, {}]
     >> sort_array_by_start_date(unsorted_datetime_array)

    --Output will be same array structure but sorted !
    ---------------------------------------------------------------------------
    """
    return sorted(array, key=lambda item: item['start'])


def find_date_gap(array, max_date="2099-12-30", days_to_add=2):
    """
    ---------------------------------------------------------------------------
    This function finds a date "gap" for a given datetime date objects array,
    and based on that it will return a new start/end str_date object to be used.

    --Using Example:
        sorted_datetime_array = [{"start": datetime.datetime(1899, 12, 30, 0, 0), ...}, {}]
     >> find_date_gap(sorted_datetime_array)

    --Output example, will be inserted as text on UI form date selectors:
        {'start': '01011900', 'end': '02011900'}
    ---------------------------------------------------------------------------
    """
    max_date = fdate(max_date)
    saved_start_date = None
    saved_end_date = None
    counter = 0
    if len(array) == 1:
        return {"start": fstrtime(array[0]["end"] + timedelta(days=1)),
                "end": fstrtime(array[0]["end"] + timedelta(days=days_to_add))}
    for date in array:
        # case0: behavior when max date detected or rebased.
        if date["start"] >= max_date or date["end"] >= max_date:
            return {"start": fstrtime(array[0]["start"] + timedelta(days=-days_to_add)),
                    "end": fstrtime(array[0]["start"] + timedelta(days=-1))}
        else:
            counter += 1
            # case1: saving dates on first iteration.
            if not saved_start_date:
                saved_start_date = date["start"]
                saved_end_date = date["end"]
                continue
            # case2: updating saved dates if overlaps.
            if (date["start"] - saved_end_date).days <= days_to_add:
                saved_start_date = date["start"]
                if (date["end"] - saved_end_date).days > 0:
                    saved_end_date = date["end"]
            # case3: return first date gap found.
            if (date["start"] - saved_end_date).days > days_to_add:
                return {"start": fstrtime(saved_end_date + timedelta(days=1)),
                        "end": fstrtime(saved_end_date + timedelta(days=days_to_add))}
            # case4: solving when array iterations ends.
            if counter == len(array):
                return {"start": fstrtime(saved_end_date + timedelta(days=1)),
                        "end": fstrtime(saved_end_date + timedelta(days=days_to_add))}


"""Author : Sadiya Kotwal
       Description : This method selects date(MOnth/Date/Year) from clender 
                     Provude input agrument as below. 
       Arguments : date_format(Eg:date_format="06/14/2023"  MM/DD/YYYY)
       Returns : NA"""


def select_date_from_calender(self, date_format):
    allure.attach("User entered date as : " + date_format, attachment_type=allure.attachment_type.TEXT)
    new_formated_date = convert_date(date_format)
    split_date = new_formated_date.split('/')
    month = split_date[0]
    date = split_date[1]
    year = split_date[2]
    select_month(self, month)
    select_year(self, year)
    select_date(self, date)
    allure.attach("User selected date as : " + month + " " + date + " " + year,
                  attachment_type=allure.attachment_type.TEXT)


"""Author : Sadiya Kotwal
       Description : This method sconverts date format          
       Arguments : date_str(Eg:date_str="06/14/2023"  MM/DD/YYYY)
       Returns : NA"""


def convert_date(date_str):
    date = datetime.strptime(date_str, '%m/%d/%Y')
    # Convert the date to the desired format
    formatted_date = date.strftime('%b/%d/%Y')
    return formatted_date


"""Author : Sadiya Kotwal
       Description : This method selects month from calender      
       Arguments : month(Eg:month= "Jan")
       Returns : NA"""


def select_month(self, month):
    button_month = "//div[@class='headermonthtxt']/button"
    get_month = forms.get_text_on_element(self, "XPATH", button_month)
    if month == get_month:
        allure.attach("User entered month which is already selected: " + month,
                      attachment_type=allure.attachment_type.TEXT)
    else:
        mouse.click_on_element(self, "XPATH", button_month)
        allure.attach("User can click on month button from calender : ", attachment_type=allure.attachment_type.TEXT)
        click_on_particular_month = "(//table[contains(@class,'monthtable')]/child::tbody/child::tr/child::td/child::div[text()='" + month + "'])[1]"
        mouse.click_on_element(self, "XPATH", click_on_particular_month)
        allure.attach("User can click on month : " + month, attachment_type=allure.attachment_type.TEXT)


"""Author : Sadiya Kotwal
       Description : This method selects year from calender      
       Arguments : year(Eg:year= "2021" or any year)
       Returns : NA"""


def select_year(self, year):
    button_year = "//div[@class='headeryeartxt']/button"
    get_year = forms.get_text_on_element(self, "XPATH", button_year)
    if year == get_year:
        allure.attach("User entered year which is already selected: " + year,
                      attachment_type=allure.attachment_type.TEXT)
    else:
        mouse.click_on_element(self, "XPATH", button_year)
        for i in range(1, 26):
            txt_year = "(//table[contains(@class,'yeartable')]/child::tbody/child::tr/child::td/child::div)[" + str(
                i) + "]"
            txt_get_year = forms.get_text_on_element(self, "XPATH", txt_year)
            txt_last_year_for_current_board = "(//table[contains(@class,'yeartable')]/child::tbody/child::tr/child::td/child::div)[25]"
            txt_get_last_year_for_current_board = forms.get_text_on_element(self, "XPATH",
                                                                            txt_last_year_for_current_board)
            if year == txt_get_last_year_for_current_board:
                mouse.click_on_element(self, "XPATH", txt_last_year_for_current_board)
                allure.attach("User can click on year: " + year, attachment_type=allure.attachment_type.TEXT)
                break
            elif year > txt_get_last_year_for_current_board:
                bln_flag = False
                counter = 0
                while bln_flag == False:
                    next_button = "//button[@class='yearchangebtn mydpicon icon-mydpdown yearchangebtnenabled']"
                    mouse.click_on_element(self, "XPATH", next_button)
                    counter = counter + 1
                    allure.attach("User can click on next arrow : " + str(counter),
                                  attachment_type=allure.attachment_type.TEXT)
                    first_year = "(//table[contains(@class,'yeartable')]/child::tbody/child::tr/child::td/child::div)[1]"
                    last_year = "(//table[contains(@class,'yeartable')]/child::tbody/child::tr/child::td/child::div)[25]"
                    txt_get_first_year = forms.get_text_on_element(self, "XPATH", first_year)
                    txt_get_last_year = forms.get_text_on_element(self, "XPATH", last_year)
                    if year == txt_get_first_year:
                        mouse.click_on_element(self, "XPATH", first_year)
                        allure.attach("User can click on year : " + year, attachment_type=allure.attachment_type.TEXT)
                        bln_flag = True
                        break
                    elif year == txt_get_last_year:
                        mouse.click_on_element(self, "XPATH", last_year)
                        allure.attach("User can click on year : " + year, attachment_type=allure.attachment_type.TEXT)
                        bln_flag = True
                        break
                    elif (year > txt_get_first_year) and (year < txt_get_last_year):
                        click_on_year_new = "(//table[contains(@class,'yeartable')]/child::tbody/child::tr/child::td/child::div[text()='" + year + "'])[1]"
                        mouse.click_on_element(self, "XPATH", click_on_year_new)
                        allure.attach("User can click on year : " + year, attachment_type=allure.attachment_type.TEXT)
                        bln_flag = True
                        break
                break
            elif (year > txt_get_year) and (year < txt_get_last_year_for_current_board):
                click_on_year = "(//table[contains(@class,'yeartable')]/child::tbody/child::tr/child::td/child::div[text()='" + year + "'])[1]"
                mouse.click_on_element(self, "XPATH", click_on_year)
                allure.attach("User can click on year : " + year, attachment_type=allure.attachment_type.TEXT)
                break
            elif year < txt_get_year:
                bln_flag = False
                counter = 0
                while bln_flag == False:
                    previous_button = "//button[@class='yearchangebtn mydpicon icon-mydpup yearchangebtnenabled']"
                    mouse.click_on_element(self, "XPATH", previous_button)
                    counter = counter + 1
                    allure.attach("User can click on previous arrow : " + str(counter),
                                  attachment_type=allure.attachment_type.TEXT)
                    first_year = "(//table[contains(@class,'yeartable')]/child::tbody/child::tr/child::td/child::div)[1]"
                    last_year = "(//table[contains(@class,'yeartable')]/child::tbody/child::tr/child::td/child::div)[25]"
                    txt_get_first_year = forms.get_text_on_element(self, "XPATH", first_year)
                    txt_get_last_year = forms.get_text_on_element(self, "XPATH", last_year)
                    if year == txt_get_first_year:
                        mouse.click_on_element(self, "XPATH", first_year)
                        allure.attach("User can click on year : " + year, attachment_type=allure.attachment_type.TEXT)
                        bln_flag = True
                        break
                    elif year == txt_get_last_year:
                        mouse.click_on_element(self, "XPATH", last_year)
                        allure.attach("User can click on year : " + year, attachment_type=allure.attachment_type.TEXT)
                        bln_flag = True
                        break
                    elif (year > txt_get_first_year) and (year < txt_get_last_year):
                        click_on_year_new = "(//table[contains(@class,'yeartable')]/child::tbody/child::tr/child::td/child::div[text()='" + year + "'])[1]"
                        mouse.click_on_element(self, "XPATH", click_on_year_new)
                        allure.attach("User can click on year : " + year, attachment_type=allure.attachment_type.TEXT)
                        bln_flag = True
                        break

                break
            break


"""Author : Sadiya Kotwal
       Description : This method selects date from calender
                     Even if the user has provided date as 01 or 09 it takes as 1 to 9 
                     as in application date is single format for  1 - 9 dates    
       Arguments : date(Eg:date= "1" or any date)
       Returns : NA"""


def select_date(self, date):
    if date.startswith('0'):
        date_new = date[1:]
        select_date_from_calender_popup_1 = "//div[contains(@class,'datevalue currmonth')]/child::span[text()='" + date_new + "']"
        mouse.click_on_element(self, "XPATH", select_date_from_calender_popup_1)
        allure.attach("User can select date as : " + date_new, attachment_type=allure.attachment_type.TEXT)
    else:
        select_date_from_calender_popup = "//div[contains(@class,'datevalue currmonth')]/child::span[text()='" + date + "']"
        mouse.click_on_element(self, "XPATH", select_date_from_calender_popup)
        allure.attach("User can select date as : " + date, attachment_type=allure.attachment_type.TEXT)

def get_system_current_date(date_format):
        system_current_date = date.today()
        system_date = system_current_date.strftime(date_format)
        return system_date