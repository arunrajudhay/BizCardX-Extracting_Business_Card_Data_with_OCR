# BizCardX-Extracting_Business_Card_Data_with_OCR
## Introduction:
In today's business world, managing contact information efficiently is vital for networking. Manual entry of business card details is time-consuming and error-prone, but developers can automate this with Optical Character Recognition (OCR) and databases. EasyOCR, an open-source Python library, uses deep learning to accurately extract text from images. By integrating EasyOCR with a MySQL database, developers can automate the extraction and storage of business card data, ensuring organized and quick access to important information.

## Table of Contents:
1. Pre-requisites
2. Key Technologies and Skills
3. Usage
4. Approach
5. Learning outcomes of this project
6. Contribution
7. Further Improvements

## Pre-requisites:
Install the following packages to run the project :
1. pip install streamlit
2. pip install easyocr
3. pip install mysql.connector
4. pip install PIL.Image
5. pip install cv2
6. pip install oc
7. pip install re
8. pip install streamlit_option_menu
9. pip install pandas as pd

## Key Technologies and Skills:
1. Python
2. MySQL
3. Pandas
4. EasyOCR Implementation
5. Streamlit

## Usage:
1. Clone the repository
2. Install the required packages
3. Run the Streamlit app by using the streamlit command streamlit run Bizcard.py
4. Access the app in your browser

## Approach:
1. After running the streamlit command, a webpage will be displayed in browser where i have created the app with three menu options namely HOME, UPLOAD & EXTRACT, MODIFY where user has the option to upload the respective Business Card whose information has to be extracted, stored, modified or deleted if needed.

2. Once user uploads a business card, the text present in the card is extracted by easyocr library.

3. The extracted text is sent to get_data() function(user defined- I have coded this function) for respective text classification as company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code using loops and some regular expression.

4. The classified data is displayed on screen which can be further edited by user based on requirement.

5. On Clicking Upload to Database Button the data gets stored in the MySQL Database. (Note: Provide respective host, user, password, database name in create_database, sql_table_creation and connect_database for establishing connection.)

6. Further with the help of MODIFY menu the uploaded data’s in SQL Database can be accessed for Read, Update and Delete Operations.

## Learning outcomes of this project:
1. The project creates an automated system that extracts multilingual text from business cards using EasyOCR and stores it in a MySQL database, eliminating manual data entry.

2. Users can upload business card images via a simple interface, and the extracted data, such as names and contact info, is validated and stored efficiently for quick access.

3. The system handles real-time error management, ensuring accurate text extraction and reliable data storage, reducing human errors.

4. The entire workflow, from OCR-based extraction to dynamic data storage, demonstrates proficiency in Python, MySQL integration, and automation, enhancing business process efficiency.

5. The project provides practical experience in handling scalable solutions, making it a valuable tool for streamlining networking, contact management, and future expansion.

## Contribution:
Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to submit a pull request.

## Contact:

Email : [ruarunraj2013@gmail.com](mailto:ruarunraj2013@gmail.com)

Linkedin : https://www.linkedin.com/in/arunraj-r-u-27722a146

Thanks for showing interest in this repository !







