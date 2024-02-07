import itertools
import math
import os
import random
import operator
from collections import Counter
from datetime import datetime
from libraries import dates, files, generics, cnp_logs
from sparc_pages.constants import *

LOGGER = cnp_logs.get_logger("general_sparc")


class LoginSparc:
    @staticmethod
    def do_login(sparc_api):
        LOGGER.info("logging in")
        username = os.environ.get("SPARC_USER_NAME", None)
        password = os.environ.get("SPARC_PASSWORD", None)
        sparc_api.login(username, password)
        LOGGER.info("logging created")

        LOGGER.info("choosing client and service")
        service_name = os.environ.get("SPARC_SERVICE_NAME", None)
        client_name = os.environ.get("SPARC_CLIENT_NAME", None)
        contract = sparc_api.get_client_by(client_name, service_name)
        if contract:
            sparc_api.choose_services(contract)
            LOGGER.info("session started")
            return True
        return False


class CommonOperations:
    @staticmethod
    def format_status(full_status):
        status = full_status["status"]
        if status == ACTIVE:
            if PENDING in full_status.keys():
                if full_status["PENDING"] is True:
                    status = "ACTIVE (PENDING)"
                    return status
            elif DRAFT in full_status.keys():
                if full_status["DRAFT"] is True:
                    status = "ACTIVE (DRAFT)"
                    return status
        return status


class EntityOperations:
    @staticmethod
    def parse_entities_data(data):
        entities = {}
        for entity in data:
            if entity["state_id"] in entities.keys():
                entities[entity["state_id"]].append({"id": entity["program_id"],
                                                     "name": entity["program_code"]})
            else:
                entities[entity["state_id"]] = [{"id": entity["program_id"],
                                                 "name": entity["program_code"]}]
        return entities

    @staticmethod
    def parse_programs_data(data):
        programs = []
        for program in data["rows"]:
            programs.append(
                {
                    "program_id": program["id"],
                    "program": program["program_code"],
                    "rpu_type": program["rpu_type"],
                    "program_group": program["program_group"]

                }
            )
        return programs

    @staticmethod
    def contains_program_by_state(entity, invoices):
        for invoice in invoices:
            if invoice["program_id"] == entity["id"] and invoice["state_id"] == entity["state"]:
                return True
        return False

    @staticmethod
    def contains_program_by_state_and_quarter(entity, quarter, labeler, invoices):
        for invoice in invoices:
            if invoice["program_id"] == entity["id"] and invoice["state_id"] == entity["state"] and \
                    invoice["util_quarter"] == quarter and invoice["labeler"] == labeler:
                return True
        return False

    @staticmethod
    def filter_programs_by_program_group(programs, rpu_type, list_groups):
        filter_programs = []
        for program in programs:
            if program["rpu_type"] == rpu_type:
                if program["program_group"] in list_groups:
                    filter_programs.append(program)
        return filter_programs

    @staticmethod
    def get_available_entities(filter_programs_id, entities, invoices):
        available = []
        for key, value in entities.items():
            programs = [program for program in value if program["id"] in filter_programs_id]
            for program in programs:
                entity = {"state": key, "id": program["id"], "name": program["name"]}
                if not EntityOperations.contains_program_by_state(entity, invoices):
                    available.append({"state": key, "program": program})
        return available

    @staticmethod
    def get_available_entities_current_quarter(filter_programs_id, entities, invoices, quarters, labeler):
        available = []
        for key, value in entities.items():
            programs = [program for program in value if program["id"] in filter_programs_id]
            for program in programs:
                entity = {"state": key, "id": program["id"], "name": program["name"]}
                for quarter in quarters:
                    if not EntityOperations.contains_program_by_state_and_quarter(entity, quarter, labeler, invoices):
                        available.append({"state": key, "program": program, "quarter": quarter, "labeler": labeler})
        return available


