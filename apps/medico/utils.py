import os
from django.conf import settings
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView
from django.core.exceptions import ImproperlyConfigured
import xmltodict
import json
from xml.parsers.expat import ExpatError
import zipfile
from tenacity import *
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .qs_group import agrupar_queryset
from collections import OrderedDict
import uuid


class AjaxListView(ListView):
    """CBV que permite paginacion con ajax de una lista de objetos."""

    paginate_grid = False

    def get_context_data(self, **kwargs):
        """
        Agrega la variable 'template_paginacion' en el contexto
        """
        context = super(AjaxListView, self).get_context_data(**kwargs)
        t_grid = self.template_pagination_grid
        t_list = self.template_pagination_list

        if t_grid is None and t_list is None:
            raise ImproperlyConfigured(
                'AjaxListView requiere una plantilla para la paginacion'
            )
        return context

    def get_template_names(self):
        """
        Cambia la plantilla para peticiones AJAX.
        """
        request = self.request
        t_grid = self.template_pagination_grid
        t_list = self.template_pagination_list

        try:
            t_agrupacion = self.template_agrupacion_list
        except Exception:
            t_agrupacion = None

        if request.is_ajax():
            self.paginate_grid = request.GET.get('view') == 'grid'
            if 'agrupacion' in request.GET:
                return t_agrupacion
            elif self.paginate_grid:
                return t_grid
            else:
                return t_list
        return super(AjaxListView, self).get_template_names()


def obtener_queryset_paginado(pagina, qs_paginacion, paginar_por):
    """

    :param pagina: Numero de pagina de la paginacion. ej: 1
    :param qs_paginacion: Queryset de items a paginar
    :param paginar_por: Cantidad de items por pagina a mostrar
    :return: Retorna el queryset paginado
    """
    try:
        paginar_por = int(paginar_por)
    except (ValueError, TypeError):
        paginar_por = settings.PAGINATE_BY

    paginador = Paginator(qs_paginacion, paginar_por)

    try:
        qs_paginacion = paginador.page(pagina)
    except PageNotAnInteger:
        qs_paginacion = paginador.page(1)
    except EmptyPage:
        qs_paginacion = paginador.page(paginador.num_pages)

    return qs_paginacion


def limpiar_filtros(filtros):
    """
    Convierte un diccionario key value a objetos de busqueda de un modelo
    :param filtros: [{'key':'estado', 'value':'BORRADOR'}]
    :return: Q(estado__icontains=BORRADOR)
    """

    filtros = json.loads(filtros) if filtros else []
    criteria = None
    campos_busqueda = []

    q_data = Q()

    if len(filtros) > 0:
        has_filter_all = filter(lambda obj: obj.get('key') == 'filter_all', filtros)

        has_filter_all = list(has_filter_all)

        if len(has_filter_all) > 0:
            criteria = has_filter_all[0].get('value')
        else:

            for filtro in filtros:

                if 'key' in filtro and 'value' in filtro:
                    if filtro['value'].upper() == 'SI':
                        filtro['value'] = 'true'
                    elif filtro['value'].upper() == 'NO':
                        filtro['value'] = 'false'

                    item = preparar_campo_filtro(filtro)

                    if not item:
                        continue

                    operador_or = es_grupal(filtros, item) > 1

                    f_value = Q(**{item.get('key'): item.get('value')})

                    if item.get('excluir'):
                        f_value = ~f_value

                    if operador_or:
                        q_data |= f_value
                    else:
                        q_data &= f_value

    return q_data, criteria


from .constantes import (
    FILTRO_EXCLUYE, PARAMETROS_FILTRO, BOOLEAN_FILTRO
)
def preparar_campo_filtro(item):

    filtroa = item.get('filter')
    campo = item.get('key')

    if filtroa is None or filtroa == '' or campo is None or campo == '':
        return False

    # verificar si existe en las opciones
    filtro = PARAMETROS_FILTRO.get(filtroa, None)

    if filtro is None:
        return False

    campo = item.get('key')
    if campo is None or campo == '':
        return False

    valor = item.get('value')

    key_format =  '{0}{1}'.format(campo, filtro)
    if filtroa in BOOLEAN_FILTRO:
        key_format = campo
        valor = filtro

    return {
        'key': key_format,
        'value': valor,
        'excluir': filtroa in FILTRO_EXCLUYE,
        'group': item.get('group')
    }


