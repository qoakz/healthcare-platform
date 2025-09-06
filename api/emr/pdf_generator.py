from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import uuid
import io

def generate_prescription_pdf(prescription, request=None):
    """Generate PDF for a prescription using ReportLab"""
    
    # Create a BytesIO buffer to store the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Define custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2563eb')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#374151')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6
    )
    
    # Build the PDF content
    story = []
    
    # Header
    story.append(Paragraph("Healthcare Platform", title_style))
    story.append(Paragraph("123 Medical Center Drive<br/>Healthcare City, HC 12345<br/>Phone: (555) 123-4567 | Email: info@healthcareplatform.com", 
                          ParagraphStyle('Address', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, textColor=colors.grey)))
    story.append(Spacer(1, 20))
    
    # Prescription ID
    prescription_id = str(prescription.id)[:8].upper()
    story.append(Paragraph(f"Prescription ID: {prescription_id}", 
                          ParagraphStyle('ID', parent=styles['Normal'], fontSize=10, alignment=TA_RIGHT, textColor=colors.grey)))
    story.append(Spacer(1, 20))
    
    # Title
    story.append(Paragraph("PRESCRIPTION", 
                          ParagraphStyle('PrescriptionTitle', parent=styles['Heading1'], fontSize=18, alignment=TA_CENTER, textColor=colors.HexColor('#1f2937'))))
    story.append(Spacer(1, 20))
    
    # Patient and Doctor Information Table
    patient_doctor_data = [
        ['Patient Information', 'Prescribing Doctor'],
        [f"Name: {prescription.patient.get_full_name()}<br/>DOB: {prescription.patient.date_of_birth.strftime('%B %d, %Y')}<br/>Gender: {prescription.patient.get_gender_display()}<br/>Phone: {prescription.patient.phone_number}", 
         f"Name: Dr. {prescription.doctor.get_full_name()}<br/>Specialty: {prescription.doctor.specialty}<br/>License: {prescription.doctor.license_number}<br/>Date: {prescription.created_at.strftime('%B %d, %Y')}"]
    ]
    
    patient_doctor_table = Table(patient_doctor_data, colWidths=[3*inch, 3*inch])
    patient_doctor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
    ]))
    
    story.append(patient_doctor_table)
    story.append(Spacer(1, 20))
    
    # Medication Details
    story.append(Paragraph("Medication Details", heading_style))
    
    medication_data = [
        ['Medication Name', prescription.medication_name],
        ['Generic Name', prescription.generic_name or 'N/A'],
        ['Dosage', prescription.dosage],
        ['Frequency', prescription.frequency],
        ['Duration', prescription.duration],
        ['Quantity', str(prescription.quantity)],
        ['Refills Allowed', str(prescription.refills_allowed)],
        ['Status', prescription.get_status_display()],
    ]
    
    if prescription.expiry_date:
        medication_data.append(['Expiry Date', prescription.expiry_date.strftime('%B %d, %Y')])
    
    medication_table = Table(medication_data, colWidths=[2*inch, 4*inch])
    medication_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(medication_table)
    story.append(Spacer(1, 15))
    
    # Instructions
    if prescription.instructions:
        story.append(Paragraph("Instructions", 
                              ParagraphStyle('InstructionsTitle', parent=styles['Heading3'], fontSize=14, textColor=colors.HexColor('#92400e'))))
        story.append(Paragraph(prescription.instructions, 
                              ParagraphStyle('Instructions', parent=styles['Normal'], fontSize=11, 
                                           leftIndent=20, backColor=colors.HexColor('#fef3c7'), 
                                           borderColor=colors.HexColor('#f59e0b'), borderWidth=1, 
                                           borderPadding=10)))
        story.append(Spacer(1, 15))
    
    # Diagnosis
    if prescription.medical_record and prescription.medical_record.diagnosis:
        story.append(Paragraph("Diagnosis", heading_style))
        story.append(Paragraph(prescription.medical_record.diagnosis, normal_style))
        story.append(Spacer(1, 15))
    
    # Signature Section
    story.append(Spacer(1, 30))
    signature_data = [
        ['Doctor\'s Signature', 'Date'],
        ['', '']
    ]
    
    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
    signature_table.setStyle(TableStyle([
        ('LINEBELOW', (0, 1), (0, 1), 1, colors.black),
        ('LINEBELOW', (1, 1), (1, 1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 1), (-1, 1), 20),
    ]))
    
    story.append(signature_table)
    story.append(Spacer(1, 30))
    
    # Footer
    story.append(Paragraph("This prescription is valid for 30 days from the date of issue.", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
    story.append(Paragraph("For questions, contact your healthcare provider.", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
    
    # Build PDF
    doc.build(story)
    
    # Get the PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def generate_medical_record_pdf(medical_record, request=None):
    """Generate PDF for a complete medical record"""
    
    # Prepare context data
    context = {
        'medical_record': medical_record,
        'patient': medical_record.patient,
        'doctor': medical_record.doctor,
        'prescriptions': medical_record.prescriptions.all(),
        'lab_results': medical_record.lab_results.all(),
        'vital_signs': medical_record.vital_signs.all(),
        'generated_at': datetime.now(),
        'record_id': str(medical_record.id)[:8].upper(),
        'logo_url': request.build_absolute_uri('/static/images/logo.png') if request else None,
    }
    
    # Render HTML template
    html_string = render_to_string('emr/medical_record_pdf.html', context)
    
    # CSS for styling
    css_string = """
    @page {
        size: A4;
        margin: 1cm;
    }
    
    body {
        font-family: 'Arial', sans-serif;
        font-size: 11px;
        line-height: 1.4;
        color: #333;
    }
    
    .header {
        text-align: center;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    .clinic-name {
        font-size: 20px;
        font-weight: bold;
        color: #2563eb;
        margin-bottom: 5px;
    }
    
    .record-title {
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        margin: 15px 0;
        color: #1f2937;
    }
    
    .section {
        margin-bottom: 20px;
        page-break-inside: avoid;
    }
    
    .section-title {
        font-size: 14px;
        font-weight: bold;
        color: #374151;
        background-color: #f3f4f6;
        padding: 8px 12px;
        border-left: 4px solid #2563eb;
        margin-bottom: 10px;
    }
    
    .section-content {
        padding: 10px;
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 3px;
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-bottom: 15px;
    }
    
    .info-item {
        display: flex;
        margin-bottom: 5px;
    }
    
    .info-label {
        font-weight: bold;
        width: 100px;
        color: #4b5563;
    }
    
    .info-value {
        flex: 1;
    }
    
    .vital-signs-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-bottom: 10px;
    }
    
    .vital-item {
        text-align: center;
        padding: 8px;
        background-color: #f8fafc;
        border-radius: 3px;
    }
    
    .vital-label {
        font-size: 10px;
        color: #6b7280;
        margin-bottom: 2px;
    }
    
    .vital-value {
        font-size: 14px;
        font-weight: bold;
        color: #1f2937;
    }
    
    .prescription-item {
        margin-bottom: 15px;
        padding: 10px;
        border: 1px solid #d1d5db;
        border-radius: 3px;
        background-color: #fefce8;
    }
    
    .medication-name {
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 5px;
    }
    
    .medication-details {
        font-size: 10px;
        color: #6b7280;
    }
    
    .lab-result-item {
        margin-bottom: 10px;
        padding: 8px;
        border: 1px solid #d1d5db;
        border-radius: 3px;
        background-color: #f0f9ff;
    }
    
    .test-name {
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 3px;
    }
    
    .test-details {
        font-size: 10px;
        color: #6b7280;
    }
    
    .footer {
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #d1d5db;
        text-align: center;
        font-size: 9px;
        color: #6b7280;
    }
    """
    
    # Generate PDF
    font_config = FontConfiguration()
    html_doc = HTML(string=html_string)
    css_doc = CSS(string=css_string, font_config=font_config)
    
    pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc], font_config=font_config)
    
    return pdf_bytes

def generate_prescription_response(prescription, filename=None):
    """Generate HTTP response for prescription PDF"""
    if not filename:
        filename = f"prescription_{prescription.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    pdf_bytes = generate_prescription_pdf(prescription)
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

def generate_medical_record_response(medical_record, filename=None):
    """Generate HTTP response for medical record PDF"""
    if not filename:
        filename = f"medical_record_{medical_record.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    pdf_bytes = generate_medical_record_pdf(medical_record)
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
