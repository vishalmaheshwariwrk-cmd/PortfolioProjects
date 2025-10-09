Overview
This individual project was developed to design and implement a menu-driven hospital management system aimed at supporting hospital staff during the COVID-19 pandemic. 
The system enables efficient registration, testing, and tracking of patients, thereby reducing manual workload and improving record accessibility.

Purpose
The project addresses the issue of disorganised and unregistered patient data during the pandemic. It provides hospital staff with a simplified platform to:
Register patients across defined categories
Record and manage COVID-19 test results
Generate statistical reports in real time
Maintain records of active, recovered, and deceased patients

System Design
The program is written in Python, using file handling (.txt files) to store and retrieve patient and testing information. It features:
A main menu with six options (Registration, Testing, Statistical Information, Patient Records, Deceased Records, Exit)
Five patient groups (AEO, ACC, ATO, AHS, SID) representing different exposure types
Functions for registration, multiple testing stages, and automatic status assignment
Statistical computation of active/recovered/deceased cases by zone and category
File-based storage for persistent record management

Key Functionalities
Registration: Captures personal data (name, age, contact, height, weight, category, zone, etc.)
Testing: Conducts up to three test cycles per patient, automatically generating case IDs
Statistics: Outputs real-time metrics such as total cases, group-wise and zone-wise counts
Records Management: Allows search by patient or case ID and lists deceased patients

Outcome
The system successfully demonstrates the use of modular programming, file manipulation, and logical control structures to create a functional hospital information system.
It was designed to be scalable and adaptable—capable of modification for future public health emergencies or hospital record systems.