def es_grupal(items, item):

    return len([x for x in items if x.get('group') == item.get('group')])


def _finditem(obj, key, default=None):
    """Buscar recursivamente un objecto dada la clava en un diccionario"""
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = _finditem(v, key)
            if item is not None:
                return item

    return default


def xml_headers(xml):
    """
    Selecciona el root (comprobante: <comprobante> </comprobante>) del xml según el diseño del mismo.
    :param xml: Archivo xml
    :return: bytes results
    """

    try:
        data = xmltodict.parse(xml, encoding='utf-8')

        xml_tmp = _finditem(data, 'comprobante')
        numero_autorizacion = _finditem(data, 'numeroAutorizacion', '-----')
        fecha_autorizacion = _finditem(data, 'fechaAutorizacion', '-----')
        estado = _finditem(data, 'estado', '')

        if xml_tmp is None:
            xml_tmp = data

        result = {
            'xml': xml_tmp,
            'estado': estado,
            'fechaAutorizacion': fecha_autorizacion,
            'numeroAutorizacion': numero_autorizacion
        }
    except ExpatError as error:
        print("Error=> %s" % error)
    else:
        return result


def get_data_from_xml(xml):
    data = xmltodict.parse(xml)
    return data


def read_zipfile(zip):
    """
    Función que parsea una xml dentro de un archivo zip.
    :param zip: Archivo zip
    :return: Retorna un json con los datos del xml
    """
    vouchers = []
    count = 0
    success = 0
    errors = []
    if zipfile.is_zipfile(zip):
        content = zipfile.ZipFile(zip, 'r')
        # De la lista de nombres de archivos dentro del zip, buscar el que sea con extension .xml
        # obteniendo el index del acchivo se procede a leerlo directamente a.read(index)
        # se obtiene un b'datos del xml', que es lo que se le pasa al parseador de xml.
        for file in content.namelist():
            count += 1
            if file.endswith('.xml') or file.endswith('.XML'):
                xml = xml_headers(content.read(file).decode("iso-8859-1"))
                if xml:
                    try:
                        voucher = get_data_from_xml(xml.get('xml'))
                        clean_data = {
                            'numeroAutorizacion':  xml.get('numeroAutorizacion'),
                            'estado': xml.get('estado'),
                            'fechaAutorizacion': xml.get('fechaAutorizacion'),
                            'infoTributaria': voucher.get('factura').get('infoTributaria'),
                            'infoFactura': voucher.get('factura').get('infoFactura'),
                            'detalles': voucher.get('factura').get('detalles'),
                            'infoAdicional': voucher.get('factura').get('infoAdicional'),
                        }
                        vouchers.append(clean_data)
                    except Exception as exc:
                        errors.append(
                            "Error parseando el archivo %s. Error=> %s" % (file, exc))
                    else:
                        success += 1
                else:
                    errors.append("Error parseando el archivo %s" % file)

            else:
                print("El archivo [%s] no es un xml" % file)
                errors.append("El archivo [%s] no es un xml" % file)
    else:
        errors.append("Archivo no válido")
    return {
        'archivos_analizados': count,
        'satisfactorios': success,
        'comprobantes': vouchers,
        'errores': errors
    }