class PricingOperations:

    @staticmethod
    def parse_pricing_data(data):
        new_data = []
        for pricing in data:
            new_data.append(
                {
                    "status": CommonOperations.format_status(pricing["edit_state"]),
                    "NDC11": pricing["product"]["ndc11"],
                    "Product Name": pricing["product"]["product_name"],
                    "Price Type": pricing["price_type"],
                    "Unit Price NDC11": pricing["unit_price_ndc11"],
                    "Period Type": pricing["period_type"],
                    "Start Date": dates.format_sparc_date(pricing["start_date"]["date"]),
                    "End Date": dates.format_sparc_date(pricing["end_date"]["date"]),
                    "Effective Date": dates.format_sparc_date(pricing["effective_date"]["date"]),
                    "Expiration Date": dates.format_sparc_date(pricing["expiration_date"]["date"]),
                    "modified_on": pricing["modified_on_tmz"]
                }
            )
        return new_data

    @staticmethod
    def filter_pricing_data(data, status, price_type):
        elements = []

        for price in data:
            if price["status"] == status:
                if price["Price Type"] == price_type:
                    if price["Start Date"] <= price["Effective Date"]:
                        elements.append(price)
        elements.sort(key=lambda element: datetime.strptime(element["Start Date"], '%d/%m/%Y'))
        exp_date = elements[-1]["End Date"].split('/')
        year = exp_date[2]
        exp_date = exp_date[1] + '/' + exp_date[0]

        quarter = [q_item for q_item, value in QUARTER_RANGE.items() if value == exp_date][0]
        util_quarter = year + 'q' + quarter
        labeler = elements[-1]["NDC11"]
        pricing = {
            "labeler": labeler[0:5],
            "NDC11": elements[-1]["NDC11"],
            "year": year,
            "quarter": quarter,
            "util_quarter": util_quarter,
            "Start Date": elements[-1]["Start Date"],
            "End Date": elements[-1]["End Date"]
        }
        return pricing

    @staticmethod
    def filter_pricing_by_date(price, date_type, t_date):
        if price[f'{date_type}'] in t_date:
            return True
        return False

    @staticmethod
    def filter_pricing_by_status(data, status, date_type, t_date=None):
        elements = []
        for price in data:
            if price["status"] == status:
                if t_date is not None:
                    has_date = PricingOperations.filter_pricing_by_date(price, date_type, t_date)
                    if has_date:
                        elements.append(price)
                elements.append(price)
        return elements

    @staticmethod
    def filter_pricing_by_ndc11(data, ndc11):
        elements = []
        for price in data:
            if price["NDC11"] == ndc11:
                elements.append(price)
        return elements

    @staticmethod
    def get_price_by_period(period):
        if "1" in period[-1:]:
            return "1"
        if "2" in period[-1:]:
            return "2"
        if "3" in period[-1:]:
            return "3"
        if "4" in period[-1:]:
            return "4"

    @staticmethod
    def get_data_to_create_pricing_file(products, pricings):
        new_pricing = ProductsOperations.get_ndc11_list_by_products(products)
        ndc11_list = random.sample(new_pricing["list"], 4)
        eff_start, eff_date = dates.get_random_dates()
        year = dates.get_random_year_by_date(eff_start)
        new_pricing["path"] = "/Medicaid/automation_test/uploadfiles/pricing_load " + new_pricing["labeler"] + ".csv"
        new_pricing["data"] = "ndc11,price_type,price,period,start_date,end_date,eff_start,eff_end"
        for ndc11 in ndc11_list:
            periods = dates.get_periods_for_file(year)
            for period in periods:
                price = PricingOperations.get_price_by_period(period)
                pricing_data = (
                        "\n" + ndc11 + "," + "URA" + "," + price + ".0000" + "," + period + "," + "" + "," + "" + "," +
                        eff_start + "," + "12/31/2099")
                check_data = {"NDC11": ndc11, "Price Type": "URA", "Unit Price NDC11": price + ".0000",
                              "Period Type": period, "Effective Date": eff_start, "Expiration Date": "12/31/2099"}
                pricing_list = PricingOperations.filter_pricing_by_ndc11(pricings, ndc11)
                for pricing in pricing_list:
                    pricing_nor = PricingOperations.normalize_pricing_data(pricing, "NA")
                    check_data_nor = PricingOperations.normalize_pricing_data(check_data, "NA")
                    if check_data_nor != pricing_nor:
                        if pricing_data not in new_pricing["data"]:
                            new_pricing["data"] += pricing_data
                    pricing_list.remove(pricing)
        return new_pricing

    @staticmethod
    def normalize_pricing_data(pricing, file_type=UPDATED):
        if 'float' not in str(type(pricing["Unit Price NDC11"])):
            pricing["Unit Price NDC11"] = float(pricing["Unit Price NDC11"])
        if "new_price" in pricing:
            pricing = generics.remove_dict_key(pricing, "new_price")
        if file_type != UPDATED or file_type != "UPLOADED":
            if "Start Date" in pricing:
                if "/" in pricing["Start Date"]:
                    pricing["Start Date"] = datetime.strptime(pricing["Start Date"], '%m/%d/%Y').date().strftime(
                        '%m/%d/%Y')
                elif pricing["Start Date"] == "":
                    pricing["Start Date"] = pricing["Start Date"]
                else:
                    pricing["Start Date"] = datetime.strptime(pricing["Start Date"], '%Y-%m-%d').date().strftime(
                        '%m/%d/%Y')
            if "End Date" in pricing:
                if "/" in pricing["End Date"]:
                    pricing["End Date"] = datetime.strptime(pricing["End Date"], '%m/%d/%Y').date().strftime('%m/%d/%Y')
                elif pricing["End Date"] == "":
                    pricing["End Date"] = pricing["End Date"]
                else:
                    pricing["End Date"] = datetime.strptime(pricing["End Date"], '%Y-%m-%d').date().strftime('%m/%d/%Y')
            if "Effective Date" in pricing:
                if "/" in pricing["Effective Date"]:
                    pricing["Effective Date"] = datetime.strptime(pricing["Effective Date"],
                                                                  '%m/%d/%Y').date().strftime('%m/%d/%Y')
                else:
                    pricing["Effective Date"] = datetime.strptime(pricing["Effective Date"],
                                                                  '%Y-%m-%d').date().strftime('%m/%d/%Y')
            if "Expiration Date" in pricing:
                if "/" in pricing["Expiration Date"]:
                    pricing["Expiration Date"] = datetime.strptime(pricing["Expiration Date"],
                                                                   '%m/%d/%Y').date().strftime('%m/%d/%Y')
                else:
                    pricing["Expiration Date"] = datetime.strptime(pricing["Expiration Date"],
                                                                   '%Y-%m-%d').date().strftime('%m/%d/%Y')
            if "status" in pricing:
                pricing = generics.remove_dict_key(pricing, "status")
            if "modified_on" in pricing:
                pricing = generics.remove_dict_key(pricing, "modified_on")
            if "Period Type" in pricing:
                pricing = generics.remove_dict_key(pricing, "Period Type")
            if "Product Name" in pricing:
                pricing = generics.remove_dict_key(pricing, "Product Name")
                pricing = generics.remove_dict_key(pricing, "Start Date")
                pricing = generics.remove_dict_key(pricing, "End Date")
        if file_type == UPDATED or file_type == "UPLOADED":
            if "Product Name" in pricing:
                pricing = generics.remove_dict_key(pricing, "Product Name")
            if "Effective Date" in pricing:
                pricing = generics.remove_dict_key(pricing, "Effective Date")
            if "Expiration Date" in pricing:
                pricing = generics.remove_dict_key(pricing, "Expiration Date")
            if "Start Date" in pricing:
                pricing = generics.remove_dict_key(pricing, "Start Date")
            if "End Date" in pricing:
                pricing = generics.remove_dict_key(pricing, "End Date")
        return pricing

    @staticmethod
    def validate_price(target_price):
        price = str(target_price).split('.')[0]
        if len(price) > 3:
            if len(price) > 6:
                new_price = price[:-6] + ',' + price[-6:-3] + ',' + price[-3:]
            else:
                new_price = price[:-3] + ',' + price[-3:]
        else:
            new_price = target_price
        return new_price


class ProgramTemplatesOpeartion:
    @staticmethod
    def parse_program_data(data):
        new_data = []
        for pricing in data:
            new_data.append(
                {
                    "status": CommonOperations.format_status(pricing["edit_state"]),
                    "program_code": pricing["program_code"],
                    "description": pricing["program_desc"],
                    "designation": pricing["designation_display"],
                    "program_type": pricing["program_type"],
                    "program_group": pricing["program_group"],
                    "rpu_type": pricing["rpu_type"]
                }
            )
        return new_data


class ApprovalsOperations:
    @staticmethod
    def parse_dates(fields_list):
        out_list = []
        for element in fields_list:
            if isinstance(element, dict):
                for field in element.keys():
                    if isinstance(element[field], dict):
                        if "date" in element[field]:
                            element[field] = dates.format_sparc_date(element[field]["date"])
            out_list.append(element)
        return out_list

    @staticmethod
    def parse_approvals_data(data):
        approvals = []
        for approval in data["data"]:
            approvals.append(
                {
                    "diff_type": approval["diff_type"],
                    "client_id": approval["client"]["id"],
                    "client": approval["client"]["pretty_name"],
                    "old_id": approval["old_id"],
                    "delete": approval["delete"],
                    "fields": ApprovalsOperations.parse_dates(approval["diff_data"]["data"]["diffs"])
                }
            )
        return approvals

    @staticmethod
    def filter_approvals_by_diff_type(approvals, diff_type):
        filter_approvals = []
        for approval in approvals:
            if approval["diff_type"] == diff_type:
                filter_approvals.append(approval)
        return filter_approvals

    @staticmethod
    def get_fields_to_compare(approval):
        fields_to_compare = []
        for field in approval:
            if field["name"] == "program" or field["name"] == "state" or field["name"] == "util_quarter":
                fields_to_compare.append(field["new"])
        return fields_to_compare

    @staticmethod
    def invoices_with_postmark_contains_approval(field, invoices):
        for invoice in invoices:
            if invoice["program"] == field[0] and invoice["state"] == field[1] and invoice["util_quarter"] == field[2]:
                return True
        return False

    @staticmethod
    def get_postmarks_with_pending_approvals(filter_approvals, invoices_with_postmark):
        target_approvals = []
        for approval in filter_approvals:
            fields = ApprovalsOperations.get_fields_to_compare(approval["fields"])
            if ApprovalsOperations.invoices_with_postmark_contains_approval(fields, invoices_with_postmark):
                target_approvals.append(approval)
        return target_approvals

    @staticmethod
    def filter_approvals_by_file_type(approvals_list, file_type):
        filter_approvals = []
        for approval in approvals_list:
            if file_type == "(Updated)" and approval["old_id"] is not None:
                filter_approvals.append(approval)
            if file_type == "(New)" and approval["delete"] is False and approval["old_id"] is None:
                filter_approvals.append(approval)
            if file_type == "(Deleted)" and approval["delete"] is True:
                filter_approvals.append(approval)
        return filter_approvals

    @staticmethod
    def validate_fields_updated(validate_fields, info_list):
        new_list = []
        for info in info_list:
            try:
                value = [value for key, value in validate_fields.items() if key == info][0]
            except IndexError:
                value = ""
            new_list.append(value)
        return new_list

    @staticmethod
    def format_approval_data_to_compare(data_list, file_type):
        formatted_list = []
        val_fields_old = {}
        val_fields_new = {}
        info_list = ["program", "state", "util_quarter", "postmark_date", "received_date"]
        for field in data_list["fields"]:
            if field["name"] in info_list:
                if file_type == "(Updated)":
                    val_fields_old[field["name"]] = field["old"]
                    val_fields_new[field["name"]] = field["new"]
                else:
                    formatted_list.append(field["new"])
        if file_type == "(Updated)":
            old = ApprovalsOperations.validate_fields_updated(val_fields_old, info_list)
            formatted_list.append({"old": old})
            new = ApprovalsOperations.validate_fields_updated(val_fields_new, info_list)
            formatted_list.append({"new": new})
        return formatted_list


