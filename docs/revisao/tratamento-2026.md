> Registro do lote anterior. O inventário ativo e as pendências foram atualizados em [Catálogo 2026](espelho-2026.md).

# Conferência de tratamento — catálogo completo

Data: 03/11/2026. Repositório: `D:/git/ressucitou_geradorjson`, branch `revisao/edicao-2026`.

## Cobertura

Foram examinados os 229 cantos, nas versões normal e estendida (458 HTML), procurando pronomes de tratamento, possessivos, imperativos e concordância verbal. A comparação textual incluiu as páginas de continuação das fichas extensas. Os candidatos foram avaliados em contexto; apenas as diferenças confirmadas foram alteradas.

Resultado: 18 cantos corrigidos em 35 HTML, com 171 linhas de letra alteradas. A versão estendida de Não resistais ao mal já estava correta e não foi regravada. O Glória, corrigido no lote anterior, foi novamente incluído na varredura sem nova alteração.

Os demais 211 cantos não receberam correções de tratamento neste lote. Destes, cinco têm a limitação de correspondência textual descrita abaixo. “Sem divergência adicional confirmada” não significa certificação integral de todas as palavras, cifras ou posições do canto.

## Cantos corrigidos

| Chave do canto | Página inicial da ficha 2026 | Variantes alteradas | Linhas de letra alteradas |
|---|---:|---|---:|
| A VITIMA PASCAL | 31 | normal, estendida | 2 |
| ANAFORA DO SAL | 209 | normal, estendida | 4 |
| BENCAO DA AGUA | 210 | normal, estendida | 24 |
| BENCAO PENITENCIAL | 212 | normal, estendida | 2 |
| HINO A CRISTO LUZ | 106 | normal, estendida | 2 |
| LADAINHA PENITENCIAL I | 218 | normal, estendida | 28 |
| LADAINHA PENITENCIAL II | 219 | normal, estendida | 66 |
| ORACAO EUCARISTICA IV | 223 | normal, estendida | 4 |
| PRECONIO PASCAL | 228 | normal, estendida | 6 |
| SALVE RAINHA | 167 | normal, estendida | 2 |
| TE DEUM | 244 | normal, estendida | 14 |
| NAO RESISTAIS AO MAL | 250 | normal | 1 |
| SANTO 1982 | 238 | normal, estendida | 2 |
| SANTO 1988 | 239 | normal, estendida | 4 |
| SANTO HEBRAICO | 240 | normal, estendida | 4 |
| SANTO PALESTINA 74 | 241 | normal, estendida | 2 |
| SANTO PALOMERAS 65 | 242 | normal, estendida | 2 |
| SANTO ROMA 77 | 243 | normal, estendida | 2 |

Exemplos: tua → vossa nos seis Santo; tu/deste → vós/destes e tem → tende nas ladainhas; pronomes e imperativos na Bênção da Água; verbos no Te Deum; amaste → amastes e deu graças → deu-vos graças na Oração Eucarística IV.

## Casos que devem continuar no singular

- Precônio Pascal: a invocação à noite conserva tu, despojaste, enriqueceste e conheceste. As invocações a Deus foram corrigidas para aceitai e vos, conforme a página 229.
- À vítima pascal: a página 31 conserva Tu, Rei vitorioso e usa dá-nos; o HTML estava inconsistente com dai-nos.
- Não resistais ao mal: os exemplos pessoais mantêm te/teu; o refrão isolado que estava no singular foi corrigido para resistais.
- Salmos e outros textos que conservam tu/te no PDF não foram convertidos globalmente para vós/vos.

## Limitações explícitas de correspondência

Todos os cinco HTML abaixo foram lidos nas duas variantes. Eles não foram tratados como certificados contra uma ficha textual idêntica em 2026:

- HINO DAS LAUDES DE PENTECOSTES: Não localizada ficha correspondente no PDF de 2026; texto em tu preservado, sem presumir troca para vós.
- PREFACIO DO NATAL DO SENHOR I: Não localizada ficha textual correspondente no PDF de 2026. Texto já usa vós; preservado.
- PREFACIO DO ADVENTO I: Página 231 fornece outro texto (Advento IIA), com melodia adaptável. Não foi tomada como transcrição equivalente do prefácio I.
- PREFACIO DO ADVENTO II: Página 231 fornece o prefácio Advento IIA, não o mesmo texto do cadastro legado. Texto já em vós foi preservado.
- SALMODIA PARA O SALMO RESPONSORIAL: Página 235 usa outro salmo como exemplo. Não converter o salmo legado para o novo apenas por diferença de tratamento.

## Cifras, repetição e evidências

As notas e sua sequência foram preservadas. As colunas das cifras foram ajustadas apenas para acompanhar os deslocamentos do texto. Na Ladainha Penitencial I, as respostas foram deslocadas oito colunas para a direita para evitar sobreposição com as invocações mais longas; as respectivas cifras acompanharam as respostas.

Foram geradas 70 capturas reais antes/depois dos 35 HTML alterados. Os trechos modificados foram inspecionados nas versões normal e estendida. As páginas relevantes do PDF foram renderizadas e os pontos alterados conferidos visualmente. Isso não certifica outras divergências de letra/cifra fora deste escopo. As capturas estão em `docs/revisao/evidencias/tratamento/`.

## Correção de correspondência de título

Carmen 63 já é o canto ESTAO ROTAS MINHAS ATADURAS; seu subtítulo identifica o poema. Foi corrigido o manifesto anterior, preservando a chave de áudio e aplicando Comunhão com o cálice e Canto final ao registro existente. Não foi criado um canto duplicado. O relatório de classificação anterior foi atualizado para 256 associações aplicáveis ao catálogo e quatro associações de três cantos ainda ausentes.

## Verificações

- JSON regenerado com o gerador Dart.
- Contrato dos 229 registros e equivalência dos 458 base64 com os HTML: aprovados.
- Pronomes/versos corrigidos e sequência das cifras comparados à base do lote.
- Classificações e cores verificadas; somente os filtros comu/cfin de Carmen 63 foram corrigidos neste lote.
- IDs, chaves de áudio, ordem, títulos e numerações preservados.
- Versões estendidas e repetições mantidas.
- Sem publicação ou atualização dos aplicativos.

O manifesto `docs/revisao/tratamento-2026.json` contém uma entrada de cobertura para cada um dos 229 cantos, mais o antes/depois de cada linha alterada.