def read_xml(archivo):
    vouchers = []
    count = 0
    success = 0
    errors = []

    xml = xml_headers(archivo)

    if xml:
        try:


            if xml.get('xml') is not None:

                if not isinstance(xml.get('xml'), OrderedDict):
                    voucher = xmltodict.parse(xml.get('xml'))
                else:
                    voucher = xml.get('xml')
            else:
                try:
                    salida = str(archivo.read())
                    salida = salida[2:]
                    salida = salida.replace('\n', '')

                    last_char = salida[:-1]

                    if last_char == "'":
                        salida = salida[:-1]

                    voucher = xmltodict.parse(salida, encoding='utf-8')
                except Exception as ex:
                    print(ex)

            if voucher.get('factura'):
                clean_data = {
                    'numeroAutorizacion': xml.get('numeroAutorizacion'),
                    'estado': xml.get('estado'),
                    'fechaAutorizacion': xml.get('fechaAutorizacion'),
                    'infoTributaria': voucher.get('factura').get('infoTributaria'),
                    'infoFactura': voucher.get('factura').get('infoFactura'),
                    'detalles': voucher.get('factura').get('detalles'),
                    'infoAdicional': voucher.get('factura').get('infoAdicional'),
                    'retenciones': voucher.get('factura').get('retenciones'),
                }
            elif voucher.get('notaCredito'):
                clean_data = {
                    'numeroAutorizacion': xml.get('numeroAutorizacion'),
                    'estado': xml.get('estado'),
                    'fechaAutorizacion': xml.get('fechaAutorizacion'),
                    'infoTributaria': voucher.get('notaCredito').get('infoTributaria'),
                    'infoNotaCredito': voucher.get('notaCredito').get('infoNotaCredito'),
                    'detalles': voucher.get('notaCredito').get('detalles'),
                    'infoAdicional': voucher.get('notaCredito').get('infoAdicional'),
                }
            elif voucher.get('notaDebito'):
                clean_data = {
                    'numeroAutorizacion': xml.get('numeroAutorizacion'),
                    'estado': xml.get('estado'),
                    'fechaAutorizacion': xml.get('fechaAutorizacion'),
                    'infoTributaria': voucher.get('notaDebito').get('infoTributaria'),
                    'infoNotaDebito': voucher.get('notaDebito').get('infoNotaDebito'),
                    'detalles': voucher.get('notaDebito').get('detalles'),
                    'infoAdicional': voucher.get('notaDebito').get('infoAdicional'),
                }
            

            vouchers.append(clean_data)
        except Exception as exc:
            print('============')
            print(exc)
            print('============')
            errors.append(
                "Error parseando el archivo %s. Error=> %s" % (xml, exc))
        else:
            count += 1
            success += 1
    else:
        errors.append("Error parseando el archivo %s" % xml)

    return {
        'archivos_analizados': count,
        'satisfactorios': success,
        'comprobantes': vouchers,
        'errores': errors
    }


class AttrDict(dict):
    """
        Convierte un diccionario a estructura de atributos
    """

    def __getattr__(self, attr):
        try:
            element = self.get(attr)
        except KeyError:
            return None
        if isinstance(element, list):
            return element[0]
        return element

    def __setattr__(self, attr, value):
        self[attr] = value


