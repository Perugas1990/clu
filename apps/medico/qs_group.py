from django.db.models import Count, Sum, F, Value, TextField
from datetime import datetime
from itertools import groupby


def agrupar_queryset(queryset, grupos):

    if not grupos:
        return []

    queryset = queryset.order_by(
        *grupos).values(
        *grupos)

    for grupo in grupos:
        queryset = queryset.annotate(
            Count(grupo)
        )
    # buscar los grupos primaros
    items = []

    grupo_inicial = None
    if len(grupos) > 0:
        grupo_inicial = grupos[0]

    grupos_padres = []
    order_reverse = False
    for it in queryset.order_by(*grupos):
        valor = dict(it).get(grupo_inicial)
        if valor and isinstance(valor, datetime):
            valor = valor.date()
            order_reverse = True

        grupos_padres.append(str(valor))

    grupos_padres = list(set(grupos_padres))

    try:
        grupos_padres = list(grupos_padres.sort(key=str, reverse=order_reverse))
    except Exception:
        pass

    c = 0

    for padre in grupos_padres:

        if padre is None or padre == 'None':
            subcategorias = queryset.filter(**{'{0}__isnull'.format(grupo_inicial): True})
        else:
            subcategorias = queryset.filter(**{grupo_inicial: padre})

        pjs = subcategorias.aggregate(
            a=Sum('{0}__count'.format(grupo_inicial))).get('a')

        subgrupos = []

        if len(grupos) > 1:
            subgrupo = grupos[1]
            subgrupos = subcategorias.annotate(
                total=F('{0}__count'.format(subgrupo)),
                texto=F(subgrupo),
                campo=Value(subgrupo, output_field=TextField())
            )

        item = {
            'agrupacion': c,
            'texto': padre,
            'campo': grupo_inicial,
            'total': pjs,
            'grupos': subgrupos
        }
        c += 1

        items.append(item)

    return items


def group_list_dict(listado, group_by):
    """
    Agrupa un listado de diccionarios por un campo
    :param listado: listado de diccionarios
    :param group_by: campo por el que se va a agrupar
    :return: listado de diccionarios agrupados
    """

    # define a fuction for key
    def key_func(k):
        return k[group_by]

    # sort listado data by group_by key.
    listado = sorted(listado, key=key_func)

    return groupby(listado, key=key_func)