class ContractClientOperations:
    @staticmethod
    def parse_contract_client_data(data):
        contracts_client = []
        for contract_client in data:
            contracts_client.append(
                {
                    "contract_customer_id": contract_client["id"],
                    "customer_name": contract_client["customer_name"]
                }
            )
        return contracts_client

    @staticmethod
    def get_available_invoices_by_contract(invoices, contracts_client):
        available = []
        for invoice in invoices:
            if not ContractClientOperations.invoice_related_to_contract(invoice, contracts_client):
                available.append(invoice)
        return available

    @staticmethod
    def invoice_related_to_contract(invoice, contracts_client):
        for contract in contracts_client:
            if invoice["contracting_entity_id"] == contract["contract_customer_id"] \
                    and invoice["customer_name"] == contract["customer_name"]:
                return True
        return False


class ProductsOperations:
    @staticmethod
    def parse_products_data(data):
        new_data = []
        for product in data:
            new_data.append(
                {
                    "ndc11": product["ndc11"],
                    "status": product["status"]
                }
            )
        return new_data

    @staticmethod
    def filter_products_data(data, status):
        elements = []

        for product in data:
            if product["status"] == status:
                elements.append(product["ndc11"])
        return elements

    @staticmethod
    def get_labeler_by_products(products_list):
        ndcs = []
        for ndc_prod in products_list:
            ndcs.append(ndc_prod[:5])
        ndcs_dict = Counter(ndcs)
        labeler = max(ndcs_dict.items(), key=operator.itemgetter(1))[0]
        return labeler

    @staticmethod
    def get_ndcs_by_labeler(products_list, labeler):
        ndcs_list = []
        for product in products_list:
            if labeler in product:
                ndcs_list.append(product)
        return ndcs_list

    @staticmethod
    def get_ndc11_list_by_products(products):
        ndcs = {}
        products_list = []
        for product in products:
            if product["status"] == "ACTIVE":
                products_list.append(product["ndc11"])
        ndcs["labeler"] = ProductsOperations.get_labeler_by_products(products_list)
        ndcs_list = ProductsOperations.get_ndcs_by_labeler(products_list, ndcs["labeler"])
        ndcs["list"] = list(dict.fromkeys(ndcs_list))
        return ndcs

    @staticmethod
    def random_ndc11_as_str():
        return str(77777000000 + random.randint(0, 999999))

    @staticmethod
    def ndcs_generator(products):
        new_ndc11 = ProductsOperations.random_ndc11_as_str()
        ndc11_array = []
        for element in products:
            ndc11_array.append(element.get('ndc11', 'none'))
        while new_ndc11 in ndc11_array:
            new_ndc11 = ProductsOperations.random_ndc11_as_str()
        return new_ndc11

    @staticmethod
    def get_data_to_edit_product_file(products):
        product = {}
        ndcs_list = [ProductsOperations.ndcs_generator(products) for i in range(0, 10)]
        product["path"] = "/Medicaid/automation_test/uploadfiles/product.csv"
        file_data = files.read_csv_file(product["path"])
        count = 0
        for row in file_data:
            if row[0] == "ndc11":
                product["data"] = ','.join(row)
            elif row[0] != "ndc11":
                new_row = list(map(lambda x: x.replace(row[0], ndcs_list[count]), row))
                product["data"] += ("\n" + ','.join(new_row))
                count += 1
        return product


# Medicaid Classes


class MediInvoiceOperations:
    @staticmethod
    def parse_invoices_data(data):
        invoices = []
        for invoice in data:
            invoice_info = {
                "invoice_id": invoice["id"],
                "labeler": invoice["labeler"],
                "util_quarter": invoice["util_quarter"],
                "year": invoice["util_quarter"].split('q')[0],
                "quarter": invoice["util_quarter"].split('q')[1],
                "program_id": invoice["program_id"],
                "program": invoice["program"]["program_code"],
                "state_id": invoice["state_id"],
                "state": invoice["state"]["abbr"],
                "stage": invoice["stage"],
                "invoice_name": invoice["inv_num"],
                "postmark_date": "",
                "received_date": ""
            }
            if "date" in invoice["postmark_date"]:
                postmark_date = invoice["postmark_date"]["date"]
                invoice_info["postmark_date"] = dates.format_sparc_date(postmark_date)
            if "date" in invoice["received_date"]:
                received_date = invoice["received_date"]["date"]
                invoice_info["received_date"] = dates.format_sparc_date(received_date)
            invoices.append(invoice_info)
        return invoices

    @staticmethod
    def invoice_contains_postmark(invoices, postmark):
        for invoice in invoices:
            if invoice["state_id"] == postmark["state_id"] \
                    and invoice["program"] == postmark["program_name"] \
                    and invoice["util_quarter"] == postmark["util_quarter"]:
                return True
        return False

    @staticmethod
    def get_invoices_not_reconciled(invoices, util_quarter):
        target_invoices = []
        for invoice in invoices:
            condition = invoice["invoice_name"] == "" or invoice["received_date"] == "" and invoice[
                "postmark_date"] == ""
            if invoice["util_quarter"] == util_quarter and invoice["stage"] == 1 and condition is False:
                target_invoices.append({"invoice_id": str(invoice["invoice_id"]),
                                        "state_id": str(invoice["state_id"]),
                                        "program_id": str(invoice["program_id"])})
        return target_invoices

    @staticmethod
    def get_invoices_in_entry_stage(invoices):
        target_invoices = [invoice for invoice in invoices if invoice["stage"] == 1]
        return target_invoices

    @staticmethod
    def get_invoices_with_associated_postmarks(invoices, postmarks):
        target_invoices = []
        for invoice in invoices:
            if PostmarkOperations.postmark_contains_invoices(postmarks, invoice):
                target_invoices.append(invoice)
        return target_invoices

    @staticmethod
    def get_invoices_without_associated_postmarks(invoices, postmarks):
        target_invoices = []
        for invoice in invoices:
            if not PostmarkOperations.postmark_contains_invoices(postmarks, invoice):
                target_invoices.append(invoice)
        return target_invoices

    @staticmethod
    def invoice_contains_approval_data(invoices_list, approval_data, file_type):
        if file_type == "(Updated)":
            approval_data = approval_data[0]["old"]
        for invoice in invoices_list:
            if invoice["program"] == approval_data[0]:
                if invoice["state"] == approval_data[1] and invoice["util_quarter"] == approval_data[2]:
                    return invoice
        return invoice

    @staticmethod
    def invoice_contains_invoice_tracker(invoices_entry, invoice_tracker):
        for invoice in invoices_entry:
            if generics.compare_dicts(invoice, invoice_tracker) is True:
                return True
        return False

    @staticmethod
    def format_invoice_data_to_approval(data_list):
        formatted_list = [data_list["program"], data_list["state"], data_list["util_quarter"],
                          data_list["postmark_date"], data_list["received_date"]]
        return formatted_list

    @staticmethod
    def filter_invoice_by_name(invoices):
        target_invoices = [invoice for invoice in invoices if invoice["invoice_name"] != ""]
        return target_invoices


