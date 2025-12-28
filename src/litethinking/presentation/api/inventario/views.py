from datetime import datetime
from io import BytesIO
import threading
import re

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ....application.use_cases.empresa_use_cases import ObtenerEmpresaUseCase
from ....application.use_cases.producto_use_cases import ListarProductosUseCase
from ....infrastructure.persistence.empresa.repository_impl import DjangoEmpresaRepository
from ....infrastructure.persistence.producto.repository_impl import DjangoProductoRepository

empresa_repository = DjangoEmpresaRepository()
producto_repository = DjangoProductoRepository()


def _validar_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def _enviar_pdf_por_correo(pdf_content: bytes, empresa_nit: str, empresa_nombre: str, email_destino: str, fecha_generacion: str):

    try:
        email_from = settings.DEFAULT_FROM_EMAIL
        if not email_from or not email_from.strip():
            raise ValueError(
                "La configuración de email no está completa. "
                "Por favor, configure EMAIL_HOST_USER o DEFAULT_FROM_EMAIL en las variables de entorno."
            )
        
        filename = f'inventario_{empresa_nit}_{fecha_generacion}.pdf'
        
        email = EmailMessage(
            subject=f'Inventario de Productos - {empresa_nombre}',
            body=f'''
                Estimado/a,

                Adjunto encontrará el reporte de inventario de productos de la empresa {empresa_nombre}.

                Fecha de generación: {fecha_generacion}

                Este es un correo automático, por favor no responda.

                Saludos cordiales,
                Sistema LiteThinking
            ''',
            from_email=email_from,
            to=[email_destino],
        )
        
        email.attach(filename, pdf_content, 'application/pdf')
        email.send()
        
    except Exception as e:
        print(f"Error al enviar correo a {email_destino}: {str(e)}")


def _generar_pdf_inventario(empresa, productos, fecha_generacion_formateada: str) -> bytes:

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1,  # Centrado
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
    )
    normal_style = styles['Normal']
    
    elements.append(Paragraph("Vista de Inventario", title_style))
    elements.append(Spacer(1, 0.2 * inch))
    
    elements.append(Paragraph(f"<b>Empresa:</b> {empresa.nombre}", heading_style))
    elements.append(Paragraph(f"<b>NIT:</b> {empresa.nit}", normal_style))
    elements.append(Paragraph(f"<b>Dirección:</b> {empresa.direccion}", normal_style))
    elements.append(Paragraph(f"<b>Teléfono:</b> {empresa.telefono}", normal_style))
    elements.append(Paragraph(
        f"<b>Fecha de generación:</b> {fecha_generacion_formateada}",
        normal_style
    ))
    elements.append(Spacer(1, 0.3 * inch))
    
    if productos:
        data = [['Código', 'Nombre', 'Características', 'Precios']]
        
        for producto in productos:
            precios_texto = []
            if producto.precios:
                for precio in producto.precios:
                    valor_formateado = f"{precio.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    precios_texto.append(f"{precio.moneda.value}: {valor_formateado}")
                precios_str = "<br/>".join(precios_texto)
            else:
                precios_str = "Sin precios"
            
            caracteristicas = producto.caracteristicas or "N/A"
            if len(caracteristicas) > 50:
                caracteristicas = caracteristicas[:47] + "..."
            
            data.append([
                producto.codigo,
                producto.nombre,
                caracteristicas,
                Paragraph(precios_str, normal_style)
            ])
        
        table = Table(data, colWidths=[1.2 * inch, 2.5 * inch, 2.5 * inch, 1.8 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(
            f"<b>Total de productos:</b> {len(productos)}",
            normal_style
        ))
    else:
        elements.append(Paragraph(
            "<i>No hay productos registrados para esta empresa.</i>",
            normal_style
        ))
    
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generar_inventario_pdf(request, empresa_nit):

    try:
        email_destino = request.query_params.get('email', '').strip()
        enviar_por_correo = bool(email_destino)
        
        if enviar_por_correo:
            if not _validar_email(email_destino):
                return Response(
                    {'error': 'El formato del correo electrónico no es válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        empresa_use_case = ObtenerEmpresaUseCase(empresa_repository)
        empresa = empresa_use_case.ejecutar(empresa_nit)
        
        if not empresa:
            return Response(
                {'error': f'No existe una empresa con el NIT: {empresa_nit}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        producto_use_case = ListarProductosUseCase(producto_repository)
        productos = producto_use_case.ejecutar(empresa_nit=empresa_nit)
        
        fecha_generacion = datetime.now().strftime('%Y%m%d_%H%M%S')
        fecha_generacion_formateada = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        pdf = _generar_pdf_inventario(empresa, productos, fecha_generacion_formateada)
        
        if enviar_por_correo:
            thread = threading.Thread(
                target=_enviar_pdf_por_correo,
                args=(pdf, empresa_nit, empresa.nombre, email_destino, fecha_generacion),
                daemon=True
            )
            thread.start()
            
            return Response(
                {
                    'message': f'El archivo PDF se está enviando a {email_destino}',
                    'empresa_nit': empresa_nit,
                    'empresa_nombre': empresa.nombre,
                    'email_destino': email_destino,
                    'total_productos': len(productos),
                    'fecha_generacion': fecha_generacion_formateada
                },
                status=status.HTTP_200_OK
            )
        else:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f'inventario_{empresa.nit}_{fecha_generacion}.pdf'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
    except Exception as e:
        return Response(
            {'error': f'Error al generar el PDF: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

