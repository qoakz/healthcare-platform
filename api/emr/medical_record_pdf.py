from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io

def generate_medical_record_pdf(medical_record, request=None):
    """Generate PDF for a complete medical record using ReportLab"""
    
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
        fontSize=20,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2563eb')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.HexColor('#374151'),
        backColor=colors.HexColor('#f3f4f6'),
        leftIndent=10,
        rightIndent=10,
        borderColor=colors.HexColor('#2563eb'),
        borderWidth=1,
        borderPadding=8
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    # Build the PDF content
    story = []
    
    # Header
    story.append(Paragraph("Healthcare Platform", title_style))
    story.append(Paragraph("123 Medical Center Drive | Healthcare City, HC 12345 | (555) 123-4567", 
                          ParagraphStyle('Address', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, textColor=colors.grey)))
    story.append(Spacer(1, 20))
    
    # Record ID
    record_id = str(medical_record.id)[:8].upper()
    story.append(Paragraph(f"Medical Record ID: {record_id}", 
                          ParagraphStyle('ID', parent=styles['Normal'], fontSize=10, alignment=TA_RIGHT, textColor=colors.grey)))
    story.append(Spacer(1, 20))
    
    # Title
    story.append(Paragraph("MEDICAL RECORD", 
                          ParagraphStyle('RecordTitle', parent=styles['Heading1'], fontSize=16, alignment=TA_CENTER, textColor=colors.HexColor('#1f2937'))))
    story.append(Spacer(1, 20))
    
    # Patient and Doctor Information
    info_data = [
        ['Patient', 'Doctor'],
        [f"Name: {medical_record.patient.get_full_name()}<br/>DOB: {medical_record.patient.date_of_birth.strftime('%B %d, %Y')}<br/>Gender: {medical_record.patient.get_gender_display()}<br/>Phone: {medical_record.patient.phone_number}", 
         f"Name: Dr. {medical_record.doctor.get_full_name()}<br/>Specialty: {medical_record.doctor.specialty}<br/>License: {medical_record.doctor.license_number}<br/>Date: {medical_record.created_at.strftime('%B %d, %Y')}"]
    ]
    
    info_table = Table(info_data, colWidths=[3*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 20))
    
    # Chief Complaint
    story.append(Paragraph("Chief Complaint", heading_style))
    story.append(Paragraph(medical_record.chief_complaint, normal_style))
    story.append(Spacer(1, 15))
    
    # History of Present Illness
    story.append(Paragraph("History of Present Illness", heading_style))
    story.append(Paragraph(medical_record.history_of_present_illness, normal_style))
    story.append(Spacer(1, 15))
    
    # Past Medical History
    if medical_record.past_medical_history:
        story.append(Paragraph("Past Medical History", heading_style))
        story.append(Paragraph(medical_record.past_medical_history, normal_style))
        story.append(Spacer(1, 15))
    
    # Family History
    if medical_record.family_history:
        story.append(Paragraph("Family History", heading_style))
        story.append(Paragraph(medical_record.family_history, normal_style))
        story.append(Spacer(1, 15))
    
    # Social History
    if medical_record.social_history:
        story.append(Paragraph("Social History", heading_style))
        story.append(Paragraph(medical_record.social_history, normal_style))
        story.append(Spacer(1, 15))
    
    # Vital Signs
    vital_signs = medical_record.record_vital_signs.all()
    if vital_signs:
        story.append(Paragraph("Vital Signs", heading_style))
        
        vital_data = [['Measurement', 'Value', 'Unit']]
        for vital in vital_signs:
            if vital.blood_pressure_systolic:
                vital_data.append(['Blood Pressure', f"{vital.blood_pressure_systolic}/{vital.blood_pressure_diastolic}", 'mmHg'])
            if vital.heart_rate:
                vital_data.append(['Heart Rate', str(vital.heart_rate), 'bpm'])
            if vital.temperature:
                vital_data.append(['Temperature', str(vital.temperature), '°F'])
            if vital.respiratory_rate:
                vital_data.append(['Respiratory Rate', str(vital.respiratory_rate), '/min'])
            if vital.oxygen_saturation:
                vital_data.append(['Oxygen Saturation', str(vital.oxygen_saturation), '%'])
            if vital.weight:
                vital_data.append(['Weight', str(vital.weight), 'kg'])
            if vital.height:
                vital_data.append(['Height', str(vital.height), 'cm'])
            if vital.bmi:
                vital_data.append(['BMI', str(vital.bmi), ''])
        
        if len(vital_data) > 1:  # More than just header
            vital_table = Table(vital_data, colWidths=[2*inch, 1.5*inch, 1*inch])
            vital_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
            ]))
            story.append(vital_table)
        
        story.append(Spacer(1, 15))
    
    # Physical Examination
    story.append(Paragraph("Physical Examination", heading_style))
    story.append(Paragraph(medical_record.physical_examination, normal_style))
    story.append(Spacer(1, 15))
    
    # Diagnosis
    story.append(Paragraph("Diagnosis", heading_style))
    story.append(Paragraph(medical_record.diagnosis, normal_style))
    story.append(Spacer(1, 15))
    
    # Treatment Plan
    story.append(Paragraph("Treatment Plan", heading_style))
    story.append(Paragraph(medical_record.treatment_plan, normal_style))
    story.append(Spacer(1, 15))
    
    # Prescriptions
    prescriptions = medical_record.prescriptions.all()
    if prescriptions:
        story.append(Paragraph("Prescriptions", heading_style))
        for prescription in prescriptions:
            story.append(Paragraph(f"<b>{prescription.medication_name}</b> - {prescription.dosage} - {prescription.frequency} - {prescription.duration}", 
                                  ParagraphStyle('Prescription', parent=styles['Normal'], fontSize=10, 
                                               leftIndent=20, backColor=colors.HexColor('#fefce8'), 
                                               borderColor=colors.HexColor('#d1d5db'), borderWidth=1, 
                                               borderPadding=8)))
            if prescription.instructions:
                story.append(Paragraph(f"Instructions: {prescription.instructions}", 
                                      ParagraphStyle('Instructions', parent=styles['Normal'], fontSize=9, 
                                                   leftIndent=40, textColor=colors.HexColor('#6b7280'))))
        story.append(Spacer(1, 15))
    
    # Lab Results
    lab_results = medical_record.lab_results.all()
    if lab_results:
        story.append(Paragraph("Lab Results", heading_style))
        for lab_result in lab_results:
            story.append(Paragraph(f"<b>{lab_result.test_name}</b> - {lab_result.test_type} - {lab_result.test_date.strftime('%B %d, %Y')}", 
                                  ParagraphStyle('LabResult', parent=styles['Normal'], fontSize=10, 
                                               leftIndent=20, backColor=colors.HexColor('#f0f9ff'), 
                                               borderColor=colors.HexColor('#d1d5db'), borderWidth=1, 
                                               borderPadding=8)))
            if lab_result.interpretation:
                story.append(Paragraph(f"Interpretation: {lab_result.interpretation}", 
                                      ParagraphStyle('Interpretation', parent=styles['Normal'], fontSize=9, 
                                                   leftIndent=40, textColor=colors.HexColor('#6b7280'))))
        story.append(Spacer(1, 15))
    
    # Additional Notes
    if medical_record.notes:
        story.append(Paragraph("Additional Notes", heading_style))
        story.append(Paragraph(medical_record.notes, normal_style))
        story.append(Spacer(1, 15))
    
    # Follow-up
    if medical_record.follow_up_required:
        story.append(Paragraph("Follow-up", heading_style))
        story.append(Paragraph("Follow-up required: Yes", normal_style))
        if medical_record.follow_up_date:
            story.append(Paragraph(f"Follow-up date: {medical_record.follow_up_date.strftime('%B %d, %Y')}", normal_style))
        story.append(Spacer(1, 15))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"This medical record was generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
    story.append(Paragraph(f"Record ID: {record_id}", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
    story.append(Paragraph("For questions or concerns, please contact your healthcare provider.", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
    
    # Build PDF
    doc.build(story)
    
    # Get the PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