@retry(stop=stop_after_attempt(5), wait=wait_fixed(0.5))
def abrir_pdf_generado(ruta_pdf):
    with open(ruta_pdf, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(ruta_pdf)
        return response


def check_placa_vehiculo(identificador):
    import re

    identificador = identificador.upper()

    regex = re.match("^[A-Z]{3}[0-9]{4}$", identificador, re.I)

    resultado = ''
    if regex is not None:
        resultado = 'vehiculo'

    regex = re.match("^[A-Z]{2}[0-9]{3}[A-Z]{1}$", identificador, re.I)

    if regex is not None:
        resultado = 'moto'

    return resultado


def get_tipo_identificacion(identificacion):
    tipo_identificacion_id = 5

    if len(identificacion) > 10:
        tipo_identificacion_id = 4

    if check_placa_vehiculo(identificacion) != '':
        tipo_identificacion_id = 9

    return tipo_identificacion_id


def floatformat(value, decimal_places=2):
    """
    Retorna un numero redondeado a n decimales
    :param value:
    :param decimal_places:
    :return:
    """
    if type(value) == str:
        from decimal import Decimal
        value = Decimal(value)
    if not value:
        value = 0.0

    return "%.2f" % value


def get_item(dictionary, key):
    dic = dictionary.dict
    return dic.get(key)


def resize_image(img_ruta, ancho=320, alto=320):
    #Opening the uploaded image
    im = Image.open(img_ruta)
    im = im.convert('RGB')

    size = (ancho, alto)

    output = BytesIO()

    # Resize/modify the image
    # im = im.resize( (ancho, alto) )
    im.thumbnail(size, Image.ANTIALIAS)

    #after modifications, save it to the output
    im.save(output, format='JPEG', quality=100)
    output.seek(0)

    #change the imagefield value to be the newley modifed image value
    img = InMemoryUploadedFile(output,'ImageField', "%s.jpg" % img_ruta.path.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

    return img


def create_thumbnail(img_ruta, ancho=220, alto=220):
    """Crea una imagen en miniatura (thumbnail)."""
    im = Image.open(img_ruta)
    image_extension = os.path.splitext(str(img_ruta))[1][1:]
    image_format = str(im.format)
    size = (ancho, alto)

    output = BytesIO()

    im = im.resize((ancho, alto), Image.LANCZOS)

    #after modifications, save it to the output
    im.save(output, format=image_format, quality=100)
    output.seek(0)

    #change the imagefield value to be the newley modifed image value
    img = InMemoryUploadedFile(
        output,'ImageField',
        "{0}.{1}".format(
            img_ruta.path.split('.')[0],
            image_extension
        ),
        'image/{}'.format(image_format.lower()),
        sys.getsizeof(output), None)

    return img



def float_or_empty(value, decimal_places=2):
    """
    Retorna un numero redondeado a n decimales o vacio
    :param value:
    :param decimal_places:
    :return:
    """
    if not value or value == '':
        return ''
    import decimal
    value = decimal.Decimal(value)
    return "%.2f" % value


def formato_comprobante(fecha):

    month= fecha.strftime("%m")
    day = fecha.strftime("%d")
    year = fecha.strftime("%Y")
    choices = {'01': 'ENERO', '02':'FEBRERO','03': 'MARZO',
               '04': 'ABRIL', '05':'MAYO', '06': 'JUNIO',
               '07': 'JULIO', '08':'AGOSTO', '09': 'SEPTIEMBRE',
               '10': 'OCTUBRE','11':'NOVIEMBRE', '12': 'DICIEMBRE'}
    month = choices.get(month, 'default')
    return month +" " + day + " DEL " + year


def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    """
    Retorna el formato de fecha por defecto: Año-Mes-Dia Hora:Minuto
    :param value: fecha
    :param format: formato para resultado de fecha
    :return:
    """
    if isinstance(value, str):
        from datetime import datetime
        import locale
        locale.setlocale(locale.LC_TIME, 'es_EC.utf8')
        date = datetime.strptime(value, '%Y-%m-%d')#.date()
        return date.strftime(format)

    return value.strftime(format)


def default_none(value):
    """
    Retorna '' si el valor es None
    :param value:
    :return:
    """
    if type(value) == str and str(value) == 'None':
        value = ''
    
    return '' if not value or value == '' else value


def round_money(num, precision=2):
    import decimal
    import math

    if isinstance(num, str):
        return decimal.Decimal()

    try:
        num_ = str(round(decimal.Decimal(num), 6)).split('.')[1][2]
    except IndexError:
        return decimal.Decimal(num).quantize(decimal.Decimal("0.00"), decimal.ROUND_HALF_UP)

    if int(num_) >= 5:
        r = math.ceil(round(decimal.Decimal(num), 6) * 100) / 100
        return decimal.Decimal(r)
    else:
        return decimal.Decimal(num).quantize(decimal.Decimal("0.00"), decimal.ROUND_HALF_UP)


def to_ascii(text):
    import unicodedata
    """
        Convierte un unicode en ascii, reemplaza acentos y otros caracteres.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")

    return str(text)


def prepare_agrupacion(request, queryset):

    # campos con agrupacion
    filtros = request.GET.get('filtros')
    agrupacion = request.GET.get('agrupacion')

    # convertir a json
    agrupacion = json.loads(agrupacion) if agrupacion else []
    filtros = json.loads(filtros) if filtros else []

    grupos = [it.get('key') for it in filtros if it.get('tipo') == 'grupo']

    for item in agrupacion:
        queryset = queryset.filter(**item)

    agrupados = agrupar_queryset(queryset=queryset, grupos=grupos)

    return {
        'qs': queryset,
        'grupos': grupos,
        'agrupados': agrupados,
        'agrupacion': agrupacion
    }



def guardar_archivo_en_disco(file, ruta_directorio):
    # Guardar el archivo en disco

    filename = str(file)
    path = os.path.join(settings.MEDIA_ROOT, ruta_directorio)

    print('path: ', path)

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, filename)
    else:
        if os.path.isfile(os.path.join(path, filename)):
            n = os.path.splitext(filename)[0]
            u = '_' + str(uuid.uuid4()).split('-')[0]
            x = os.path.splitext(filename)[1]
            filename = n + u + x
            path = os.path.join(path, filename)
        else:
            path = os.path.join(path, filename)

    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return filename


def cortar_texto(texto, longitud=50):
    """
    Retorna una cadena cortada a x longitud
    :param texto:
    :param longitud:
    :return:
    """
    salida = texto
    if texto:
        salida = texto[:min(len(texto), longitud)]
    return salida


def normalizar_decimal(valor):
    
    import decimal
    try:
        return decimal.Decimal(valor).normalize()
    except Exception:
        return valor