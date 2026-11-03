# Ressuscitou — fonte dos HTML e catálogo JSON

O catálogo ativo segue o inventário da edição 2026. As fichas retiradas
continuam no Git e são omitidas do JSON. IDs e chaves de áudio existentes
são preservados; `numero` contém a página da edição 2026 como string.
O JSON não contém `nr_2019`, `nr_2026` ou `conteudo`.

Este repositório passa a ser a fonte do catálogo consumido pelo app,
substituindo `ressuscitou_android`. A raiz do JSON é um objeto com `edicao`,
`categorias` e `cantos`. O Índice Litúrgico é definido dinamicamente pelo
catálogo de dez categorias e pelos IDs em `categorias` de cada canto;
os antigos booleanos foram removidos. Veja o
[contrato do JSON](docs/revisao/esquema-json.md) para adaptar o consumidor.

Na raiz do repositório:

```powershell
dart lib/generateJson.dart
dart tools/test_catalog_output.dart
python tools/validate_catalog.py cantos.json --html-root html
python tools/validate_edicao.py
python tools/validate_classificacao.py
python tools/validate_tratamento.py
python -m unittest discover -s tools -p "test_*.py"
```

Para reproduzir os HTML das transcrições revisadas deste lote, execute
`python tools/build_reviewed_sheets.py` antes de gerar o JSON.
As transcrições integrais adicionais são reproduzidas com
`python tools/build_eucharistic_sheets.py` e
`python tools/build_complementary_sheets.py`. O validador de edição confere
os HTML contra as fontes estruturadas. As fichas reconstituídas na revisão
por faixas usam também `python tools/build_faixa1_sheets.py` e
`python tools/build_maximum_review_faixa3.py`. Edite essas fontes quando
alterar uma ficha mantida por esses geradores, para preservar a correção.

Veja o [estado do catálogo 2026](docs/revisao/espelho-2026.md) e as
[instruções de revisão](docs/revisao/README.md). O inventário está completo;
a revisão integral do conteúdo de todas as fichas continua por lotes.

`cantos_versao.txt`, na raiz, contém a revisão inteira do catálogo. O app
consulta esse arquivo e baixa `cantos.json` quando a revisão for diferente
da cópia local. Os dois arquivos devem ser publicados juntos na mesma branch.
O gerador inicia em 1 e incrementa a revisão somente quando o JSON muda.