class PostmarkOperations:
    @staticmethod
    def parse_postmarks_data(data):
        postmarks = []
        for postmark in data:
            postmark_info = {
                "postmark_id": postmark["id"],
                "state_id": postmark["state"]["id"],
                "state_abbr": postmark["state"]["abbr"],
                "program_id": postmark["program_template"]["id"],
                "program_name": postmark["program_template"]["program_code"],
                "util_quarter": postmark["inv_quarter"],
                "year": postmark["inv_quarter"].split('q')[0],
                "quarter": postmark["inv_quarter"].split('q')[1],
                "status": postmark["edit_state"]["status"],
                "postmark_date": "",
                "received_date": ""
            }
            if "date" in postmark["postmark_date"]:
                postmark_date = postmark["postmark_date"]["date"]
                postmark_info["postmark_date"] = dates.format_sparc_date(postmark_date)
            if "date" in postmark["received_date"]:
                received_date = postmark["received_date"]["date"]
                postmark_info["received_date"] = dates.format_sparc_date(received_date)
            postmarks.append(postmark_info)
        return postmarks

    @staticmethod
    def get_postmarks_without_invoice(invoices, postmarks):
        target_postmarks = []
        for postmark in postmarks:
            if not MediInvoiceOperations.invoice_contains_postmark(invoices, postmark):
                target_postmarks.append(postmark)
        return target_postmarks

    @staticmethod
    def postmark_contains_invoices(postmarks, invoice):
        for postmark in postmarks:
            if postmark["state_id"] == invoice["state_id"] \
                    and postmark["program_name"] == invoice["program"] \
                    and postmark["util_quarter"] == invoice["util_quarter"]:
                return True
        return False

    @staticmethod
    def postmarks_available_to_create_invoice(program_names, target_postmarks, util_quarter):
        postmarks_available = []
        postmarks = [postmark for postmark in target_postmarks if postmark["program_name"] in program_names]
        for postmark in postmarks:
            if postmark["util_quarter"] == util_quarter and postmark["status"] == "ACTIVE":
                postmarks_available.append(postmark)
        return postmarks_available

    @staticmethod
    def equals(postmark_1, postmark_2, file_type):
        postmark_1 = dates.format_postmark_received_dates(postmark_1)
        postmark_2 = dates.format_postmark_received_dates(postmark_2)
        if postmark_1[:3] == postmark_2[:3] and dates.postmark_received_dates_equals(postmark_1, postmark_2, file_type):
            return True
        return False

    @staticmethod
    def postmark_contains_approval_data(postmarks_list, approval_data, file_type):
        if file_type == "(Updated)":
            approval_data = approval_data[0]["old"]
        for postmark in postmarks_list:
            if postmark["program_name"] == approval_data[0] and postmark["state_abbr"] == approval_data[1] and \
                    postmark["util_quarter"] == approval_data[2]:
                return postmark
        return None

    @staticmethod
    def format_postmark_data_to_compare(data_list):
        formatted_list = [data_list["program_name"], data_list["state_abbr"], data_list["util_quarter"],
                          data_list["postmark_date"], data_list["received_date"]]
        return formatted_list

    @staticmethod
    def normalize_postmark_data(postmark):
        if "Invoice Quarter" not in postmark:
            postmark["Invoice Quarter"] = postmark["year"] + 'q' + postmark["quarter"]
        if "year" in postmark:
            postmark = generics.remove_dict_key(postmark, "year")
        if "quarter" in postmark:
            postmark = generics.remove_dict_key(postmark, "quarter")
        postmark_list = [postmark["Program"], postmark["State"], postmark["Invoice Quarter"], postmark["Postmark Date"],
                         postmark["Received Date"]]
        return postmark_list


class PaymentTrackerOperations:
    @staticmethod
    def parse_payment_tracker_data(data):
        payment_tracker = []
        for payment in data["rows"]:
            pt_info = {
                "labeler": payment["labeler"],
                "state_id": payment["state_id"],
                "state": payment["state"],
                "program_id": payment["program_id"],
                "program": payment["program"],
                "util_quarter": payment["util_quarter"],
                "postmark_date": "",
                "received_date": "",
                "client_id": payment["client_id"],
                "client_name": payment["client_name"]
            }
            if "date" in payment["postmark_date"]:
                postmark_date = payment["postmark_date"]["date"]
                pt_info["postmark_date"] = dates.format_sparc_date(postmark_date)
            if "date" in payment["received_date"]:
                received_date = payment["received_date"]["date"]
                pt_info["received_date"] = dates.format_sparc_date(received_date)
            payment_tracker.append(pt_info)
        return payment_tracker

    @staticmethod
    def filter_tracker_by_state_and_quarter(payment_tracker, state, quarter):
        filter_payment_tracker = []
        for payment in payment_tracker:
            if payment["state"] == state and payment["util_quarter"] == quarter:
                filter_payment_tracker.append(payment)
        return filter_payment_tracker

    @staticmethod
    def tracker_contains_approval_data(payment_tracker_list, approval_data, file_type):
        if file_type == "(Updated)":
            approval_data = approval_data[0]["old"]
        for tracker in payment_tracker_list:
            if tracker["program"] == approval_data[0]:
                if tracker["state"] == approval_data[1] and tracker["util_quarter"] == approval_data[2]:
                    return tracker
        return tracker

    @staticmethod
    def format_tracker_data_to_compare(data_list):
        formatted_list = [data_list["program"], data_list["state"], data_list["util_quarter"],
                          data_list["postmark_date"], data_list["received_date"]]
        return formatted_list

    @staticmethod
    def normalize_tracker_data(data):
        data = generics.remove_dict_key(data, "client_id")
        data = generics.remove_dict_key(data, "year")
        data = generics.remove_dict_key(data, "labeler")
        return data

    @staticmethod
    def get_invoices_tracker_without_invoices_entry(invoices_tracker, invoices_entry):
        available_invoices = []
        for invoice_tracker in invoices_tracker:
            if not MediInvoiceOperations.invoice_contains_invoice_tracker(invoices_entry, invoice_tracker):
                available_invoices.append(invoice_tracker)
        return available_invoices


class DocumentOperations:
    @staticmethod
    def has_the_same_info(document_1, document_2):
        fields = ["program", "state", "quarter"]
        for field in fields:
            if not document_1[field] == document_2[field]:
                return False
        if dates.postmark_received_dates_equals(document_1, document_2):
            return True


# UBR Classes


