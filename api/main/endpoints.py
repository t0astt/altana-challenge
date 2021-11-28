from typing import Optional
from urllib.parse import unquote

from flask import request, jsonify

from . import main
from ..models import Company


@main.route("/operators", methods=["GET"])
def operators():
    """
    Route to get operators based on a company.
    :return: JSON response containing all operators for a specified company, if any.
    """
    company_name = _extract_query_param(query_string=request.query_string,
                                        arg_key="company")

    # If no company name was able to be extracted, then the request is bad. Return a 400.
    if not company_name:
        response = jsonify({
            "error": "Bad request"
        })
        response.status_code = 400

        return response

    # Query the DB for the operators.
    all_operators: [Company] = Company.query.filter_by(nm_fantasia=company_name).with_entities(Company.nm_socio).all()
    return jsonify(
        {
            "operators": list(set(o.nm_socio for o in all_operators))  # Cast to set, then list, to de-dupe
        }
    )


@main.route("/companies", methods=["GET"])
def companies():
    """
    Route to get company based on an operator.
    :return: JSON response containing all companies for a specified operator, if any.
    """
    operator_name = _extract_query_param(query_string=request.query_string,
                                         arg_key="operator")

    # If no company name was able to be extracted, then the request is bad. Return a 400.
    if not operator_name:
        response = jsonify({
            "error": "Bad request"
        })
        response.status_code = 400

        return response

    # Query the DB for the companies.
    all_companies: [Company] = Company.query.filter_by(nm_socio=operator_name).with_entities(Company.nm_fantasia).all()
    return jsonify(
        {
            "companies": list(set(o.nm_fantasia for o in all_companies)) # Cast to set, then list, to de-dupe
        }
    )


@main.route("/companies/connected", methods=["GET"])
def connected_companies():
    """
    Route to get companies connected to a company by shared operators.
    :return: JSON response containing all companies connected, if any.
    """
    company_name = _extract_query_param(query_string=request.query_string,
                                        arg_key="company")

    # If no company name was able to be extracted, then the request is bad. Return a 400.
    if not company_name:
        response = jsonify({
            "error": "Bad request"
        })
        response.status_code = 400

        return response

    # First, query the DB for operators associated with the specified company.
    all_operators: [Company] = Company.query.filter_by(nm_fantasia=company_name).with_entities(Company.nm_socio).all()

    # Next, for each operator in the de-duped operators, query for associated companies.
    connected_companies_: [Company] = []
    for operator in set(all_operators):
        connected_companies_.extend(
            Company.query.filter_by(nm_socio=operator.nm_socio).with_entities(Company.nm_fantasia).all())

    return jsonify(
        {
            "companies": list(set(c.nm_fantasia for c in connected_companies_)) # Cast to set, then list, to de-dupe
        }
    )


def _extract_query_param(query_string: bytes, arg_key: str) -> Optional[str]:
    """
    Extracts query parameters from a raw query string.
    Unquotes and allows for inclusion of ampersands within query values.
    :param query_string: Raw query string to process.
    :param arg_key: Key to get value for.
    :return: Value if present and query string is properly formatted, None otherwise.
    """
    raw_query: str = query_string.decode()  # Decode the querystring from bytes to string.
    query_components = raw_query.split(f"{arg_key}=")  # Split on the desired querystring key.

    # If the length of the query components is greater than two, then the querystring provided is invalid.
    # Return None in this instance.
    if len(query_components) != 2:
        return None

    # Lastly, unquote the value and return it.
    query_value = unquote(query_components[1])

    return query_value
