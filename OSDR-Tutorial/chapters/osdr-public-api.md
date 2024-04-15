---
description: >-
  NASA OSDR provides a RESTful Application Programming Interface (API) to its
  full-text search, data file retrieval, and metadata retrieval capabilities.
---

# OSDR Public API

{% embed url="https://api.nasa.gov/" %}

The API provides a choice of standard web output formats, either JavaScript Object Notation (JSON) or Hyper Text Markup Language (HTML), of query results. The Data File API returns metadata on data files associated with dataset(s), including the location of these files for download via https. The Metadata API returns entire sets of metadata for input study dataset accession numbers. The Search API can be used to search dataset metadata by keywords and/or metadata. It can also be used to provide search of three other omics databases: the National Institutes of Health (NIH) / National Center for Biotechnology Information's (NCBI) Gene Expression Omnibus (GEO); the European Bioinformatics Institute's (EBI) Proteomics Identification (PRIDE); the Argonne National Laboratory's (ANL) Metagenomics Rapid Annotations using Subsystems Technology (MG-RAST).

In addition to study datasets, NASA OSDR also hosts metadata for 7 other data types: experiments, payloads, subjects, biospecimens, missions, vehicles, and hardware. The API for these data types is listed separately and uniform throughout, to make for easy metadata exploration.

