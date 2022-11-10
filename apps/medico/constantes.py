
TIPO_PAGOS_SRI = {
    '01': 'SIN UTILIZACION DEL SISTEMA FINANCIERO',
    '15': 'COMPENSACIÓN DE DEUDAS',
    '16': 'TARJETA DE DÉBITO',
    '17': 'DINERO ELECTRÓNICO',
    '18': 'TARJETA PREPAGO',
    '19': 'TARJETA DE CRÉDITO',
    '20': 'OTROS CON UTILIZACION DEL SISTEMA FINANCIERO',
    '21': 'ENDOSO DE TÍTULOS'
}

FORMATOS_ARCHIVOS = {
    'ODS': {
        'content_type': 'application/vnd.oasis.opendocument.spreadsheet',
        'convert_cmd': ''
    },
    'PDF': {
        'content_type': 'application/pdf',
        'convert_cmd': 'pdf'
    },
    'XLS': {
        'content_type': 'application/vnd.ms-excel',
        'convert_cmd': 'xls:"MS Excel 97"'
    },
    'XLSX': {
        'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'convert_cmd': 'xlsx'
    },
    'CSV': {
        'content_type': 'text/csv',
        'convert_cmd': 'csv'
    },
    'DOCX': {
        'content_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'convert_cmd': 'docx'
    },
    'DOC': {
        'content_type': 'application/msword',
        'convert_cmd': 'doc'
    },
    'ODT': {
        'content_type': 'application/vnd.oasis.opendocument.text',
        'convert_cmd': 'odt'
    }
}

FILTRO_EXCLUYE = ['not_equals', 'no_contains', '!=']
BOOLEAN_FILTRO = ['verdadero', 'falso']

PARAMETROS_FILTRO = {
    'equals': '__iexact',
    'not_equals': '__iexact',
    'contains': '__icontains',
    'no_contains': '__icontains',
    '=': '',
    '!=': '',
    '>': '__gt',
    '<': '__lt',
    '>=': '__gte',
    '<=': '__lte',
    'verdadero': True,
    'falso': False,
    'd=': '__date',
    'd!=': '__date',
    'd>': '__date__gt',
    'd<': '__date__lt',
    'd>=': '__date__gte',
    'd<=': '__date__lte',
}