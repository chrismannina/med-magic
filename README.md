# MedMagic

***MedMagic*** is a simple application that allows users to search for any clinical drug through the National Library of Medicine's RxNorm API.

## Table of Contents

- [What is RxNorm?](#what-is-rxnorm)
- [How to Use](#how-to-use)
- [Other Information](#other-information)

## What is RxNorm?

**RxNorm** is two things: a normalized naming system for generic and branded drugs; and a tool for supporting semantic interoperation between drug terminologies and pharmacy knowledge base systems. The National Library of Medicine (NLM) produces RxNorm.

### Purpose of RxNorm
Hospitals, pharmacies, and other organizations use computer systems to record and process drug information. Because these systems use many different sets of drug names, it can be difficult for one system to communicate with another. To address this challenge, RxNorm provides normalized names and unique identifiers for medicines and drugs. The goal of RxNorm is to allow computer systems to communicate drug-related information efficiently and unambiguously.

### Scope of RxNorm 
RxNorm contains the names of prescription and many over-the-counter drugs available in the United States. RxNorm includes generic and branded:

#### Clinical drugs 
- Pharmaceutical products given to (or taken by) a patient with therapeutic intent

#### Drug packs
- packs that contain multiple drugs, or drugs designed to be administered in a specified sequence

*Non-therapeutic radiopharmaceuticals, bulk powders, contrast media, food, dietary supplements, and medical devices are all out-of-scope for RxNorm. Medical devices include but are not limited to bandages and crutches.*

## How to Use

To run this application locally, please follow the instructions below.

#### Requirements
- Python 3
#### Installation
```
git clone https://github.com/chrismannina/med-magic.git
cd med-magic
pip install -r requirements.txt
```
#### Start Up
```
python wsgi.py
```
- By default the service will be hosted on http://localhost:5000/
- The port can be changed by editing ```wsgi.py``` to include the port you choose: ```app.run(port=1337)``` 
- Press ctrl+c to end hosting

### Other Information

MedMagic also includes an image search running off a microservice. Simply navigate to the search page, select 'Image' in the drop down and search for anything you want! The image microservice is currently deployed [here](https://image-srv.herokuapp.com/), and the source code can be found [here](https://github.com/shenalexw/image-microservice). 

MedMagic also utilizes a UUID generator microservice. The UUID generator is currently deployed [here](https://uuid-genie.herokuapp.com/), and the source code can be found [here](https://github.com/chrismannina/uuid-genie).