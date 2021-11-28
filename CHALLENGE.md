# Altana AI Challenge

## Overview

This project is intended to replicate the type of work a Software Engineer will undertake at Altana.  Altana's Atlas is a knowledge graph of companies connected to each other via shared owners and operators. You’ll be creating a similar project to import this CSV file of Brazilian companies (~400MB compressed) into a data store, and create an API to query it.

### About the Data

* **nr_cnpj**: numeric(ish) (should have leading zeros in some cases, handle as you think appropriate): Company’s registration ID
* **nm_fantasia**: string: Company’s name
* **sg_uf**: string: State where the company is located
* **in_cpf_cnpj**: numeric: Indicates if the business partner is a Company (1) or a Person (2)
* **nr_cpf_cpnj_socio**:  numeric(ish). Business partner registration ID (only for Companies, null when refers to individuals as has been redacted for privacy reasons)
* **cd_qualificacao_socio**: numeric: Code of the business partner role
* **ds_qualificacao_socio**: string: Description of the business partner role
* **nm_socio**: string: operator / administrator name
  * Given that the nr_cpf_cpnj_socio is often null, please use this string as the unique key for this operator/administrator of the company.
  * The operator/administrator can be either a person or (somewhat more rarely) a company itself.

Your deliverable should be a git repository (zipped and attached) with the following requirements:

### Requirements

* Clean code, preferably in Python but choose your strongest language if not comfortable with Python.  
* It doesn't need to be performant, but it should be readable and correct.  Keep it simple.
* A command line tool for importing/transforming data from the CSV file into a data store of your choosing.
* A service that runs an API to query the datastore for the following:
  * All operators associated with a given company
  * All companies associated with a given operator
  * All companies connected to a given company via shared operators
* A README describing:
  * How to build and run your project, e.g. installing requirements and prerequisites, importing data, running the API service, etc.  
  * Try to steer clear of anything too esoteric, but you're probably safe sticking to popular languages like Python, Java, Javascript, or Go, and data stores with little or no setup needed.
  * Architecture of the system - what concerns did you have about the data and the project requirements, how does your design solve them, and why choose certain frameworks/tools?  Simplicity is key.  If you feel strongly that something complex is the right choice, document why.