class UbrInvoiceOperations:
    @staticmethod
    def parse_invoice_data(data):
        new_data = []
        for invoice in data:
            new_data.append(
                {
                    "invoice_id": invoice["id"],
                    "invoice_name": invoice['invoice_name'],
                    "contracting_entity_id": invoice["contracting_entity"]["id"],
                    "customer_name": invoice["contracting_entity"]["customer_name"],
                    "year": invoice["year"],
                    "period": invoice["period"]
                }
            )
        return new_data

    @staticmethod
    def invoice_contains_contract(invoices, contract):
        for invoice in invoices:
            if invoice["customer_name"] == contract["customer_name"] \
                    and invoice["year"] == contract["year"] \
                    and invoice["period"] == contract["period"]:
                return True
        return False

    @staticmethod
    def get_invoices_available(invoices, contracts):
        target_contracts = []
        for contract in contracts:
            if not UbrInvoiceOperations.invoice_contains_contract(invoices, contract):
                target_contracts.append(contract)
        return target_contracts

    @staticmethod
    def get_invoices_with_data(invoices):
        invoices_with_data = []
        for invoice in invoices:
            if invoice["reconciled_units"] != 0:
                invoices_with_data.append(invoice)
        return invoices_with_data

    @staticmethod
    def filter_invoices(
            invoices,
            stage=None,
            contract_name=None,
            customer_name=None,
            year=None,
            period=None,
            prepayment_allowed=None,
            modified_user=None, ):
        filters = []
        if stage:
            filters.append(lambda i: stage in str(i["stage"]))
        if contract_name:
            filters.append(lambda i: contract_name in i["contract"]["contract_name"])
        if customer_name:
            filters.append(lambda i: customer_name in i["contracting_entity"]["customer_name"])
        if year:
            filters.append(lambda i: year == i["year"])
        if period:
            filters.append(lambda i: period == i["period"])
        if prepayment_allowed:
            filters.append(lambda i: prepayment_allowed in i["contract"]["prepayment_allowed"])
        if modified_user:
            filters.append(lambda i: modified_user in i["modified_user"]["name"])
        try:
            return list(filter(lambda p: all(f(p) for f in filters), invoices))
        except StopIteration:
            return None

    @staticmethod
    def filter_invoice_files(
            invoice_files,
            filename=None, ):
        filters = []
        if filename:
            filters.append(lambda i: filename in i["filename"])
        try:
            return list(filter(lambda p: all(f(p) for f in filters), invoice_files))
        except StopIteration:
            return None

    @staticmethod
    def filter_invoices_by_filename(invoice, filename):
        for file in invoice["files"]:
            if filename in file["filename"]:
                return True
        return False

    @staticmethod
    def filter_non_esi_invoices(invoice):
        if invoice["contract"]["contract_type"] == MANAGED_CARE:
            if "EXPRESS SCRIPTS" not in invoice["contracting_entity"]["customer_name"]:
                return True
        return False

    @staticmethod
    def filter_non_ascent_invoices(invoice):
        if invoice["contract"]["contract_type"] == MANAGED_CARE:
            if "ASCENT" not in invoice["contracting_entity"]["customer_name"]:
                return True
        return False

    @staticmethod
    def filter_invoices_by_type(invoices, stage, invoice_type):
        available_invoices = []
        for invoice in invoices:
            if stage == str(invoice["stage"]):
                if invoice_type == "Non-ESI":
                    available = UbrInvoiceOperations.filter_non_esi_invoices(invoice)
                    if available:
                        available_invoices.append(invoice)
                if invoice_type == "Medical Claims":
                    available = UbrInvoiceOperations.filter_invoices_by_filename(invoice, MEDICAL)
                    if MEDICAL in invoice["contracting_entity"]["customer_name"] or available:
                        available_invoices.append(invoice)
                if invoice_type == "Ascent":
                    available_invoices = UbrInvoiceOperations.filter_invoices(invoices, stage=stage,
                                                                              customer_name="ASCENT")
                if invoice_type == "Non-Ascent":
                    available = UbrInvoiceOperations.filter_non_ascent_invoices(invoice)
                    if available:
                        available_invoices.append(invoice)
        return available_invoices

    @staticmethod
    def filter_invoice_data_by_type(invoices, stage, invoice_type):
        if invoice_type == "ESI":
            filtered_invoices = UbrInvoiceOperations.filter_invoices(invoices, stage=stage,
                                                                     customer_name="EXPRESS SCRIPTS")
        else:
            filtered_invoices = UbrInvoiceOperations.filter_invoices_by_type(invoices, stage, invoice_type)
        filtered_invoices = UbrInvoiceOperations.get_invoices_with_data(filtered_invoices)
        return filtered_invoices

    @staticmethod
    def filter_invoices_without_payment_portal(invoices):
        invoices_without_pp = []
        for invoice in invoices:
            if invoice["payment_portal"] is None:
                invoices_without_pp.append(invoice)
        return invoices_without_pp

    @staticmethod
    def get_invoices_available_according_to_the_user(json_invoices, stage, user_name=None):
        f_invoices = UbrInvoiceOperations.filter_invoices(json_invoices, stage=stage, modified_user=user_name,
                                                          prepayment_allowed='N')
        invoices_available = UbrInvoiceOperations.filter_invoices_without_payment_portal(f_invoices)
        return invoices_available


class UbrContractOperations:
    @staticmethod
    def parse_contracts_data(data):
        contracts = []
        for contract in data:
            contract_info = {
                "sb_id": contract["sb_id"],
                "contract_name": contract["contract_name"],
                "customer_id": contract["customer"]["id"],
                "customer_name": contract["customer"]["customer_name"],
                "status": CommonOperations.format_status(contract["edit_state"]),
                "contract_type": contract["contract_type"],
                "segment": contract["segment"],
                "contract_owner": contract["contract_owner"],
                "prepayment": contract["prepayment_allowed"]
            }
            if "date" in contract["contract_start_date"]:
                start_date = contract["contract_start_date"]["date"]
                contract_info["start_date"] = dates.format_sparc_date(start_date)
            if "date" in contract["contract_end_date"]:
                end_date = contract["contract_end_date"]["date"]
                contract_info["end_date"] = dates.format_sparc_date(end_date)
            contracts.append(contract_info)
        return contracts

    @staticmethod
    def filter_contracts(
            contracts,
            sb_id=None,
            customer_name=None,
            contract_name=None,
            contract_type=None,
            contract_owner=None,
            segment=None,
            status=None, ):
        filters = []
        if sb_id:
            filters.append(lambda c: sb_id == c["sb_id"])
        if customer_name:
            filters.append(lambda c: customer_name in c["customer_name"])
        if contract_name:
            filters.append(lambda c: contract_name in c["contract_name"])
        if contract_type:
            filters.append(lambda c: contract_type == c["contract_type"])
        if contract_owner:
            filters.append(lambda c: contract_owner in c["contract_owner"])
        if segment:
            filters.append(lambda c: segment == c["segment"])
        if status:
            filters.append(lambda c: status == CommonOperations.format_status(c["edit_state"]))
        try:
            return list(filter(lambda p: all(f(p) for f in filters), contracts))
        except StopIteration:
            return None

    @staticmethod
    def get_random_valid_contract(contracts):
        filter_contracts = []
        for contract in contracts:
            if contract["status"] == ACTIVE and contract["prepayment"] != "Y" and \
                    contract["contract_type"] == MANAGED_CARE and contract["customer_name"] != "DO NOT USE":
                filter_contracts.append(contract)
        return random.choice(filter_contracts)

    @staticmethod
    def get_contract_combination(contract, periods, years):
        target_contracts = []
        py_combinations = dates.generate_period_year_combinations(contract["start_date"],
                                                                  contract["end_date"],
                                                                  periods, years)
        for combination in py_combinations:
            target_contracts.append({"customer_id": contract["customer_id"],
                                     "customer_name": contract["customer_name"], "year": combination["year"],
                                     "period": combination["period"]})
        return target_contracts

    @staticmethod
    def normalize_contract(contract):
        contract["customer_name"] = contract["customer_name"].strip()
        contract["contract_type"] = contract["contract_type"].lower()
        contract["contract_type"] = contract["contract_type"].replace("_", " ")
        if "start_date" in contract:
            contract["start_date"] = datetime.strptime(contract["start_date"], '%m/%d/%Y').date().strftime('%m/%d/%Y')
        if "end_date" in contract:
            if contract["end_date"] == "":
                contract["end_date"] = "12/31/2099"
            else:
                contract["end_date"] = datetime.strptime(contract["end_date"], '%m/%d/%Y').date().strftime('%m/%d/%Y')
        if "contract_data_type" in contract:
            contract = generics.remove_dict_key(contract, "contract_data_type")
            contract = generics.remove_dict_key(contract, "submission_limit")
            contract = generics.remove_dict_key(contract, "contract_late_fee")
            contract = generics.remove_dict_key(contract, "submit_by_days")
            contract = generics.remove_dict_key(contract, "contract_id")
            contract = generics.remove_dict_key(contract, "days_to_pay")
            contract = generics.remove_dict_key(contract, "decimals")
        elif "sb_id" in contract:
            contract = generics.remove_dict_key(contract, "sb_id")
            contract = generics.remove_dict_key(contract, "customer_id")
            contract = generics.remove_dict_key(contract, "prepayment")
        return contract

    @staticmethod
    def normalize_contract_to_clone(contract):
        contract = generics.remove_dict_key(contract, "sb_id")
        contract = generics.remove_dict_key(contract, "contract_name")
        contract = generics.remove_dict_key(contract, "status")
        contract = generics.remove_dict_key(contract, "contract_owner")
        contract = generics.remove_dict_key(contract, "start_date")
        contract = generics.remove_dict_key(contract, "end_date")
        return contract

    @staticmethod
    def exclude_contract(contract_exc, contracts):
        for contract in contracts:
            if generics.compare_dicts(contract_exc, contract) is True:
                contracts.remove(contract)
        return contracts

    @staticmethod
    def get_contracts_to_exclude(contracts):
        contracts_to_exclude = []
        for cont_1, cont_2 in itertools.combinations(contracts, 2):
            cont1 = UbrContractOperations.normalize_contract_to_clone(cont_1)
            cont2 = UbrContractOperations.normalize_contract_to_clone(cont_2)
            if generics.compare_dicts(cont1, cont2) is True:
                contracts_to_exclude.append(cont_1)
                contracts_to_exclude.append(cont_2)
        return contracts_to_exclude

    @staticmethod
    def get_contracts_available_to_clone(contracts):
        new_contracts = []
        contracts_to_exclude = UbrContractOperations.get_contracts_to_exclude(contracts)
        if contracts_to_exclude:
            for contract_exc in contracts_to_exclude:
                new_contracts = UbrContractOperations.exclude_contract(contract_exc, contracts)
        else:
            for contract in contracts:
                if contract["status"] == "ACTIVE":
                    new_contracts.append(contract)
        return new_contracts

    @staticmethod
    def api_contract_payload(customer_id,
                             contract_type,
                             contract_owner,
                             start_date,
                             end_date):
        contract_name = "QA test " + str(random.randint(1, 999)) + " " + datetime.now().strftime("%Y-%m-%d")
        sd = datetime.strptime(start_date, '%m/%d/%Y')
        ed = datetime.strptime(end_date, '%m/%d/%Y')
        payload = {
            "contract_name": contract_name,
            "contract_type": contract_type,
            "customer_id": customer_id,
            "segment": random.choice(["Commercial", "Medicare Part D"]),
            "submission_limit": str(random.randint(1, 99)),
            "data_type": random.choice(["Utilization", "WAC Sales", "Indirect Sales"]),
            "late_fee": str(round(random.uniform(0.001, 0.999), 3)),
            "prepayment_allowed": "N",
            # "prepayment_pct": null,
            # "prepayment_pct_source":" ",
            "days_to_pay": str(random.randint(1, 90)),
            "days_to_submit": str(random.randint(1, 5)),
            "contract_owner": contract_owner,
            "contract_start_date": {
                "date": {
                    "year": sd.year,
                    "month": sd.month,
                    "day": sd.day
                }
            },
            "contract_end_date": {
                "date": {
                    "year": ed.year,
                    "month": ed.month,
                    "day": ed.day
                }
            },
            "rounding_spec": "ROUND_2"
        }
        return payload


