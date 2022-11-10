import json
import os
import uuid
import subprocess
from decimal import Decimal
from secretary import Renderer

from .utils import cortar_texto, xml_headers, floatformat, get_item, float_or_empty, formato_comprobante, \
    datetimeformat, default_none, normalizar_decimal
from .bar_codes.code128 import code128_format, code128_image

from .constantes import  FORMATOS_ARCHIVOS
import time
from collections import OrderedDict

FLOAT_CONVERT_ONLY_FLOAT_STYLE = 1



def export_reporte_hoja_calculo(queryset, template_ods_ruta, formato_salida='ODS'):
    """ Dada una plantilla convierte un archivo ODS al formato dado """

    engine = Renderer()
    print(formato_salida)
    engine.FLOAT_CONVERT = FLOAT_CONVERT_ONLY_FLOAT_STYLE

    my_uuid = str(uuid.uuid4())

    ods_out = '/tmp/output{0}.ods'.format(my_uuid)
    coverted_file = '/tmp/output{0}.{1}'.format(my_uuid, formato_salida.lower())

    with open(template_ods_ruta, 'rb') as template:
        engine.environment.filters['floatformat'] = floatformat
        engine.environment.filters['get_item'] = get_item
        engine.environment.filters['floatformat'] = float_or_empty
        engine.environment.filters['floatformat_'] = floatformat
        engine.environment.filters['default_none'] = default_none
        engine.environment.filters['formato_comprobante'] = formato_comprobante
        engine.environment.filters['datetimeformat'] = datetimeformat
        engine.environment.filters['cortar_texto'] = cortar_texto
        engine.environment.filters['normalizar_decimal'] = normalizar_decimal
        result = engine.render(template=template, **queryset)

    with open(ods_out, 'wb') as output:
        output.write(result)

    if formato_salida != 'ODS':
        command_convert = "libreoffice --headless --convert-to {0} --outdir {1} {2}".format(
            FORMATOS_ARCHIVOS.get(formato_salida).get('convert_cmd'), '/tmp/', ods_out
        )

        subprocess.call(command_convert, shell=True)
        return coverted_file

    return ods_out