**Resources:** For more information on making API requests with python, try this [python API tutorial](https://www.dataquest.io/blog/python-api-tutorial/).

Alternatively for more advanced information on the OSDR Public API visit [https://api.nasa.gov/](https://api.nasa.gov/).

### &#x20;<a href="#id-22paw416qpf8" id="id-22paw416qpf8"></a>

### [OSDR API](https://genelab.nasa.gov/genelabAPIs)

[Find out more about the OSDR Automatic programmatic interaction (API) here.](https://genelab.nasa.gov/genelabAPIs)

{% embed url="https://genelab.nasa.gov/genelabAPIs" %}

### **Making API Requests with Python**

Python to make basic API requests. This will be crucial for anyone working with bioinformatics data, as many resources offer data access through APIs.

### **The requests library**

The go-to library for making API requests in Python is called requests. It provides a simple and elegant way to interact with web services. The first step is to install the library using pip, the Python package manager. Open your terminal and type the following command:

\`` `` bash `

`pip install requests`

` ``` `

`Once you've installed requests, you can import it into your Python code. Here's an example of a basic API request:`

` ``` python `

`import requests`

`# Replace API_ENDPOINT_HERE with the actual API endpoint URL`

`response = requests.get("API_ENDPOINT_HERE").json()`

`# Process the data in the response object`

` ``` `

In this code, we first import the requests library. Then, we use the requests.get() function to send a GET request to the specified API endpoint URL. The .json() method is used to parse the JSON response from the API into a Python dictionary that we can easily work with in our code.

### **Example: Accessing NASA data**

Let's look at a concrete example. Suppose we want to retrieve some data from NASA's Open Science Data Repository (OSDR). Here's how we can use the requests library to fetch a specific file:



` ```Python `

`import requests`

`# API endpoint URL for a specific file in OSDR`

`url = "https://osdr.nasa.gov/osdr/data/osd/files/87"`

`response = requests.get(url).json()`

`# Now you have the data from the file in the response object`

` ``` `

By replacing API\_ENDPOINT\_HERE with the actual URL of the API endpoint you want to access, you can use this code template to retrieve data from a variety of web services.



### Summary of Study Metadata API <a href="#oa543j8meou9" id="oa543j8meou9"></a>

**Syntax:** _“a set of rules for or an analysis of the syntax of a language.”_

`https://osdr.nasa.gov/osdr/data/osd/meta/{OSD_STUDY_ID}`

| Parameters       | Data Type | Notes                         | Values       | Required |
| ---------------- | --------- | ----------------------------- | ------------ | -------- |
| {OSD\_STUDY\_ID} | Integer   | Single study accession number | Example: 137 | Yes      |

Single Study Metadata Request:

**Example:** [https://osdr.nasa.gov/osdr/data/osd/meta/137](https://osdr.nasa.gov/osdr/data/osd/meta/137)

**Returns:** JSON-formatted response

**Response:** This example provides all metadata for OSD sample # 137 revealing the datatypes that are linked to this study accession #.

### **Explanation of the OSDR Study Metadata API** <a href="#xlmaonc22d9n" id="xlmaonc22d9n"></a>

The OSDR Study Metadata API provides access to detailed information about specific studies stored in NASA's Open Science Data Repository (OSDR), making it a valuable tool for bioinformatics researchers.

#### Understanding Syntax: The Rules of the Game

Before diving in, let's clarify the term "syntax." In computer science, syntax refers to the specific rules that define how elements of a language are arranged to create a well-formed instruction. Here, the syntax defines how we structure the API request to target a particular study.

#### The API Endpoint: Your Gateway to Study Data

The OSDR Study Metadata API uses the following endpoint URL structure:

### https://osdr.nasa.gov/osdr/data/osd/meta/{OSD\_STUDY\_ID} <a href="#y1ghpc1dn4ak" id="y1ghpc1dn4ak"></a>

This endpoint acts like a doorway to a specific study's metadata.&#x20;

The key element here is the {OSD\_STUDY\_ID} placeholder.

#### Parameters: The Keys that Unlock Information

**The API uses a single parameter:** {OSD\_STUDY\_ID} (Integer, Required): This represents the unique accession number assigned to a specific study within OSDR. Think of it as the study's identification code.

#### Putting it all Together: A Real-World Example

Let's say you're interested in exploring the metadata for a particular OSDR study with the accession number 37. Here's how you would construct the API request URL:

### https://osdr.nasa.gov/osdr/data/osd/meta/37 <a href="#dcke2d2hpnil" id="dcke2d2hpnil"></a>

By using this URL through the API, you'll receive a response containing all the metadata associated with study 137. This metadata serves as a treasure trove of information, revealing details about the study design, samples involved, data types collected, and much more. [This Google CoLab Notebook ](https://github.com/dr-richard-barker/Space\_Biology\_and\_AstroBotany.io/blob/main/OSDR\_API\_demo\_GLDS-37.ipynb)demonstrates what this API looks like and is available for users to edit and evolve.

{% @github-files/github-code-block url="https://github.com/dr-richard-barker/Space_Biology_Education.io/blob/main/OSDR_API_demo_GLDS-37.ipynb" %}

#### The Power of the Response: Unveiling Study Secrets

The response from the API will be delivered in JSON format, a common and easily readable format for data exchange. This JSON response will essentially be a digital document containing all the metadata associated with the requested study. Imagine it as a detailed report outlining the study's purpose, methods, and collected data.

By parsing through this response using Python or other programming languages, you can extract valuable insights into the study and its associated data. This information can be crucial for understanding the context and design of the research, ultimately enabling more informed analysis and interpretation of the data itself.

#### Remember:

Replace {OSD\_STUDY\_ID} with the actual accession number of the study you're interested in.

This API retrieves metadata, not the actual data files themselves. Use the Data File API (covered elsewhere) to download the data associated with a study.

Always refer to the official OSDR documentation for the latest information on the API and its functionalities.

### Summary of Study Data File API <a href="#tz0q8lmeplzy" id="tz0q8lmeplzy"></a>

Syntax 1:

https://osdr.nasa.gov/osdr/data/osd/files/{**OSD\_STUDY\_IDs**}/?page={CURRENT\_PAGE\_NUMBER}\&size={RESULTS\_PER\_PAGE}?all\_files={ALL\_FILES}

| Parameters              | Data Type          | Notes                                                                                                                                                                              | Values                  | Required |
| ----------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- | -------- |
| {OSD\_STUDY\_IDs}       | Integer or Decimal | Comma separated list with mixture of single OSD accession numbers and ranges. Use single decimal numbers to indicate a specific study version (Ex: 4.1 would be OSD-4, version 1). | ex. 87-95,137,153.2     | Yes      |
| {CURRENT\_PAGE\_NUMBER} | Integer            | Current page number in pagination                                                                                                                                                  | Starts from 0           | No       |
| {RESULTS\_PER\_PAGE}    | Integer            | Number of results returned per page in pagination                                                                                                                                  | Max 25 results per page | No       |
| {ALL\_FILES}            | Boolean            | Include hidden files. true to include invisible files; false to exclude. Default value is false.                                                                                   | true or false           | No       |

#### Example requests: <a href="#rxafhhfdshrl" id="rxafhhfdshrl"></a>

* Single study request using study accession number

**Example:** [https://osdr.nasa.gov/osdr/data/osd/files/87](https://osdr.nasa.gov/osdr/data/osd/files/87)

* Multiple studies request using combination of range and comma-separated list

**Example:** [https://osdr.nasa.gov/osdr/data/osd/files/137,87-95,13,20-50](https://osdr.nasa.gov/osdr/data/osd/files/137,87-95,13,20-50)

**Returns:** The JSON-formatted response includes the study\_files element, and the remote\_url attribute will obtained from that element. Which can be used to obtain the specific download URL for the file by prefacing with the OSDR data server address, [https://osdr.nasa.gov](https://osdr.nasa.gov/) .

In the example query/response below, the first study file for OSD-87 (version 1) study in the response below can be downloaded from [https://osdr.nasa.gov/geode-py/ws/studies/OSD-87/download?source=datamanager\&file=GLDS-87\_metadata\_Zanello\_STS135-ISA.zip](https://osdr.nasa.gov/geode-py/ws/studies/OSD-87/download?source=datamanager\&file=GLDS-87\_metadata\_Zanello\_STS135-ISA.zip)



### **Explanation of the OSDR Study Data File API** <a href="#ivh1s0qlv61f" id="ivh1s0qlv61f"></a>

Alright class, buckle up! Today we're diving into the OSDR Study Data File API, the key to unlocking the actual data associated with studies in NASA's Open Science Data Repository. This API empowers you to download the data files used in a specific study or a collection of studies.

#### **Understanding the API's Language: Syntax Breakdown**

The API uses a specific syntax to define your request. Here's how it works:

**Base URL:** https://osdr.nasa.gov/osdr/data/osd/files/

This is the foundation of your API request URL.

#### **Parameters: The Keys to Specificity**

The API offers several parameters to fine-tune your request:

* **{OSD\_STUDY\_IDs} (Integer or Decimal, Required):** This is the star of the show! It's a comma-separated list containing the accession numbers of the studies you want to retrieve data files from. You can even include ranges of accession numbers for efficiency.
* {CURRENT\_PAGE\_NUMBER} (Integer, **Optional**): If the number of data files associated with a study is extensive, the API will return them in pages. This parameter allows you to specify the specific page of results you want to retrieve. Pagination starts from page 0, so the first page would be 0.
* {RESULTS\_PER\_PAGE} (Integer, **Optional**): This parameter lets you control how many data files are returned per page. The maximum allowed value is 25, so keep that in mind when dealing with large datasets.
* {ALL\_FILES} (Boolean, **Optional**): This parameter allows you to include hidden files in your search results. By default, only visible files are returned. Set it to true to include hidden files and false to exclude them.

#### **Constructing Your Request URL: Examples in Action** <a href="#id-19gl8lt4uvzb" id="id-19gl8lt4uvzb"></a>

Let's explore some real-world examples:

1. **Single Study Request:**

Want to download data files for the study with accession number 87? Use this URL:

#### https://osdr.nasa.gov/osdr/data/osd/files/87 <a href="#w1xkxlkruyfu" id="w1xkxlkruyfu"></a>

1. **Multiple Studies Request:**

Need data from multiple studies? This URL grabs data from studies 137, 87-95 (accession numbers 87 to 95), study 13, and studies 20 to 50:

#### https://osdr.nasa.gov/osdr/data/osd/files/137,87-95,13,20-50 <a href="#wr2nxymxrizr" id="wr2nxymxrizr"></a>

**Decoding the Response: Your Downloading Roadmap**

The response from the API will be delivered in JSON format. Within the response, look for the study\_files element. This element will contain information about the data files associated with the requested studies, including a crucial attribute called remote\_url.

The remote\_url provides the download link for the specific data file. To get the complete download URL, simply prepend the OSDR data server address (https://osdr.nasa.gov) to the remote\_url provided in the response.

For example, if the remote\_url for the first data file in study OSD-87 (version 1) is geode-py/ws/studies/OSD-87/download?source=datamanager\&file=GLDS-87\_metadata\_Zanello\_STS135-ISA.zip, the complete download URL would be:

https://osdr.nasa.gov/geode-py/ws/studies/OSD-87/download?source=datamanager\&file=GLDS-87\_metadata\_Zanello\_STS135-ISA.zip

**Remember:**

* This API retrieves data file information, not the actual data files themselves. Use the provided download URL to access the data.
* Pagination is your friend for large datasets. Play around with the {CURRENT\_PAGE\_NUMBER} and {RESULTS\_PER\_PAGE} parameters to navigate through extensive data collections.
* Always refer to the official OSDR documentation for the latest information on the API and its functionalities.

#### &#x20;<a href="#fkzsxq1uj01p" id="fkzsxq1uj01p"></a>

#### Study Dataset Search API <a href="#fkzsxq1uj01p" id="fkzsxq1uj01p"></a>

Syntax 1 (returns JSON response)

https://osdr.nasa.gov/osdr/data/search?\<PARAMETER-LIST>

| parameters | definition                  | values                                                                                                                                                                                            |
| ---------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| term       | search keyword              | string                                                                                                                                                                                            |
| from       | starting page               | integer (single value)                                                                                                                                                                            |
| size       | search result display count | integer (single value)                                                                                                                                                                            |
| type       | datasource                  | cgene , nih\_geo, ebi\_pride, mg\_rast (accepts multiple value separated by comma separated)                                                                                                      |
| sort       | sort field                  | string (Field Name)                                                                                                                                                                               |
| order      | sort order                  | ASC - ascending order; DESC - descending order                                                                                                                                                    |
| ffield     | filter field                | string (should always be pared with fvalue); append .raw to the end of the field to use the exact match index; see table below for possible filter field values and example filter value pairings |
| fvalue     | filter value                | string (should always be pared with ffield)                                                                                                                                                       |

#### Crafting Your Search Query: Understanding the Syntax <a href="#d30ufompv5ir" id="d30ufompv5ir"></a>

The API uses a specific syntax to understand your search criteria. Here's how it breaks down:

**Base URL:** [https://osdr.nasa.gov/osdr/data/**search**](https://osdr.nasa.gov/osdr/data/search)**?**

This is the foundation of your API request URL.

**Parameters: The Fine-Tuning Tools**

The API offers a variety of parameters to tailor your search:

* **term (String):** This is your search keyword. Enter the term(s) you want to use to find relevant datasets.
* **from (Integer, Optional):** If the search results are extensive, the API will return them in pages. This parameter allows you to specify the page number you want to start your search results from. The first page is numbered 0.
* **size (Integer, Optional):** This parameter controls how many datasets are displayed per page in the search results. The maximum allowed value is typically 25, so keep that in mind for large searches.
* **type (String, Optional):** This allows you to filter your search by specific data sources within OSDR. Some examples include cgene (Gene Expression Omnibus), nih\_geo (Gene Expression Omnibus by NIH), ebi\_pride (PRoteomics IDentification Experiment), and mg\_rast (Metagenomics Research Analysis Sharing Tool). You can even search across multiple sources by separating them with commas.
* **sort (String, Optional):** Want to organize your search results in a particular way? This parameter allows you to sort the results by a specific field name.
* **order (String, Optional):** This parameter refines the sorting further. Use ASC for ascending order (e.g., A to Z) or DESC for descending order (Z to A).
* **ffield (String, Required if using fvalue):** This defines the field you want to filter your search by. The OSDR documentation provides a detailed list of available filter fields. For exact matches, append .raw to the field name (e.g., title.raw).
* **fvalue (String, Required if using ffield):** This specifies the value you want to filter by. It should always be paired with the corresponding ffield.

#### Building Your Search URL: Examples in Action <a href="#eo0brdniye4v" id="eo0brdniye4v"></a>

Let's explore some real-world examples to solidify your understanding:

1. **Basic Search:**

Looking for datasets containing the term "microbiome"? Use this URL:

[https://osdr.nasa.gov/osdr/data/search?term=microbiome](https://osdr.nasa.gov/osdr/data/search?term=microbiome)

1. **Paginated Search with Filtering:**

Want to see datasets related to "RNA-seq" starting from page 2, displaying 10 results per page, and filtered by data source "nih\_geo"? This URL achieves that:

[https://osdr.nasa.gov/osdr/data/search?term=RNA-seq\&from=1\&size=10\&type=nih\_geo](https://osdr.nasa.gov/osdr/data/search?term=RNA-seq\&from=1\&size=10\&type=nih\_geo)

1. **Exact Match Filtering:**

Need datasets with the exact title "A Study of Microbial Communities in Space"? This URL leverages the .raw extension for exact matching:

[https://osdr.nasa.gov/osdr/data/search?term=\&ffield=title.raw\&fvalue=A%20Study%20of%20Microbial%20Communities%20in%20Space](https://osdr.nasa.gov/osdr/data/search?term=\&ffield=title.raw\&fvalue=A%20Study%20of%20Microbial%20Communities%20in%20Space)

**Remember:**

* This API searches for datasets, not the actual data files themselves. Use the provided information within the search results to locate the data.
* Pagination and filtering are your allies for efficient searching, especially with large datasets.
* Always refer to the official OSDR documentation for the latest list of available filter fields and for more advanced search functionalities.

#### POST and GET requests accept the URL encoded name/value pairs for submission <a href="#id-9lfixb1g42vf" id="id-9lfixb1g42vf"></a>

| **Filter Field (Case Sensitive)** | **Example Filter Value**                                                                        |
| --------------------------------- | ----------------------------------------------------------------------------------------------- |
| Accession                         | OSD-4                                                                                           |
| Acknowledgments                   | NASA JPL                                                                                        |
| Authoritative Source URL          | OSD-4                                                                                           |
| Data Source Accession             | GSE18388                                                                                        |
| Data Source Type                  | cgene                                                                                           |
| Experiment Platform               | Animal Enclosure Module                                                                         |
| Flight Program                    | Shuttle                                                                                         |
| links                             | GPL13112                                                                                        |
| Managing NASA Center              | Ames Research Center                                                                            |
| Material Type                     | thymus                                                                                          |
| organism                          | Mus musculus                                                                                    |
| Project Identifier                | NNA04CC97G                                                                                      |
| Project Link                      | https://taskbook.nasaprs.com/tbp/index.cfm?action=public\_query\_taskbook\_content\&TASKID=7191 |
| Project Title                     | Vector-Averaged Gravity                                                                         |
| Project Type                      | Spaceflight                                                                                     |
| Space Program                     | NASA                                                                                            |
| Study Assay Measurement Type      | transcription profiling                                                                         |
| Study Assay Technology Platform   | Affymetrix                                                                                      |
| Study Assay Technology Type       | DNA microarray                                                                                  |
| Study Description                 | Murine Thymus Tissue                                                                            |
| Study Factor Name                 | Spaceflight                                                                                     |
| Study Factor Type                 | Space Flight                                                                                    |
| Study Funding Agency              | NNA04CC97G                                                                                      |
| Study Identifier                  | OSD-4                                                                                           |
| Study Protocol Description        | thymus tissue                                                                                   |
| Study Protocol Name               | sample collection                                                                               |
| Study Protocol Type               | sample collection                                                                               |
| Study Public Release Date         | 1268179200                                                                                      |
| Study Publication Author List     | Gruener R                                                                                       |
| Study Publication Title           | spaceflown murine thymus tissue                                                                 |
| Study Title                       | Space-flown Murine Thymus Tissue                                                                |

**Example(s):** [https://osdr.nasa.gov/osdr/data/search?term=space\&from=0\&type=cgene,nih\_geo\_gse\&ffield=links\&fvalue=GPL16417\&ffield=Data%20Source%20Accession.raw\&fvalue=GSE82255](https://osdr.nasa.gov/osdr/data/search?term=space\&from=0\&type=cgene,nih\_geo\_gse\&ffield=links\&fvalue=GPL16417\&ffield=Data%20Source%20Accession.raw\&fvalue=GSE82255)

[https://osdr.nasa.gov/osdr/data/search?ffield=organism\&fvalue=Homo%20sapiens\&ffield=Study%20Assay%20Technology%20Type\&fvalue=RNA%20Sequencing](https://osdr.nasa.gov/osdr/data/search?ffield=organism\&fvalue=Homo%20sapiens\&ffield=Study%20Assay%20Technology%20Type\&fvalue=RNA%20Sequencing)

#### Understanding POST and GET Filter Field Options <a href="#cpl54pj0ww3a" id="cpl54pj0ww3a"></a>

The API provides a comprehensive list of filter fields that you can leverage to pinpoint datasets that meet your specific criteria. Remember, filter fields are case-sensitive, so ensure you use the exact spelling as specified in the API documentation.

Here are some noteworthy filter fields along with example filter values to illustrate their functionality:

* **Accession (OSD-4):** This field allows you to search for datasets based on their unique accession number within OSDR.
* **Acknowledgments (NASA JPL):** Want to find datasets that acknowledge a specific entity (e.g., funding agency, collaborator)? Use this field.
* **Authoritative Source URL (OSD-4):** This filter helps you identify datasets with a specific authoritative source URL.
* **Data Source Accession (GSE18388):** If you know the accession number of the dataset in the original data source (e.g., Gene Expression Omnibus), you can use this filter to locate it within OSDR.
* **Data Source Type (cgene):** Refine your search by specifying the data source type (e.g., cgene for Gene Expression Omnibus, nih\_geo for Gene Expression Omnibus by NIH).
* **Experiment Platform (Animal Enclosure Module):** This filter helps you narrow down datasets based on the specific experimental platform used (e.g., specific instrument, growth chamber).
* **Flight Program (Shuttle):** This field is useful for studies related to a particular spaceflight program (e.g., Shuttle, Apollo).
* **Links (GPL13112):** Search for datasets that are linked to other relevant resources identified by their IDs (e.g., gene expression platform in GEO).
* **Additional Fields:** The API offers a variety of other filter fields encompassing details like the managing NASA center, material type, organism, project information, study characteristics (assay type, technology platform, description), and more.

**Crafting Powerful Search Queries:**

By strategically combining search terms with filter fields, you can formulate highly specific search queries that efficiently navigate the vast amount of data within OSDR. For instance, you could search for datasets related to "spaceflight" that involve "Mus musculus" (house mouse) organisms, were collected during the "Shuttle" program, and focus on "thymus" tissue.

**Remember:**

* Refer to the official OSDR documentation for a complete list of available filter fields and their descriptions.
* Filter fields are powerful tools, but use them judiciously to avoid overly restricting your search results.
* Combine search terms and filter fields creatively to pinpoint datasets that perfectly align with your research needs.

**Syntax 2 (returns HTML response):**

Example Format: [https://osdr.nasa.gov/bio/repo/search?q=](https://osdr.nasa.gov/bio/repo/search?q=)<**SEARCH-TERMS**>\&data\_source=<**DATA-SOURCE**>

**Example(s):**

[https://osdr.nasa.gov/bio/repo/search?q=**cancer**\&data\_source=**cgene**](https://osdr.nasa.gov/bio/repo/search?q=cancer\&data\_source=cgene)

[https://osdr.nasa.gov/osdr/bio/repo/search?q=**mouse%20AND%20liver**\&data\_source=**cgene**](https://osdr.nasa.gov/bio/repo/search?q=mouse%20AND%20liver\&data\_source=cgene)

| Parameters   | Values                                     | Usage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------ | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SEARCH-TERMS | text                                       | <p>Any text to search for, can be augmented by the keywords:</p><ul><li>AND - ALL search terms must be present (default boolean search)</li><li>OR - ANY of your search terms can be present</li><li>NOT - exclude words from your search</li></ul><p>If no conjunctive or disjunctive operator specified, the default is "AND"</p>                                                                                                                                                                                                  |
| DATA-SOURCE  | cgene, nih\_geo\_gse, ebi\_pride, mg\_rast | <ul><li><strong>cgene</strong> - Search authoritative data records in NASA Open Science Data Repository</li><li><strong>nih_geo_gse</strong> - Search authoritative data records in NIH Gene Expression Omnibus database</li><li><strong>ebi_pride</strong> - Search authoritative data records in the European Bioinformatics Institute Proteomics Identification database</li><li><strong>mg_rast</strong> - Search authoritative data records in the Metagenomic Rapid Annotations using Subsystems Technology database</li></ul> |

### &#x20;<a href="#id-67jejmnznql6" id="id-67jejmnznql6"></a>

#### Alternative Search Interface: Syntax Breakdown

This alternative search syntax offers a user-friendly interface for exploring datasets within OSDR:

### **Base URL:** [https://osdr.nasa.gov/bio/repo/search](https://osdr.nasa.gov/bio/repo/search)?

### **Parameters:**

* Values (Text): This is where you enter your search terms. You can use standard search operators (AND, OR, NOT) to refine your search. By default, the system uses "AND" which means all search terms must be present in the results.
* data\_source (String): This parameter specifies the data source you want to search within OSDR. Your options include:
  * cgene: Search authoritative data records in NASA Open Science Data Repository.
  * nih\_geo\_gse: Search authoritative data records in NIH Gene Expression Omnibus database.
  * ebi\_pride: Search authoritative data records in the European Bioinformatics Institute Proteomics Identification database.
  * mg\_rast: Search authoritative data records in the Metagenomic Rapid Annotations using Subsystems Technology database.

**Examples in Action:** Let's see some examples to understand how this syntax works:

1. **Basic Search**: Looking for datasets related to "cancer" within the Gene Expression Omnibus database?

**Use this URL:** [https://osdr.nasa.gov/bio/repo/search?q=cancer\&data\_source=nih\_geo\_gse](https://osdr.nasa.gov/bio/repo/search?q=cancer\&data\_source=nih\_geo\_gse)

1. **Advanced Search with Operators:** Want to find datasets that contain "mouse" AND "liver" within the Gene Expression Omnibus database?

**This URL achieves that:**

[https://osdr.nasa.gov/bio/repo/search?q=mouse%20AND%20liver\&data\_source=nih\_geo\_gse](https://osdr.nasa.gov/bio/repo/search?q=mouse%20AND%20liver\&data\_source=nih\_geo\_gse)

### **Key Points to Remember:** <a href="#l1um6r5i21tp" id="l1um6r5i21tp"></a>

* This syntax returns results in an HTML format, providing a user-friendly interface for browsing datasets.
* You can leverage search operators (AND, OR, NOT) to refine your search criteria.
* This approach may be useful for more general exploration of datasets, while the previously covered JSON-based syntax with filter fields offers more precise control for experienced users.

### Experiments, Missions, Payloads, Hardware, Vehicles, Subjects, Biospecimens <a href="#si5ui8eh4y04" id="si5ui8eh4y04"></a>

Experiments, Missions, Payloads, Hardware, Vehicles, Subjects, and Biospecimens follow the same API format. The "All" call returns a list of all objects within that data type, while the "Single" call returns an expanded version of a specific object. The endpoint for any single object can be selected from the "All" call. Some objects may include links to other objects within the API, such as a vehicle within a mission.

**A Universal API Structure: "All" vs. "Single"**

The OSDR API offers a standardized approach for interacting with various data types. Here's the core concept:

**All Call:** This endpoint retrieves a list of all objects within a specific data type.

For example, using the **"All"** call for experiments would return a list of all experiments stored in OSDR.

**Single Call:** This endpoint allows you to delve deeper and access detailed information about a particular object within a data type.

To use the **"Single"** call, you'll need the unique identifier of the specific object you're interested in. These identifiers can often be found within the response from the "All" call.

**API Endpoints: Your Gateways to Information**

Here's a breakdown of the API endpoints for each data type, allowing you to retrieve information using the "All" or "Single" call structure:

Important Considerations:

* Remember to replace {identifier} in the "Single" call URLs with the actual identifier of the specific object you're interested in. You can often find these identifiers within the response from the corresponding "All" call.
* The response from the API will be delivered in JSON format, making it easy to parse and integrate into your bioinformatics workflows.

**Some objects may contain links to other objects within the API.**

* Experiments:
  * All: [https://osdr.nasa.gov/geode-py/ws/api/experiments](https://osdr.nasa.gov/geode-py/ws/api/experiments) (lists all experiments)
  * Single: [https://osdr.nasa.gov/geode-py/ws/api/experiment/](https://osdr.nasa.gov/geode-py/ws/api/experiment/) + {identifier} (detailed information about a specific experiment)
* Missions:
  * All: [https://osdr.nasa.gov/geode-py/ws/api/missions](https://osdr.nasa.gov/geode-py/ws/api/missions) (lists all missions)
  * Single: [https://osdr.nasa.gov/geode-py/ws/api/mission/](https://osdr.nasa.gov/geode-py/ws/api/mission/) + {identifier} (detailed information about a specific mission)
* Payloads:
  * All: [https://osdr.nasa.gov/geode-py/ws/api/payloads](https://osdr.nasa.gov/geode-py/ws/api/payloads) (lists all payloads)
  * Single: [https://osdr.nasa.gov/geode-py/ws/api/payload/](https://osdr.nasa.gov/geode-py/ws/api/payload/) + {identifier} (detailed information about a specific payload)
* Hardware:
  * All: [https://osdr.nasa.gov/geode-py/ws/api/hardware](https://osdr.nasa.gov/geode-py/ws/api/hardware) (lists all hardware)
  * Single: [https://osdr.nasa.gov/geode-py/ws/api/hardware/](https://osdr.nasa.gov/geode-py/ws/api/hardware/) + {identifier} (detailed information about a specific hardware component)
* Vehicles:
  * All: [https://osdr.nasa.gov/geode-py/ws/api/vehicles](https://osdr.nasa.gov/geode-py/ws/api/vehicles) (lists all vehicles)
  * Single: [https://osdr.nasa.gov/geode-py/ws/api/vehicle/](https://osdr.nasa.gov/geode-py/ws/api/vehicle/) + {identifier} (detailed information about a specific vehicle)
* Subjects:
  * All: [https://osdr.nasa.gov/geode-py/ws/api/subjects](https://osdr.nasa.gov/geode-py/ws/api/subjects) (lists all subjects)
  * Single: [https://osdr.nasa.gov/geode-py/ws/api/subject/](https://osdr.nasa.gov/geode-py/ws/api/subject/) + {identifier} (detailed information about a specific subject)
* Biospecimens:
  * All: [https://osdr.nasa.gov/geode-py/ws/api/biospecimens](https://osdr.nasa.gov/geode-py/ws/api/biospecimens) (lists all biospecimens)
  * Single: [https://osdr.nasa.gov/geode-py/ws/api/biospecimen/](https://osdr.nasa.gov/geode-py/ws/api/biospecimen/) + {identifier} (detailed information about a specific biospecimen)

**Examples in Action:**

**Single Mission Example:** Want to know everything about the SpaceX-12 mission? Use this URL: [https://osdr.nasa.gov/geode-py/ws/api/mission/SpaceX-12](https://osdr.nasa.gov/geode-py/ws/api/mission/SpaceX-12)

**Single Vehicle Example:** Curious about the details of the Dragon spacecraft? This URL provides the answer: [https://osdr.nasa.gov/geode-py/ws/api/vehicle/Dragon](https://osdr.nasa.gov/geode-py/ws/api/vehicle/Dragon)

### &#x20;<a href="#g4dbf6ytvc9o" id="g4dbf6ytvc9o"></a>

### **Tutorial using R Code for Bioinformatics Analysis with NASA OSDR** <a href="#id-69hdujge0cpk" id="id-69hdujge0cpk"></a>

### This tutorial guides you through leveraging R code to access, analyze, and visualize data from the NASA Open Science Data Repository (OSDR) for differential expression and pathway enrichment analysis. <a href="#id-8nsftjty6wh" id="id-8nsftjty6wh"></a>

#### **Step 1: Accessing Metadata and Data** <a href="#id-2cp6z3lz7neo" id="id-2cp6z3lz7neo"></a>

**1.1 (Optional) Tokenization:** While user authentication isn't required for this specific example, obtaining a token might be necessary for some functionalities. Refer to the OSDR documentation for details on token acquisition.

**1.2 Metadata Retrieval:**

We'll use the httr library to retrieve metadata for a specific study (e.g., OSD-569). This includes information on samples, factors, and timestamps.

**Code snippet**

**` ``` `**

`library(httr)`

`get.csv <- function(url, ...) {`

`response <- GET(url, add_headers(Authorization = paste("Bearer", TOKEN)))`

`return(read.csv(text = content(response), ...))`

`}`

`# Replace "TOKEN" with your actual token (if needed)`

`GLOPENAPI <- "https://visualization.genelab.nasa.gov/GLOpenAPI/"`

`query <- URLencode("id=OSD-569&study.factor value")`

`metadata <- get.csv(paste0(GLOPENAPI, "metadata/?", query), skip = 1)`

`summary(metadata) # View metadata column information`

` ``` `

**1.3 Data Retrieval:**

We'll retrieve unnormalized RNA-Seq counts data (suitable for differential expression analysis) for OSD-569.

**Code snippet**

query <- URLencode("id=OSD-569\&file.datatype=unnormalized counts")

url <- paste0(GLOPENAPI, "data/?", query)

data <- get.csv(url, check.names = FALSE, skip = 2, row.names = 1)

#### **Step 2: Differential Expression Analysis** <a href="#cfu8sz9mb7sx" id="cfu8sz9mb7sx"></a>

**2.1 Data Preparation:**

Ensure gene names are set as row names and sample names as column names. You might need to perform additional preprocessing steps like normalization and filtering depending on the chosen analysis data type.

**2.2 Performing Differential Expression Analysis:**

This example utilizes DESeq2 for differential expression analysis with unnormalized counts. Here, we classify timestamps into preflight, postflight, and recovery based on specific criteria.

**Code snippet**

**` ``` R `**

`rownames(metadata) <- metadata$sample.name`

`metadata$status <- sapply(metadata$timestamp, function(t) {`

`ifelse(t == "R+1", "postflight",`

`ifelse(startsWith(t, "R+"), "recovery",`

`"preflight"))`

`})`

`library(DESeq2)`

`dds <- DESeqDataSetFromMatrix(round(na.omit(data)),`

`# Ensure integer values and no NaNs`

`metadata, ~status + subject,`

`)`

`lrt <- DESeq(dds, test = "LRT", reduced = ~subject)`

`deg <- results(lrt, contrast = c("status", "postflight", "preflight"))`

`# Consider adding functionalities for multiple contrasts here.`

` ``` `

#### **Step 3: Pathway Enrichment Analysis** <a href="#boaekpp8sp8l" id="boaekpp8sp8l"></a>

There are many R packages to visualize pathway enrichment based on the results of the differential expression analysis and the subsequent clustering and intersect analysis.

` ``` R `

`library(msigdbr)`

`C2 = msigdbr(species="human", category="C2")`

`pathways = split(x=C2$ensembl_gene, f=C2$gs_name)`

`library(fgsea)`

`deg$rank = deg$padj * sign(deg$log2FoldChange)`

`ranks = with(na.omit(deg), setNames(rank, rownames(na.omit(deg))))`

`plotEnrichment(pathways$DIAZ_CHRONIC_MYELOGENOUS_LEUKEMIA_UP, ranks)`

` ``` `

**Conclusions**

By following this tutorial, researchers can effectively access, analyze, and derive insights from the rich biological datasets available through the NASA Open Science Data Repository. This tutorial serves as a foundational guide for bioinformatics professionals aiming to explore space-induced biological responses and advance research in understanding the impact of space travel on human health.

**Citation:**

\[1] Sylvain Costes, Lauren Sanders, Kirill Grigorev et al. Inspiration4 Data Access through the NASA Open Science Data Repository, 05 January 2024, PREPRINT (Version 1) available at Research Square \[https://doi.org/10.21203/rs.3.rs-3755391/v1]

### Getting Started with OSDR Data in AWS S3 buckets <a href="#a5sz8b4klkm8" id="a5sz8b4klkm8"></a>

This how-to guide is for new users who would like to access and work with the Open Science Data Repository (OSDR) data available on the Registry of Open Data on AWS. This initiative, as part of the Science Mission Directorate (SMD) Open-Source Science Initiative, aims to enhance data accessibility for open science within the NASA space biology community. Through the OSDR S3 bucket, users can access a diverse range of data including microbe, plant, fruit fly, rodent, human cell culture, ground study, and commercial astronaut studies. This guide will walk you through the steps of installing the AWS Command Line Interface (CLI) and utilizing it to access OSDR data.

### Introduction to OSDR Data on AWG <a href="#id-8ye2imi3hl09" id="id-8ye2imi3hl09"></a>

**A Universe of Data at Your Fingertips: The OSDR S3 Bucket**

The OSDR data resides within a special storage unit on AWS called an S3 bucket. This bucket holds a vast collection of data types, ready to fuel your research endeavors. It encompasses data related to experiments, missions, organisms, and more, all relevant to space biosciences.

**Two Keys to Unlock the Data: Your Access Options**

To access and explore this wealth of information, you have two primary methods:

**AWS S3 Browser Interface:** This user-friendly web interface allows you to visually navigate the OSDR data. It's a fantastic starting point for getting acquainted with the data and exploring its organization. Simply visit the following URL to launch the browser interface:\
Link:[ http://nasa-osdr.s3-website-us-west-2.amazonaws.com/](http://nasa-osdr.s3-website-us-west-2.amazonaws.com/)

**AWS Command Line Interface (CLI):** For those comfortable with command-line tools, the AWS CLI provides a powerful way to programmatically access and interact with the OSDR data. This approach offers greater flexibility and automation for researchers. The remaining lectures will focus on mastering the AWS CLI for programmatic access to the OSDR data.

### Installing the AWS CLI <a href="#h80amja1dt3q" id="h80amja1dt3q"></a>

Before you can start working with OSDR data using the AWS CLI, you need to install it on your system. Follow these steps to install the AWS CLI:

* Open a terminal window
* Visit the following link for installation instructions: [Install or update the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* Once the AWS CLI is installed, you're ready to start exploring OSDR data programmatically

#### Prerequisites: Equipping Yourself AWS CLI data access. <a href="#eiq0tb4h8v68" id="eiq0tb4h8v68"></a>

**An AWS Account:** If you don't have one already, setting up a free tier AWS account grants you access to a limited amount of AWS services, which should be sufficient for most initial explorations of the OSDR data.

**AWS CLI Installation:** Download and install the AWS CLI on your machine following the official instructions provided by AWS [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

**Learning the Language of the AWS CLI:** The AWS CLI is a command-line tool that allows users to interact with Amazon Web Services (AWS) services. Some basic commands to get started with the AWS CLI include "aws configure" to set up your credentials, "aws help" to get help on commands and options, "aws ec2 describe-instances" to list your EC2 instances, "aws s3 ls" to list your S3 buckets, and "aws iam list-users" to list your IAM users.

aws s3 ls**:** This command allows you to list the contents of an S3 bucket. For instance, to list the datasets within the OSDR S3 bucket, you could use:

aws s3 ls s3://nasa-osdr/

aws s3 cp**:** This command enables you to copy data from the S3 bucket to your local machine. For example, to download a specific data file named experiment.csv from the OSDR bucket, you could use:

aws s3 cp s3://nasa-osdr/experiment.csv ./experiment.csv

aws s3 head**:** Use this command to get information about a specific S3 object (file or folder) within the bucket. This can be helpful to determine the size and creation date of a dataset before downloading.

These are just a few foundational commands. The AWS CLI offers a comprehensive set of functionalities for managing and interacting with data stored in S3 buckets. Refer to the official AWS CLI documentation[ https://docs.aws.amazon.com/cli/](https://docs.aws.amazon.com/cli/) for a complete list of commands and detailed explanations.

#### &#x20;<a href="#lpahhb6lzyrc" id="lpahhb6lzyrc"></a>

#### Navigating the OSDR Data Landscape <a href="#qtcs4a9vt67d" id="qtcs4a9vt67d"></a>

The OSDR S3 bucket is meticulously organized. Data is typically stored within folders based on projects, missions, or experiment types. By using the aws s3 ls command recursively (with the -r flag), you can explore the folder hierarchy and identify the datasets relevant to your research.

**For instance, the command:**

\`\`\`bash

aws s3 ls -r s3://nasa-osdr/SpaceX-12/

` ``` `

This reveal subfolders containing data from the SpaceX-12 mission, allowing you to pinpoint specific datasets of interest.

#### Automating Your Workflow: Scripting with the AWS CLI <a href="#id-72f4q5osv6ai" id="id-72f4q5osv6ai"></a>

The true power of the AWS CLI lies in its ability to be integrated into scripts. By stringing together commands and incorporating conditional statements, you can automate repetitive tasks such as downloading multiple datasets or filtering data based on specific criteria. Learning basic scripting principles will unlock this advanced functionality.

#### Exploring OSDR Data <a href="#pexwa1fo84wi" id="pexwa1fo84wi"></a>

Now that you have the AWS CLI installed, you can use it to explore OSDR data in the S3 bucket.

Here are some basic commands to help you get started:

To list the contents of the OSDR S3 bucket (command line):

` ```bash `

`aws s3 ls --no-sign-request s3://nasa-osdr/`

` ``` `

To list the contents of a specific OSDR dataset (e.g., OSD-96):

` ```bash `

`aws s3 ls --no-sign-request s3://nasa-osdr/OSD-96/ --recursive`

` ``` `

#### Copying Data Locally <a href="#tfkokc87qin5" id="tfkokc87qin5"></a>

To copy specific files from the OSDR S3 bucket to your local machine, you can use the aws s3 cp command. For example:

* To copy a specific file to your local directory:

\`\`\`bash

aws s3 cp --no-sign-request s3://nasa-osdr/OSD-96/version-6/rna\_seq/GLDS-96\_rna\_seq\_Dmel\_Can-S\_wo\_GC\_5th-gen-GC-der\_1.5hr\_GSM2350418\_R2\_raw.fastq.gz\_trimming\_report.txt

\`\`\`

* To copy all files within a specific dataset to your local directory:

\`\`\`bash

aws s3 cp --no-sign-request s3://nasa-osdr/OSD-96/ --recursive

\`\`\`

### Additional Resources <a href="#o603fbfwinv0" id="o603fbfwinv0"></a>

If you're looking to delve deeper into OSDR data access and AWS capabilities, consider exploring the following resources:

* [AWS CLI Documentation:](https://aws.amazon.com/cli/) Comprehensive documentation for the AWS CLI, covering various commands and features
* [AWS S3 Documentation:](https://aws.amazon.com/s3/) Learn more about Amazon Simple Storage Service (S3) and its capabilities
* [Registry of Open Data on AWS:](http://nasa-osdr.s3-website-us-west-2.amazonaws.com/) Explore the OSDR data repository using the AWS S3 browser interface
* [NASA Space Biology Open Science Data Repository (OSDR):](https://osdr.nasa.gov/) The official website for the OSDR project, providing information about datasets and research

This tutorial serves as a starting point for beginners to access and explore OSDR data using the AWS CLI. As you become more familiar with the tools and resources, you can expand your knowledge and take advantage of advanced features for data analysis and research.

Please [Contact Us](https://osdr.nasa.gov/bio/help/contact.html) if you have any questions or need further assistance.

Happy exploring the world of open science data on AWS!

### AWS S3 bucket GUI setup <a href="#p9mbqgvy1fww" id="p9mbqgvy1fww"></a>

How to use Cyberduck (on mac and PC) to access S3 buckets

Setting up a GUI for S3 bucket visualization

The issue with cyber duck, during connection you will be prompted for

“Account name”, “Access Key ID” and the “Secret Access Key”

How does one get these terms in order to access the OSDR-S3 bucket through the cyberduck GUI?

This will all allow other similar tools to access the data.

#### RadLab API Syntax <a href="#c7nh1nbl3qjq" id="c7nh1nbl3qjq"></a>

The data can be retrieved programmatically with queries sent as a GET request to [https://visualization.osdr.nasa.gov/radlab/api](https://visualization.osdr.nasa.gov/radlab/api).

**Queries can be constructed using one of two approaches:** either as [key-value pairs](https://visualization.osdr.nasa.gov/radlab/gui/data-access/) (a simple approach, but with limited complexity with regard to nesting logical expressions), or as [boolean expressions](https://visualization.osdr.nasa.gov/radlab/gui/data-access/) (allow combining AND, OR, NOT, and comparison operators with optional parentheticals). The API responds with data in JSON format, making it easy to integrate with bioinformatics analyses. Two approaches to using the API are mutually exclusive.

The API will return an error if there is an attempt to mix the two syntaxes: _e.g.,_ query='spacecraft=ISS'\&instrument=REM\&timestamp will not be accepted; instead, either the key-value pair syntax should be used, _i.e._ spacecraft=ISS\&instrument=REM\&timestamp, or the boolean expression syntax, _i.e._ query='(spacecraft=ISS)AND(instrument=REM)'\&fields+=timestamp.

**Reaching for the Data: API Syntax Demystified**

The RadLab API utilizes GET requests to retrieve data. Here's how you can craft your queries:

**Endpoint URL:** https://visualization.osdr.nasa.gov/radlab/api

This is the foundation of your API request URL.

**Query Construction:** You have two main approaches to construct your queries:

1. Key-Value Pairs (Simple but Limited):\
   This method involves specifying parameters and their corresponding values separated by an equal sign (=), connected with ampersands (&). It's a straightforward approach, but it may struggle with complex queries that involve nested logical expressions (e.g., combining multiple filters with AND, OR, and NOT operators).\
   **Example:** spacecraft=ISS\&instrument=REM\&timestamp
2. This query retrieves data where the spacecraft is the International Space Station (ISS), the instrument is the Radiation Exposure Monitor (REM), and includes the timestamp field in the response.
3. Boolean Expressions (Powerful and Flexible):\
   This approach offers greater control by allowing you to combine logical operators (AND, OR, NOT) and comparison operators (e.g., =, >, <) to construct intricate filters. You can even leverage parentheses for more complex logic.\
   **Example:** query='(spacecraft=ISS)AND(instrument=REM)'\&fields+=timestamp
4. This query retrieves data where both conditions are met: spacecraft must be ISS AND the instrument must be REM. It also includes the timestamp field using the fields parameter (more on that later).



**Key-value pair syntax; data fields**

| Key               | Type                                              | Description                                | Unit        | Value format                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Examples                                                                                                                                                                                   |
| ----------------- | ------------------------------------------------- | ------------------------------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| source            | string                                            | name of source (data provider)             |             | <ul><li>empty: Request the field without applying filters to its values</li><li>=value: Match value</li><li>=value1|value2: Match value1 or value2</li></ul>                                                                                                                                                                                                                                                                                                                  | <p>source</p><p>source=DORELI</p><p>source=DORELI|BAS</p>                                                                                                                                  |
| spacecraft        | string                                            | name of spacecraft                         |             | <p>spacecraft</p><p>spacecraft=ISS</p>                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                            |
| instrument        | string                                            | name of instrument                         |             | <p>instrument</p><p>instrument=Liulin-5-1D</p><p>instrument=Lidal|REM</p>                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                                            |
| timestamp         | <p>ISO-formatted string</p><p>(or Unix epoch)</p> | timestamp of recorded value(s)             |             | <ul><li>empty: Request the field without applying filters to its values</li><li>&#x3C;value: Match any less than value</li><li>&#x3C;=value: Match any less or equal to value</li><li>=value: Match value</li><li>>=value: Match any greater or equal to value</li><li>>value: Match any greater than value</li></ul><p>Note: can be used more than once in a single query.</p><p>Note: special characters (&#x3C;, >, :) may need to be URL-encoded (see "Notes" below).</p> | <p>timestamp</p><p>timestamp=2021-01-01T15:25</p><p>timestamp&#x3C;=2021-01-01T15:25</p><p>timestamp>=2022-01-01T00:00&#x26;timestamp&#x3C;2023-01-01T00:00</p><p>timestamp>1683786900</p> |
| dose\_rate\_total | number                                            | total radiation dose rate                  | μGy/hour    | <p>dose_rate_total</p><p>dose_rate_total>=2</p>                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                                            |
| flux\_total       | number                                            | total particle flux                        | cm-2sr-1s-1 | <p>flux_total</p><p>flux_total&#x3C;1</p>                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                                            |
| latitude          | number                                            | latitude of spacecraft at given timestamp  | deg         | <p>latitude</p><p>latitude&#x3C;-10</p>                                                                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                            |
| longitude         | number                                            | longitude of spacecraft at given timestamp | deg         | <p>longitude</p><p>longitude>30</p>                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                                            |
| altitude          | number                                            | altitude of spacecraft at given timestamp  | km          | <p>altitude</p><p>altitude>=420</p>                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                                            |
| B                 | number                                            | B value                                    | nT          | <p>B</p><p>B&#x3C;=50000</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                                            |
| L                 | number                                            | L value                                    |             | <p>L</p><p>L>3</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                            |



**Boolean expression syntax**

| **Key** | **Aliases**                                | **Type** | **Description**                                                                                                                                       | **Examples**                                                                                                                                                                                                                                                                                           |
| ------- | ------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| query   |                                            | string   | a boolean query referencing fields described in the "data fields" table above, and using AND, OR, NOT, =, !=, <=, >= operators and parentheses ((, )) | <p>query=(timestamp>=2023-05-16)AND((instrument=REM)OR(spacecraft=LND))</p><p>Note: spaces inside the query string are allowed (e.g. spacecraft = LND); the query can be optionally encased in single or double quotes. However, spaces and quotes may need to be URL-encoded (see "Notes" below).</p> |
| fields+ | <p>fields</p><p>columns</p><p>columns+</p> | string   | a comma-separated list of additional fields to retrieve (i.e. fields not already implicated in the boolean query)                                     | fields+=dose\_rate\_total,flux\_total                                                                                                                                                                                                                                                                  |

**Auxiliary keys (used with both syntaxes)**

| **Key** | **Type** | **Description** | **Unit** | **Value format**                                                                                                          | **Examples**                        |
| ------- | -------- | --------------- | -------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| format  | string   | output format   |          | <ul><li>(not speficied): Use the default format (csv)</li><li>=value: Use "value" (one of csv, tsv, json, html)</li></ul> | <p>format=tsv</p><p>format=json</p> |

Notes

* Special characters (spaces, |, <, >, :, ', ") may need to be URL-encoded _(although_ e.g. _Python will only complain if spaces are not encoded and will accept all other characters as-is; therefore, this depends on the use case):_
  * → %20 (space)
  * \| → %7C
  * < → %3C
  * \> → %3E
  * : → %3A
  * ' → %27
  * " → %22
* Therefore, if this reference describes a query like timestamp<=2021-01-01T15:25, it may need to be sent as timestamp%3C=2021-01-01T15%3A25.
* Field _names_ are case insensitive (_i.e._ timestamp is the same as TimeStamp); string _values_ are not (_i.e._ REM is valid, but reM is not).
* Boolean expression operators are case sensitive, _i.e._ AND is understood as an operator, while and will result in a syntax error. Only the operators listed in the tables above are accepted.

**Examples**

* Key-value pair syntax
  * Dose rate and flux readings from DOSTEL1 and DOSTEL2 on the ISS between 11 PM on 01 Apr 2022, inclusive, and 1:05 AM on 02 Apr 2022, non-inclusive, only where the dose rate is above 2 μGy/hour, together with the spatial and magnetic coordinates of the ISS and the data provider name, formatted as HTML:
    * Conceptually:\
      https://visualization.osdr.nasa.gov/radlab/api/\
      ?spacecraft=ISS\
      \&instrument=DOSTEL1|DOSTEL2\
      \&source\
      \&timestamp>=2022-04-01T23:00\
      \&timestamp<2022-04-02T01:05\
      \&dose\_rate\_total>2\
      \&flux\_total\
      \&latitude\
      \&longitude\
      \&altitude\
      \&b\
      \&l\
      \&format=html
    * URL-encoded _(may not be necessary)_:\
      https://visualization.osdr.nasa.gov/radlab/api/\
      ?spacecraft=ISS\
      \&instrument=DOSTEL1%7CDOSTEL2\
      \&source\
      \&timestamp%3E=2022-04-01T23%3A00\
      \&timestamp%3C2022-04-02T01%3A05\
      \&dose\_rate\_total%3E2\
      \&flux\_total\
      \&latitude\
      \&longitude\
      \&altitude\
      \&b\
      \&l\
      \&format=html
    * Full URL: [https://visualization.osdr.nasa.gov/radlab/api/?spacecraft=ISS\&instrument=DOSTEL1%7CDOSTEL2\&source\&timestamp%3E=2022-04-01T23%3A00\&timestamp%3C2022-04-02T01%3A05\&dose\_rate\_total%3E2\&flux\_total\&latitude\&longitude\&altitude\&b\&l\&format=html](https://visualization.osdr.nasa.gov/radlab/api/?instrument=DOSTEL1%7CDOSTEL2\&spacecraft=ISS\&source\&timestamp%3E=2022-04-01T23%3A00\&timestamp%3C2022-04-02T01%3A05\&dose\_rate\_total%3E2\&flux\_total\&latitude\&longitude\&altitude\&b\&l\&format=html)
    * Full URL without encoding (should work in most browsers, Python, ...): [https://visualization.osdr.nasa.gov/radlab/api/?spacecraft=ISS\&instrument=DOSTEL1|DOSTEL2\&source\&timestamp>=2022-04-01T23:00\&timestamp<2022-04-02T01:05\&dose\_rate\_total>2\&flux\_total\&latitude\&longitude\&altitude\&b\&l\&format=html](https://visualization.osdr.nasa.gov/radlab/api/?instrument=DOSTEL1%7CDOSTEL2\&spacecraft=ISS\&source\&timestamp%3E=2022-04-01T23:00\&timestamp%3C2022-04-02T01:05\&dose\_rate\_total%3E2\&flux\_total\&latitude\&longitude\&altitude\&b\&l\&format=html)
* Boolean expression syntax
  * Dose rate readings from all detectors _not_ on the ISS between 15 Jul 2020 inclusive and 23 Jul 2020, non-inclusive; also retrieve the name of the instrument for each reading, and format the output as TSV:
    * Conceptually:\
      query: timestamp >= 2020-07-15 AND timestamp < 2020-07-23 AND NOT spacecraft = ISS\
      additional fields: dose\_rate\_total, instrument\
      format: tsv
    * URL-encoded, and strategically using parentheses to avoid having to also encode spaces in the query _(may not be necessary)_:\
      https://visualization.osdr.nasa.gov/radlab/api/\
      ?query=(timestamp%3E=2020-07-15)AND(timestamp%3C2020-07-23)AND(NOT(spacecraft=ISS))\
      \&fields+=dose\_rate\_total,instrument\
      \&format=tsv
    * Full URL: [https://visualization.osdr.nasa.gov/radlab/api/?query=(timestamp%3E=2020-07-15)AND(timestamp%3C2020-07-23)AND(NOT(spacecraft=ISS))\&fields+=dose\_rate\_total,instrument\&format=tsv](https://visualization.osdr.nasa.gov/radlab/api/?query=\(timestamp%3E=2020-07-15\)AND\(timestamp%3C2020-07-23\)AND\(NOT\(spacecraft=ISS\)\)\&fields+=dose\_rate\_total,instrument\&format=tsv)
    * Full URL without encoding (should work in most browsers, Python, ...): [https://visualization.osdr.nasa.gov/radlab/api/?query=(timestamp>=2020-07-15)AND(timestamp<2020-07-23)AND(NOT(spacecraft=ISS))\&fields+=dose\_rate\_total,instrument\&format=tsv](https://visualization.osdr.nasa.gov/radlab/api/?query=\(timestamp%3E=2020-07-15\)AND\(timestamp%3C2020-07-23\)AND\(NOT\(spacecraft=ISS\)\)\&fields+=dose\_rate\_total,instrument\&format=tsv)

#### Key-Value Pairs: A Simpler Approach

The key-value pair syntax offers a straightforward method for crafting API requests. Here's how it works:

* **Keys:** These represent the data fields you want to filter or retrieve. Refer to the provided table for a list of available data fields (source, spacecraft, instrument, etc.).
* **Values:** These specify the criteria for filtering the data. Values can be:
  * **Empty:** This includes all values for that data field in the response.
  * **Specific Value:** Retrieve data entries where that field matches the exact value you provide (e.g., spacecraft=ISS for data from the International Space Station).
  * **Multiple Values (separated by** |**):** Retrieve data entries where the field matches any of the listed values (e.g., instrument=DOSTEL1|DOSTEL2 for data from either instrument).

**Example:** Imagine you're interested in dose rate and flux readings from both DOSTEL1 and DOSTEL2 on the ISS between April 1st, 2022 (11 PM) and April 2nd, 2022 (1:05 AM), focusing only on entries where the dose rate surpasses 2 μGy/hour. You'd also like to include the spatial coordinates (latitude, longitude, and altitude) of the ISS during that time frame, along with the data source (who provided the information). Here's the key-value pair construction for this scenario:

?spacecraft=ISS

\&instrument=DOSTEL1|DOSTEL2

\&source

\&timestamp>=2022-04-01T23:00 \&timestamp<2022-04-02T01:05 \&dose\_rate\_total>2

\&flux\_total

\&latitude

\&longitude

\&altitude

#### Data Fields: The Core of Your Query

The data field table is your treasure map, guiding you to the specific data points you can retrieve using the API. This table details:

* **Key:** The data field name (e.g., source, spacecraft, instrument).
* **Type:** The data type of the field (e.g., string, number).
* **Description:** A clear explanation of what the data field represents.
* **Unit:** The unit of measurement for numerical data fields (e.g., μGy/hour for dose rate).
* **Value format:** How you should specify values in your queries (e.g., dates in ISO format, multiple values separated by pipes).
* **Examples:** Demonstrations of how to construct queries using that specific data field.

### **Important Considerations:**

* Special characters like <, >, :, and spaces might require URL encoding depending on your programming language. The reference table provides details on how to handle this encoding.
* Field names are case-insensitive (e.g., source is the same as Source), but string values are case-sensitive (e.g., REM is valid, but rem is not).
* Boolean operators (AND, OR, NOT) are case-sensitive.