class UbrRebateOperations:
    @staticmethod
    def compare_rebate_option_condition(rc_option_1, rc_option_2):
        if rc_option_1["cond_code"] == rc_option_2["cond_code"] and rc_option_1["cond_val"] == rc_option_2["cond_val"] \
                and rc_option_1["cond_val_code"] == rc_option_2["cond_val_code"]:
            return True
        return None

    @staticmethod
    def rc_options_contains_random_rc(rc_options, random_rc):
        for rc_option in rc_options:
            if not UbrRebateOperations.compare_rebate_option_condition(rc_option, random_rc):
                return True
        return None

    @staticmethod
    def generate_val_code_combinations(num_list, cond_val_list):
        combinations = []
        for num in num_list:
            for cond_val in cond_val_list:
                combinations.append({"cond_val": cond_val, "cond_val_code": str(num)})
        return combinations

    @staticmethod
    def get_rc_combinations(conditions, num_list, cond_val_list):
        target_rc_combinations = []
        for condition in conditions:
            combinations = UbrRebateOperations.generate_val_code_combinations(num_list, cond_val_list)
            for combination in combinations:
                target_rc = {"cond_code": condition, "cond_val": combination["cond_val"],
                             "cond_val_code": combination["cond_val_code"]}
                target_rc_combinations.append(target_rc)
        return target_rc_combinations

    @staticmethod
    def conditions_contains_combination(conditions, rc_combination):
        for condition in conditions:
            if condition["cond_code"] == rc_combination["cond_code"] \
                    and condition["cond_val"] == rc_combination["cond_val"] \
                    and condition["cond_val_code"] == rc_combination["cond_val_code"]:
                return True
        return False

    @staticmethod
    def get_rc_available(conditions, rc_combinations):
        target_conditions = []
        for rc_combination in rc_combinations:
            if not UbrRebateOperations.conditions_contains_combination(conditions, rc_combination):
                target_conditions.append(rc_combination)
        return target_conditions

    @staticmethod
    def normalize_rebate(rebate):
        if "rebate" in rebate:
            if rebate["rebate"] == "":
                rebate["rebate"] = "0.000000"
            if "%" in rebate["rebate"]:
                rebate["rebate"] = rebate["rebate"].replace("%", "00")
        if rebate["pp_eligible"] == "":
            rebate["pp_eligible"] = None
        if rebate["tier_basis"] == "":
            rebate["tier_basis"] = None
        if "start_date" in rebate:
            if "-" in rebate["start_date"]:
                rebate["start_date"] = datetime.strptime(rebate["start_date"], '%Y-%m-%d').date().strftime('%m/%d/%Y')
            if "/" in rebate["start_date"]:
                rebate["start_date"] = datetime.strptime(rebate["start_date"], '%m/%d/%Y').date().strftime('%m/%d/%Y')
        if "end_date" in rebate:
            if "-" in rebate["end_date"]:
                rebate["end_date"] = datetime.strptime(rebate["end_date"], '%Y-%m-%d').date().strftime('%m/%d/%Y')
            if "/" in rebate["end_date"]:
                rebate["end_date"] = datetime.strptime(rebate["end_date"], '%m/%d/%Y').date().strftime('%m/%d/%Y')
        return rebate

    @staticmethod
    def get_dates_for_rebates_with_same_type_and_data_type(rebates):
        rebates_dates = []
        for rebate_1, rebate_2 in itertools.combinations(rebates, 2):
            rebate1 = {"data_type": rebate_1["data_type"], "type": rebate_1["type"]}
            rebate2 = {"data_type": rebate_2["data_type"], "type": rebate_2["type"]}
            if generics.compare_dicts(rebate1, rebate2) is True:
                rebate1 = {"start_date": rebate_1["start_date"], "end_date": rebate_1["end_date"]}
                rebate2 = {"start_date": rebate_2["start_date"], "end_date": rebate_2["end_date"]}
                rebates_dates.append(rebate1)
                rebates_dates.append(rebate2)
        return rebates_dates

    @staticmethod
    def normalize_rebate_to_clone(rebate):
        if "name" in rebate:
            rebate = generics.remove_dict_key(rebate, "name")
        return rebate

    @staticmethod
    def parse_rebate_date(rebate):
        rebate_date = {}
        if "date" in rebate["start_date"]:
            start_date = rebate["start_date"]["date"]
            rebate_date["start_date"] = dates.format_sparc_date(start_date)
        if "date" in rebate["end_date"]:
            end_date = rebate["end_date"]["date"]
            rebate_date["end_date"] = dates.format_sparc_date(end_date)
        return rebate_date

    @staticmethod
    def get_current_rebate_dates(rebates_data):
        rebate_dates = []
        for rebate in rebates_data:
            rebate_date = UbrRebateOperations.parse_rebate_date(rebate)
            rebate_dates.append(rebate_date)
        return rebate_dates

    @staticmethod
    def get_available_contract_with_rebates_by_dates(contract_rebates):
        contract_to_exclude = []
        for contract_rebate in contract_rebates:
            for rebate in contract_rebate["rebates"]:
                rebate_dates = UbrRebateOperations.parse_rebate_date(rebate)
                if contract_rebate["contract"]["start_date"] == rebate_dates["start_date"] \
                        and contract_rebate["contract"]["end_date"] == rebate_dates["end_date"]:
                    contract_to_exclude.append(contract_rebate)
        for contract_rebate in contract_rebates:
            if contract_rebate in contract_to_exclude:
                contract_rebates.remove(contract_rebate)
        return contract_rebates

    @staticmethod
    def validate_duplicate_data_in_rebates(rebate_to_clone, rebates_data):
        rebates_to_validate_dates = []
        for rebate in rebates_data:
            if rebate["type"] in rebate_to_clone["type"] and rebate["data_type"] in rebate_to_clone["data_type"]:
                if rebate["name"] in rebate_to_clone["name"] or rebate["products"] in rebate_to_clone["products"]:
                    rebates_to_validate_dates.append(rebate)
        return rebates_to_validate_dates

    @staticmethod
    def api_rebate_payload(rebate_type,
                           contract_id,
                           numerator_id,
                           denominator_id,
                           start_date,
                           end_date,
                           data_type="PHARMACY",
                           has_overrides=False):
        rebate_name = f"{rebate_type} - {str(random.randint(1, 999))} - {datetime.now().strftime('%Y-%m-%d')}"
        sd = datetime.strptime(start_date, '%m/%d/%Y')
        ed = datetime.strptime(end_date, '%m/%d/%Y')
        payload = {
            "contract_id": str(contract_id),
            "type": rebate_type,
            "data_type": data_type,
            "invoice_freq": random.choice(["Monthly", "Quarterly"]),
            "name": rebate_name,
            "price_basis": "WAC",
            "price_date": random.choice(["DATE OF SERVICE", "BEGIN OF PERIOD", "MID-POINT OF PERIOD", "END OF PERIOD"]),
            "uom": "UNIT",
            "start_date": {
                "date": {
                    "year": sd.year,
                    "month": sd.month,
                    "day": sd.day
                }
            },
            "end_date": {
                "date": {
                    "year": ed.year,
                    "month": ed.month,
                    "day": ed.day
                }
            },
            "pp_eligible": None,
            "bfsf": None,
            "has_overrides": has_overrides,
        }
        if rebate_type == MARKET_SHARE:
            payload["condition_required"] = random.choice(["Y", "N"])
            payload["price_method"] = "% OFF"
            payload["tier_basis"] = "% OF QUANTITY"
            payload["aggregate_by_plan"] = random.choice([True, False])
            payload["aggregate_products"] = random.choice([True, False])
            payload["evaluate_only"] = random.choice([True, False])
            payload["numerator_group_id"] = str(numerator_id)
            payload["denominator_group_id"] = str(denominator_id)
        else:
            payload["condition_required"] = "N"
            payload["price_method"] = random.choice(["% OFF", "FIXED PRICE", "FIXED AMOUNT"])
            payload["rebate"] = str(round(random.uniform(0.1, 10), 1))
        return payload

    @staticmethod
    def filter_rebates(
            rebates,
            rebate_id=None,
            rebate_name=None,
            rebate_type=None,
            contract_id=None,
            data_type=None, ):
        filters = []
        if rebate_id:
            filters.append(lambda r: rebate_id == r["id"])
        if rebate_name:
            filters.append(lambda r: rebate_name in r["name"])
        if rebate_type:
            filters.append(lambda r: rebate_type == r["type"])
        if contract_id:
            filters.append(lambda r: contract_id == r["contract_id"])
        if data_type:
            filters.append(lambda r: data_type in r["data_type"])
        try:
            return list(filter(lambda p: all(f(p) for f in filters), rebates))
        except StopIteration:
            return None


