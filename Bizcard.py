import pandas as pd
import streamlit as st
import easyocr
import mysql.connector as sql
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re
from streamlit_option_menu import option_menu

# CREATING OPTION MENU
selected = option_menu(None, ["Home", "Upload & Extract", "Modify"], 
                       icons=["house", "upload", "edit"],  # Updated icons here
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "0px", "--hover-color": "#6495ED"},
                               "icon": {"font-size": "35px"},
                               "container": {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#6495ED"}})

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

# CONNECTING WITH MYSQL DATABASE
mydb = sql.connect(host="localhost",
                   user="root",
                   password="Arunudhay2024",
                   database="bizcardx_db"
                  )
mycursor = mydb.cursor(buffered=True)

# TABLE CREATION
mycursor.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')

# HOME MENU
if selected == "Home":
        st.markdown("## :green[**Technologies Used :**] Python, easy OCR, Streamlit, SQL, Pandas")
        st.markdown("## :green[**Overview :**] In this streamlit web app you can upload an image of a business card and extract relevant information from it using easyOCR. You can view, modify or delete the extracted data in this app. This app would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information.")
        st.markdown("## :blue[**Created by :**] ARUNRAJ R U")

# UPLOAD AND EXTRACT MENU
if selected == "Upload & Extract":
    st.markdown("### Upload a Business Card")
    uploaded_card = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

    if uploaded_card is not None:
        
        def save_card(uploaded_card):
            # Ensure the directory exists
            if not os.path.exists("uploaded_cards"):
                os.makedirs("uploaded_cards")
            with open(os.path.join("uploaded_cards", uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())   
        
        save_card(uploaded_card)
        
        def image_preview(image, res): 
            fig, ax = plt.subplots()  # Create a new figure and axes
            for (bbox, text, prob) in res: 
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            ax.axis('off')  # Hide the axes
            ax.imshow(image)  # Display the image on the axes
            return fig  # Return the figure
        
        # DISPLAYING THE UPLOADED CARD
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)
        # DISPLAYING THE CARD WITH HIGHLIGHTS
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(image_preview(image, res))  
                
        # easy OCR
        saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
        result = reader.readtext(saved_img, detail=0, paragraph=False)
        
        # CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
        def img_to_binary(file):
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData
        
        data = {"company_name": [],
                "card_holder": [],
                "designation": [],
                "mobile_number": [],
                "email": [],
                "website": [],
                "area": [],
                "city": [],
                "state": [],
                "pin_code": [],
                "image": [img_to_binary(saved_img)]  # Make sure this is a list
               }

        def get_data(res):
            for ind, i in enumerate(res):
                if "www " in i.lower() or "www." in i.lower():
                    data["website"].append(i)
                elif "WWW" in i:
                    data["website"] = res[4] + "." + res[5]
                elif "@" in i:
                    data["email"].append(i)
                elif "-" in i:
                    data["mobile_number"].append(i)
                    if len(data["mobile_number"]) == 2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])
                elif ind == len(res) - 1:
                    data["company_name"].append(i)
                elif ind == 0:
                    data["card_holder"].append(i)
                elif ind == 1:
                    data["designation"].append(i)
                if re.findall('^[0-9].+, [a-zA-Z]+', i):
                    data["area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+', i):
                    data["area"].append(i)
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*', i)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])
                state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                if state_match:
                    data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                    data["state"].append(i.split()[-1])
                if len(data["state"]) == 2:
                    data["state"].pop(0)
                if len(i) >= 6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                    data["pin_code"].append(i[10:])
        
        get_data(result)
        
        def create_df(data):
            # Check lengths of all lists
            lengths = {k: len(v) for k, v in data.items()}
            st.write(lengths)
            max_length = max(lengths.values())
            for key in data.keys():
                if len(data[key]) < max_length:
                    data[key] += [None] * (max_length - len(data[key]))
            
            df = pd.DataFrame(data)
            return df

        df = create_df(data)
        st.write("### Extracted Data:")
        st.write(df)
        
        # UPLOAD TO DATABASE
        if st.button("Upload to Database"):
            sql = """INSERT INTO card_data (company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, image)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (data["company_name"][0], data["card_holder"][0], data["designation"][0], data["mobile_number"][0], data["email"][0], data["website"][0], data["area"][0], data["city"][0], data["state"][0], data["pin_code"][0], img_to_binary(saved_img))
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Data Uploaded Successfully!")

# MODIFY MENU
if selected == "Modify":
    st.write("### Modify Data")
    sql_query = "SELECT * FROM card_data"
    df = pd.read_sql(sql_query, con=mydb)
    st.write(df)

    # Deleting records from the database
    delete_id = st.number_input("Enter the ID of the record to delete", min_value=1)
    if st.button("Delete Record"):
        mycursor.execute(f"DELETE FROM card_data WHERE id = {delete_id}")
        mydb.commit()
        st.success("Record Deleted Successfully!")

    # Updating records
    update_id = st.number_input("Enter the ID of the record to update", min_value=1)
    if st.button("Update Record"):
        # Fetch the current record
        mycursor.execute(f"SELECT * FROM card_data WHERE id = {update_id}")
        record = mycursor.fetchone()

        # Input fields for updating
        company_name = st.text_input("Company Name", value=record[1])
        card_holder = st.text_input("Card Holder", value=record[2])
        designation = st.text_input("Designation", value=record[3])
        mobile_number = st.text_input("Mobile Number", value=record[4])
        email = st.text_input("Email", value=record[5])
        website = st.text_input("Website", value=record[6])
        area = st.text_input("Area", value=record[7])
        city = st.text_input("City", value=record[8])
        state = st.text_input("State", value=record[9])
        pin_code = st.text_input("Pin Code", value=record[10])
        
        if st.button("Save Changes"):
            update_sql = """UPDATE card_data
                            SET company_name = %s, card_holder = %s, designation = %s, mobile_number = %s, email = %s, website = %s, area = %s, city = %s, state = %s, pin_code = %s
                            WHERE id = %s"""
            update_val = (company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, update_id)
            mycursor.execute(update_sql, update_val)
            mydb.commit()
            st.success("Record Updated Successfully!")

# CLOSE DATABASE CONNECTION
mydb.close()
