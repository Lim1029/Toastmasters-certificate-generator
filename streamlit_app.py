from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import zlib
import zipfile
import os

pdfmetrics.registerFont(TTFont('MontserratB', 'Montserrat-Bold.ttf'))
pdfmetrics.registerFont(TTFont('MontserratEB', 'Montserrat-ExtraBold.ttf'))
pdfmetrics.registerFont(TTFont('MontserratBK', 'Montserrat-Black.ttf'))
pdfmetrics.registerFont(TTFont('MontserratR', 'Montserrat-Regular.ttf'))

pdfmetrics.registerFont(TTFont('Allison', 'Allison-Regular.ttf'))


# pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
# pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
# pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

"""
# Toastmasters Certificate Generator

Generate Certificates to Appreciate Guests

Welcome to the Toastmasters Certificate Generator! I'm Ming Kang, a Toastmasters member since 2020 and a university student passionate about coding and video editing. I've created this website to help you easily generate PDF certificates for your club's guests.

## Features
- Generate multiple participation certificates at once.
- Future development: Award certificates and GE appreciation certificates, automated email delivery to recipients, multiline texts

## How to Use
1. Enter participant names, one per line.
2. Provide event details and issuer information.
3. Click "Generate."
4. Review certificate images.
5. Adjust text and font size if needed, then click "Generate" again.
6. Download certificates in two ways:

    a) If you prefer JPEG format, simply right-click or long-tap the certificate shown to save.
    
    b) A "download" button shall appear; click to download in PDF format in a zip file.

Your support is appreciated! Consider donating to support a university student and Toastmasters member working to enhance our community.

Feel free to contact me at mk1029@hotmail.com for inquiries or suggestions.

"""

with st.expander("Donate to the author"):
    st.write("If you are a malaysian, please transfer the donation to my TnG Wallet or DuitNow. If you are a non-Malaysian, please email me so we can discuss ways to do it.")

    st.image("myqr.png")

def generate_response(input_text):
    st.info(input_text+"dasda")

def compress(file_names):
    print("File Paths:")
    print(file_names)

    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED

    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile("cert.zip", mode="w")
    try:
        for file_name in file_names:
            # Add file to the zip file
            # first parameter file to zip, second filename in zip
            zf.write(file_name, file_name, compress_type=compression)

    except FileNotFoundError:
        print("An error occurred")
    finally:
        # Don't forget to close the file!
        zf.close()