class UbrCustomersOperations:

    @staticmethod
    def get_available_customers(customers):
        eligible_t_partners = []
        for customer in customers:
            if customer["customer_name_ext"] is not None:
                eligible_t_partners.append(customer)
        return eligible_t_partners

    @staticmethod
    def get_list_of_eligible_customers(customers):
        eligible_customers = []
        eligible_t_partners = UbrCustomersOperations.get_available_customers(customers)
        for eligible_tp in eligible_t_partners:
            if eligible_tp["customer_name"] not in eligible_customers:
                eligible_customers.append(eligible_tp["customer_name"])
        return eligible_customers


class UbrRebateReconOperations:

    @staticmethod
    def validate_row_type_column_in_tabs(file_name):
        count = 0
        excel_tabs = {}
        columns_in_sheets = files.get_columns_from_excel(file_name)
        for key, value in columns_in_sheets.items():
            if key in VALIDATE_ROW_TYPE:
                for column in value:
                    if "Row Type" in column:
                        excel_tabs[key] = value
                        count += 1
        if count == len(VALIDATE_ROW_TYPE):
            return excel_tabs
        return None

    @staticmethod
    def format_values(value):
        if "$" in value:
            value = value.replace("$", "")
        if "," in value:
            value = value.replace(",", "")
        return value

    @staticmethod
    def get_rebate_total_from_a_dict(data, target_value):
        rebate_total = ""
        for key, value in data.items():
            if isinstance(value, dict):
                for d_key, d_value in value.items():
                    if target_value in d_key:
                        rebate_total = str(d_value)
        return rebate_total

    @staticmethod
    def check_rebate_totals_on_cover_sheet(file_name, ws_name, column_name, rebate_summary):
        target_value = column_name + " Total"
        rebate = files.get_values_in_worksheet_by_column(file_name, ws_name, column_name)
        if rebate:
            total_data = UbrRebateReconOperations.get_rebate_total_from_a_dict(rebate, target_value)
            if total_data in rebate_summary:
                return True
        return False

    @staticmethod
    def check_rebate_totals_on_payment_summary(file_name, ws_name, rebate_summary, target_columns):
        rebate_total = target_columns[0] + " Total"
        calc_rebate_total = files.get_values_in_worksheet_by_column(file_name, ws_name, target_columns[1])
        if calc_rebate_total:
            calculated_rebate = calc_rebate_total["Payment Summary"][target_columns[1]]
            rebate = files.get_values_in_worksheet_by_column(file_name, ws_name, target_columns[0], calculated_rebate)
            if rebate:
                total_ms_data = UbrRebateReconOperations.get_rebate_total_from_a_dict(rebate, rebate_total)
                if total_ms_data in rebate_summary:
                    return True
        return False

    @staticmethod
    def compare_rebate_totals(file_name, rebate_summary, ws_name, column_name, totals_row=None):
        rebate_total = column_name + " Total"
        rebate = files.get_values_in_worksheet_by_column(file_name, ws_name, column_name, None, totals_row)
        if rebate:
            total_data = UbrRebateReconOperations.get_rebate_total_from_a_dict(rebate, rebate_total)
            if total_data in rebate_summary:
                return True
        return False

    @staticmethod
    def validate_cover_sheet(file_name, rebate_summary, ws_name, column_name, target_columns=None):
        if column_name == "Market Share":
            response = files.check_column_in_sheet(file_name, ws_name, column_name, target_columns)
            if response:
                market_share_total = UbrRebateReconOperations.check_rebate_totals_on_cover_sheet(
                    file_name, ws_name, column_name, rebate_summary)
                if market_share_total:
                    return True
        else:
            rebate_total = UbrRebateReconOperations.check_rebate_totals_on_cover_sheet(file_name, ws_name, column_name,
                                                                                       rebate_summary)
            if rebate_total:
                return True
        return False

    @staticmethod
    def validate_payment_summary(file_name, rebate_summary, ws_name, target_columns):
        if "Market Share" in target_columns:
            columns_validation = []
            for t_column in target_columns:
                response = files.check_column_in_sheet(file_name, ws_name, t_column)
                columns_validation.append(str(response))
            if "Not found" not in columns_validation:
                market_share_total = UbrRebateReconOperations.check_rebate_totals_on_payment_summary(
                    file_name, ws_name, rebate_summary, target_columns)
                if market_share_total:
                    return True
        else:
            rebate_total = UbrRebateReconOperations.check_rebate_totals_on_payment_summary(
                file_name, ws_name, rebate_summary, target_columns)
            if rebate_total:
                return True
        return False

    @staticmethod
    def validate_rebate_amount_field(file_name, rebate_summary, ws_name, column_name, totals_row=None):
        col_count = []
        if "Market Share" in column_name:
            response = ""
            if ws_name == "Explanation of Payment Summary":
                columns_to_validate = EP_SUMMARY_COLUMNS
            elif ws_name == "Explanation of Payment Details":
                columns_to_validate = EP_DETAILS_COLUMNS
            else:
                columns_to_validate = [column_name]
            for column in columns_to_validate:
                response = files.check_column_in_sheet(file_name, ws_name, column)
                col_count.append("is_column: " + str(response))
                if not response:
                    if "Not found" not in response and len(col_count) == len(columns_to_validate):
                        response = True
            if response:
                market_share_total = UbrRebateReconOperations.compare_rebate_totals(
                    file_name, rebate_summary, ws_name, column_name)
                if market_share_total:
                    return True
        else:
            if "Additional" in column_name and ws_name == "Explanation of Payment Details":
                column_name = "Additional Rebate Amt"
            rebate_total = UbrRebateReconOperations.compare_rebate_totals(
                file_name, rebate_summary, ws_name, column_name, totals_row)
            if rebate_total:
                return True
        return False

    @staticmethod
    def validate_calculations_totals_of_market_share(file_name, summary_data):
        summary_data = UbrRebateReconOperations.format_values(summary_data)
        total_ms_summary = UbrRebateReconOperations.get_rebate_total_from_a_dict(summary_data, "market_share")
        cover_sheet = UbrRebateReconOperations.validate_cover_sheet(file_name, total_ms_summary, "Cover Sheet",
                                                                    "Market Share", "Total Payment")
        payment_summary_columns = ["Market Share", "Calculated Market Share"]
        payment_summary = UbrRebateReconOperations.validate_payment_summary(file_name, total_ms_summary,
                                                                            "Payment Summary",
                                                                            payment_summary_columns)
        summary_by_plan = UbrRebateReconOperations.validate_rebate_amount_field(file_name, total_ms_summary,
                                                                                "Summary by Plan", "Market Share Amt")
        summary_by_product = UbrRebateReconOperations.validate_rebate_amount_field(file_name, total_ms_summary,
                                                                                   "Summary by Product",
                                                                                   "Market Share Amt")
        exp_payment_summary = UbrRebateReconOperations.validate_rebate_amount_field(file_name, total_ms_summary,
                                                                                    "Explanation of Payment Summary",
                                                                                    "Market Share Amt")
        exp_payment_details = UbrRebateReconOperations.validate_rebate_amount_field(file_name, total_ms_summary,
                                                                                    "Explanation of Payment Details",
                                                                                    "Market Share Amt")
        if cover_sheet and payment_summary and summary_by_plan and summary_by_product and exp_payment_summary \
                and exp_payment_details:
            return True

    @staticmethod
    def validate_final_to_pay_amount(summary_data):
        summary_data = UbrRebateReconOperations.format_values(summary_data)
        if summary_data["totals"]["total_dollars"] == summary_data["final_to_pay_amount"]:
            return True

    @staticmethod
    def simplify_additional_rebate_totals(summary_data):
        addl_total = float(summary_data["totals"]["addl_rebate"]) + float(summary_data["totals"]["addl_fee"])
        summary_data["totals"]["addl_total"] = str(addl_total)
        return summary_data

    @staticmethod
    def validate_cover_sheet_totals(file_name, summary_data):
        column_name = ""
        count_true = 0
        for rebate in REBATES_REPORT:
            if rebate == "base_rebate":
                column_name = "Base Rebate"
            elif rebate == "addl_total":
                column_name = "Additional Rebate/Fee"
            elif rebate == "admin_fee":
                column_name = "Admin Fee"
            elif rebate == "price_protection":
                column_name = "Price Protection"
            elif rebate == "data_fee":
                column_name = "Data Fee"
            response = UbrRebateReconOperations.validate_cover_sheet(
                file_name, summary_data["totals"][rebate], "Cover Sheet", column_name)
            if response:
                count_true += 1
            if 3 <= count_true <= 5:
                return True

    @staticmethod
    def validate_payment_summary_totals(file_name, summary_data):
        rebate_columns = ""
        count_true = 0
        for rebate in REBATES_REPORT:
            if rebate == "base_rebate":
                rebate_columns = ["Base Rebate", "Calculated Rebate"]
            elif rebate == "addl_total":
                rebate_columns = ["Addl Reb/Fee", "Calculated Addl Reb/Fee"]
            elif rebate == "admin_fee":
                rebate_columns = ["Admin Fee", "Calculated Admin Fee"]
            elif rebate == "price_protection":
                rebate_columns = ["Price Protection", "Calculated PP"]
            elif rebate == "data_fee":
                rebate_columns = ["Data Fee", "Calculated Data Fee"]
            response = UbrRebateReconOperations.validate_payment_summary(
                file_name, summary_data["totals"][rebate], "Payment Summary", rebate_columns)
            if response:
                count_true += 1
            if 3 <= count_true <= 5:
                return True

    @staticmethod
    def validate_rebate_amount_totals(file_name, summary_data, ws_name):
        column_name = ""
        count_true = 0
        totals_row = 0
        for rebate in REBATES_REPORT:
            if rebate == "base_rebate":
                column_name = "Rebate Amt"
            elif rebate == "addl_total":
                column_name = "Additional Rebate/Fee Amt"
            elif rebate == "admin_fee":
                column_name = "Admin Amt"
            elif rebate == "price_protection":
                column_name = "PP Amt"
            elif rebate == "data_fee":
                column_name = "Data Fee Amt"
            if totals_row == 0:
                data = files.get_values_in_worksheet_by_column(file_name, ws_name, column_name)
                if data[ws_name] is not None:
                    totals_row = data[ws_name]["row_totals"]
            response = UbrRebateReconOperations.validate_rebate_amount_field(
                file_name, summary_data["totals"][rebate], ws_name, column_name, totals_row)
            if response:
                count_true += 1
            if 3 <= count_true <= 5:
                return True

    @staticmethod
    def validate_calculation_totals(file_name, summary_data):
        summary_data = UbrRebateReconOperations.format_values(summary_data)
        summary_data = UbrRebateReconOperations.simplify_additional_rebate_totals(summary_data)
        cover_totals = UbrRebateReconOperations.validate_cover_sheet_totals(file_name, summary_data)
        pay_sum_totals = UbrRebateReconOperations.validate_payment_summary_totals(file_name, summary_data)
        sum_plan_totals = UbrRebateReconOperations.validate_rebate_amount_totals(file_name, summary_data,
                                                                                 "Summary by Plan")
        sum_prod_totals = UbrRebateReconOperations.validate_rebate_amount_totals(file_name, summary_data,
                                                                                 "Summary by Product")
        exp_pay_sum_totals = UbrRebateReconOperations.validate_rebate_amount_totals(file_name, summary_data,
                                                                                    "Explanation of Payment Summary")
        exp_pay_det_totals = UbrRebateReconOperations.validate_rebate_amount_totals(file_name, summary_data,
                                                                                    "Explanation of Payment Details")
        if cover_totals and pay_sum_totals and sum_plan_totals and sum_prod_totals and exp_pay_sum_totals \
                and exp_pay_det_totals:
            return True

    @staticmethod
    def validate_market_share_calculations_with_calc(summary_data, file_path):
        summary_data = UbrRebateReconOperations.format_values(summary_data)
        file_data = files.read_headers_from_csv_file("./" + file_path)
        column_values = files.get_values_from_column(file_data, "Market Share Rebate Amount")
        market_share = files.sum_values_list(column_values)
        total_ms_data = UbrRebateReconOperations.get_rebate_total_from_a_dict(summary_data, "market_share")
        if math.isclose(float(total_ms_data), market_share, abs_tol=10):
            return True
        return False
