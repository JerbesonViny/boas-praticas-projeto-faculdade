# O strptime aceita estas datas, mas elas nao voltam identicas no strftime.
DATAS_FORA_DO_PADRAO = [
    '2026-1-5',
    '2026-10-5',
    '２０２６-10-05',
]

# O strptime recusa estas datas e o ValueError sobe sem conversao.
DATAS_NAO_RECONHECIDAS = [
    '20261005',
    '05/10/2026',
    '2026/10/05',
    '',
    ' 2026-10-05',
    '2026-10-05 ',
    '2026-10-05T10:00',
]

DATAS_INEXISTENTES = [
    '2026-02-29',
    '2026-02-30',
    '2026-04-31',
    '2026-13-01',
    '2026-00-10',
    '2026-10-00',
]

DATAS_COM_TIPO_INVALIDO = [
    None,
    20261005,
    b'2026-10-05',
]
