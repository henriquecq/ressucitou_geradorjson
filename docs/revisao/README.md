# Revisão dos cantos — edição de 2026

Este repositório é a fonte dos HTML normal (`html/`) e estendido (`html/ext/`).
Editar aqui e gerar `cantos.json`; evitar novas correções de conteúdo apenas
na camada de carregamento do Flutter. A camada antiga continua útil para
catálogos já instalados e não deve ser retirada sem avaliar a atualização
desses dados.

## Contrato a preservar

- IDs e chave `html` estáveis: participam de dados salvos e identificação do áudio.
- A colisão legada 227 é conhecida e não será corrigida por renumeração automática.
- Preservar fonte monoespaçada, `white-space:pre`, espaços, quebras e alinhamento.
- Preservar `<H1>`, `#FF0000`, `@transp@`, `@capot@` e `font-size:12px`.
- Atualizar as duas variantes. A estendida conserva repetições por extenso.
- Não substituir as transcrições existentes pelos rascunhos OCR reprovados.
- Não usar contagem de imagens como contagem de cantos revisados.

## Geração e validação

Na raiz do repositório:

```powershell
dart lib/generateJson.dart
python tools/validate_catalog.py cantos.json --html-root html
python tools/validate_classificacao.py
python tools/validate_tratamento.py
python tools/validate_edicao.py
python -m unittest discover -s tools -p "test_*.py"
dart analyze lib
```

O gerador usa apenas bibliotecas padrão e importação relativa de `canto.dart`.
Foi executado com Dart 3.8.1 sem instalar dependências ou modificar o lockfile.
A restrição legada de SDK do `pubspec.yaml` não foi migrada; o fluxo acima
executa o script diretamente, sem `pub get`.

Para verificar estabilidade de IDs e ausência de remoções, acrescente
`--baseline caminho/catalogo-anterior.json` ao validador. A validação compara
os 458 HTML incorporados com os arquivos fonte, byte a byte. Ela não certifica
letras, cifras ou alinhamento musical.

## Estado de 03/11/2026

Estado atual: **236 fichas ativas**, conforme o [relatório do catálogo 2026](espelho-2026.md).
Três entradas antigas ficam fora do JSON, com seus HTML preservados no Git.
Dez fichas foram incluídas, e três fichas antigas tiveram o texto substituído
pelo de 2026. O inventário está completo; a revisão integral do conteúdo
das demais fichas continua separadamente.

O catálogo ativo passa a seguir a edição 2026. `data/edicao_2026/catalogo.json`
registra as entradas ativas, as retiradas e as fichas ainda sem transcrição.
O gerador omite as retiradas do JSON e preserva seus HTML no Git.
`numero` informa a página de 2026 como string. Os campos `nr_2019`,
`nr_2026` e `conteudo` foram removidos do modelo, do gerador e do JSON.
IDs e chaves de áudio foram preservados. O formato atual está descrito em
[Esquema do JSON](esquema-json.md); este chat altera apenas o catálogo e seu gerador.

As treze fichas deste lote são mantidas em
`data/edicao_2026/fichas-revisadas.json`. `python tools/build_reviewed_sheets.py`
reproduz seus HTML, incluindo a expansão das repetições na versão estendida.
As versões anteriores das quatro fichas que já possuíam HTML estão em
`html/legado/ate-2025/`.

Veja [o relatório do primeiro lote](lote-01.md) e
[a proveniência das correções migradas](migracao-correcoes-2026.json).
Capturas reais dos HTML antes/depois ficam em `evidencias/`.
O [relatório de tratamento](tratamento-2026.md) registra a varredura dos
229 cantos nas duas variantes, as correções e os cinco casos sem
correspondência textual direta na edição de 2026.

A fonte de revisão passa a ser o PDF de 2026 fornecido pelo usuário, com
comparação visual ao PDF de 2019 e aos HTML quando necessário. O PDF deve
ser mantido fora do Git. A página 8 de 2026 lista inserções e mudanças de
categoria, mas não esgota as alterações existentes no corpo do livro.

## Próximos lotes

1. Revisar integralmente os três cantos cujas correções pontuais foram migradas:
   a migração de um erro confirmado não certifica o restante da ficha.
2. As 26 mudanças de categoria, cores e o Índice Litúrgico foram incorporados.
   Veja [a classificação 2026](classificacao-2026.md) e o manifesto JSON
   correspondente, incluindo os novos cantos ainda sem transcrição.
3. Revisar `Cantai a Deus`: removido em 2019 e reinserido em 2026 com revisão.
   A mera existência do HTML antigo não autoriza reativá-lo sem atualizar.
4. Mapear inserções, renomeações e continuações. Preservar `nr_2019` e avaliar
   um campo próprio de numeração 2026 junto aos consumidores do JSON.
5. Seguir por lotes pequenos, com diferenças confirmadas, capturas das duas
   variantes e validação. Registrar ambiguidades sem inventar letra ou cifra.