def generate_participation_cert(name_list,event_name,date,venue,issuer,issuer_title,signature,
                                size_name_list,size_event,size_date_venue):
    filelist = []
    for name in name_list.split('\n'):
        packet = io.BytesIO()
        # Create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=(A4[1], A4[0]))
        can.setFont('MontserratEB', size_name_list)
        can.drawCentredString(550, 325, name.upper())

        can.setFont('MontserratB', size_event)
        can.drawCentredString(550, 235, event_name)

        can.setFont('MontserratR', size_date_venue)
        can.drawCentredString(550, 185, f'on {date} at {venue}')

        can.setFont('MontserratR', 20)
        can.drawCentredString(380, 70, date)

        can.setFont('Allison', 40)
        can.drawCentredString(722, 70, signature)

        can.setFont('MontserratR', 15)
        can.drawCentredString(722, 33, f"{issuer}")
        can.drawCentredString(722, 13, f"{issuer_title}")

        can.showPage()
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        # Read your existing PDF
        existing_pdf = PdfReader(open("Toastmasters Cert.pdf", "rb"))
        output = PdfWriter()
        # Add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        # Finally, write "output" to a real file
        outputStream = open(f"participation_{name}.pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        filelist.append(f"participation_{name}.pdf")
        # with open(f"participation_{name}.pdf",'rb') as cert:
        image = convert_from_path(f"participation_{name}.pdf")
        st.image(image)
        
    compress(filelist)

def generate_appreciation_cert(name_list,event_name,date,venue,issuer,issuer_title,signature,
                                size_name_list,size_event,size_date_venue):
    filelist = []
    for name in name_list.split('\n'):
        packet = io.BytesIO()
        # Create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=(A4[1], A4[0]))
        can.setFont('MontserratEB', size_name_list)
        can.drawCentredString(550, 325, name.upper())

        can.setFont('MontserratB', size_event)
        can.drawCentredString(550, 235, event_name)

        can.setFont('MontserratR', size_date_venue)
        can.drawCentredString(550, 185, f'on {date} at {venue}')

        can.setFont('MontserratR', 20)
        can.drawCentredString(380, 70, date)

        can.setFont('Allison', 40)
        can.drawCentredString(722, 70, signature)

        can.setFont('MontserratR', 15)
        can.drawCentredString(722, 33, f"{issuer}")
        can.drawCentredString(722, 13, f"{issuer_title}")

        can.showPage()
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        # Read your existing PDF
        existing_pdf = PdfReader(open("Appreciation Cert.pdf", "rb"))
        output = PdfWriter()
        # Add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        # Finally, write "output" to a real file
        outputStream = open(f"participation_{name}.pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        filelist.append(f"participation_{name}.pdf")
        # with open(f"participation_{name}.pdf",'rb') as cert:
        image = convert_from_path(f"participation_{name}.pdf")
        st.image(image)
        
    compress(filelist)

def generate_award_cert(name_best_TT,name_best_speech,name_best_evaluator,club_name,date,issuer,
                                size_name_list,size_club_name):
    filelist = []
    for name in name_best_TT.split('\n'):
        packet = io.BytesIO()
        # Create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=(A4[1], A4[0]))
        can.setFont('MontserratEB', size_name_list)
        can.drawCentredString(540, 300, name.upper())

        can.setFont('MontserratB', size_club_name)
        can.drawCentredString(540, 200, club_name)

        can.setFont('MontserratR', 20)
        can.drawCentredString(415, 80, date)

        can.setFont('MontserratR', 20)
        can.drawCentredString(660, 80, issuer)

        can.showPage()
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        # Read your existing PDF
        existing_pdf = PdfReader(open("cert_best_tt.pdf", "rb"))
        output = PdfWriter()
        # Add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        # Finally, write "output" to a real file
        filename = f"bestTT_{name}.pdf"
        outputStream = open(filename, "wb")
        output.write(outputStream)
        outputStream.close()
        filelist.append(filename)
        # with open(f"participation_{name}.pdf",'rb') as cert:
        image = convert_from_path(filename)
        st.image(image)
    for name in name_best_speech.split('\n'):
        packet = io.BytesIO()
        # Create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=(A4[1], A4[0]))
        can.setFont('MontserratEB', size_name_list)
        can.drawCentredString(540, 300, name.upper())

        can.setFont('MontserratB', size_club_name)
        can.drawCentredString(540, 200, club_name)

        can.setFont('MontserratR', 20)
        can.drawCentredString(415, 80, date)

        can.setFont('MontserratR', 20)
        can.drawCentredString(660, 80, issuer)

        can.showPage()
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        # Read your existing PDF
        existing_pdf = PdfReader(open("cert_best_speaker.pdf", "rb"))
        output = PdfWriter()
        # Add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        # Finally, write "output" to a real file
        filename = f"bestSpeaker_{name}.pdf"
        outputStream = open(filename, "wb")
        output.write(outputStream)
        outputStream.close()
        filelist.append(filename)
        # with open(f"participation_{name}.pdf",'rb') as cert:
        image = convert_from_path(filename)
        st.image(image)
    for name in name_best_evaluator.split('\n'):
        packet = io.BytesIO()
        # Create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=(A4[1], A4[0]))
        can.setFont('MontserratEB', size_name_list)
        can.drawCentredString(540, 300, name.upper())

        can.setFont('MontserratB', size_club_name)
        can.drawCentredString(540, 200, club_name)

        can.setFont('MontserratR', 20)
        can.drawCentredString(415, 80, date)

        can.setFont('MontserratR', 20)
        can.drawCentredString(660, 80, issuer)

        can.showPage()
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        # Read your existing PDF
        existing_pdf = PdfReader(open("cert_best_evaluator.pdf", "rb"))
        output = PdfWriter()
        # Add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        # Finally, write "output" to a real file
        filename = f"bestEvaluator_{name}.pdf"
        outputStream = open(filename, "wb")
        output.write(outputStream)
        outputStream.close()
        filelist.append(filename)
        # with open(f"participation_{name}.pdf",'rb') as cert:
        image = convert_from_path(filename)
        st.image(image)

    compress(filelist)

tab1, tab2, tab3 = st.tabs(["Participation", "Awards", "Appreciation"]) 

with tab1:
    with st.form('my_form_participation'):
        name_list = st.text_area('Enter names, separated by line:', 'Ali\nAh Kau\nMuthu')
        size_name_list = st.slider('Name Font size?', 0, 80, 40)
        event_name = st.text_area('Enter event name:', 'Malaysia Toastmasters Meeting 366')
        size_event = st.slider('Event Font size?', 0, 80, 30)
        date = st.text_area('Enter date:', '27 Sep 2023')
        venue = st.text_area('Enter venue:', 'Zoom (Online)')
        size_date_venue = st.slider('Date Venue Font size?', 0, 80, 30)
        issuer = st.text_area('Enter issuer:', 'Michael Jay')
        issuer_title = st.text_area('Enter issuer_title:', 'President')
        signature = st.text_area('Enter signature name:', 'Michael')
        submitted = st.form_submit_button('Submit')

        if submitted:
            generate_participation_cert(name_list,event_name,date,venue,issuer,issuer_title,signature,
                                        size_name_list,size_event,size_date_venue)
    if "cert.zip" in os.listdir() and submitted:
        with open("cert.zip", "rb") as fp:
            btn = st.download_button(
                label="Download Cert",
                data=fp,
                file_name="cert.zip"
            )
with tab2:
    with st.form('my_form_award'):
        name_best_TT = st.text_area('Enter names of best table topics speaker(s), separated by line:', 'Sithi\nMei Ling')
        name_best_speech = st.text_area('Enter names of best speaker(s), separated by line:', 'Jenny\nHui Xin')
        name_best_evaluator = st.text_area('Enter names best evaluator(s), separated by line:', 'Chris\nRyan')
        size_name_list = st.slider('Name Font size?', 0, 80, 30)
        club_name = st.text_area('Enter club name:', 'Malaysia Toastmasters Club')
        size_club_name = st.slider('Club Name Font size?', 0, 80, 20)
        date = st.text_area('Enter date:', '27 Sep 2023')
        venue = st.text_area('Enter venue:', 'Zoom (Online)')
        size_date_venue = st.slider('Date Venue Font size?', 0, 80, 30)
        issuer = st.text_area('Enter issuer:', 'Michael Jay')
        submitted = st.form_submit_button('Submit Award Form')

        if submitted:
            generate_award_cert(name_best_TT,name_best_speech,name_best_evaluator,club_name,date,issuer,
                                size_name_list,size_club_name)

    if "cert.zip" in os.listdir() and submitted:
        with open("cert.zip", "rb") as fp:
            btn = st.download_button(
                label="Download Cert",
                data=fp,
                file_name="cert.zip"
            )

with tab3:
    with st.form('my_form_appreciation'):
        name_list = st.text_area('Enter names, separated by line:', 'Ali\nAh Kau\nMuthu')
        size_name_list = st.slider('Name Font size?', 0, 80, 40)
        event_name = st.text_area('Enter event name:', 'Malaysia Toastmasters Meeting 366')
        size_event = st.slider('Event Font size?', 0, 80, 30)
        date = st.text_area('Enter date:', '27 Sep 2023')
        venue = st.text_area('Enter venue:', 'Zoom (Online)')
        size_date_venue = st.slider('Date Venue Font size?', 0, 80, 30)
        issuer = st.text_area('Enter issuer:', 'Michael Jay')
        issuer_title = st.text_area('Enter issuer_title:', 'President')
        signature = st.text_area('Enter signature name:', 'Michael')
        submitted = st.form_submit_button('Submit')

        if submitted:
            generate_appreciation_cert(name_list,event_name,date,venue,issuer,issuer_title,signature,
                                        size_name_list,size_event,size_date_venue)
    if "cert.zip" in os.listdir() and submitted:
        with open("cert.zip", "rb") as fp:
            btn = st.download_button(
                label="Download Cert",
                data=fp,
                file_name="cert.zip"
            )