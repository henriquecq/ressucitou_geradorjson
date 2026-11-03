# Catálogo ativo conforme a edição 2026

> Atualização do esquema: `numero` agora contém a página de 2026. `nr_2019`,
> `nr_2026` e `conteudo` foram removidos por decisão do usuário. Veja
> [Formato atual do JSON](esquema-json.md). As referências à numeração anterior
> abaixo documentam o estado antes dessa simplificação.

Data: 03/11/2026. Repositório: `D:/git/ressucitou_geradorjson`. Branch: `revisao/edicao-2026`.

## Critério aplicado

O PDF de 2026 define as fichas ativas. Os HTML antigos permanecem no Git, mas entradas sem ficha correspondente deixam de ser emitidas no JSON. A planilha Cantos.xls foi consultada como referência histórica, sem modificá-la.

O inventário agora contém as 236 fichas de cantos e modelos litúrgicos da edição: 179 de Pré-Catecumenato, 33 Litúrgicas, 16 de Catecumenato e 8 de Eleição. Índices, introduções e tabelas auxiliares de acordes/transposição não são entradas de cantos.

O JSON segue a ordem física do livro e todos os registros têm nr_2026. Os campos numero e nr_2019 foram mantidos; IDs e chaves de áudio existentes não foram renumerados. Os títulos de exibição foram atualizados para os títulos atuais, com correção de artefatos de extração como palavras quebradas. As chaves históricas de áudio/HTML permanecem estáveis.

## Retiradas do JSON, preservadas no Git

| Chave histórica | ID | Tratamento |
|---|---:|---|
| HINO DAS LAUDES DE PENTECOSTES | 104 | Ficha ausente da edição 2026. |
| PREFACIO DO ADVENTO I | 228 | A edição 2026 reúne os prefácios do Advento e Natal em uma ficha IIA. |
| PREFACIO DO NATAL DO SENHOR I | 166 | A edição 2026 reúne os prefácios do Advento e Natal em uma ficha IIA. |

Os HTML normal e estendido dessas três entradas continuam nos caminhos originais. Advento e Natal passam a usar uma única ficha atual, mantida sob a chave histórica PREFACIO DO ADVENTO II (ID 229), com título PREFÁCIO PARA O ADVENTO E NATAL.

## Transcrições deste lote

Foram incluídas as dez fichas ausentes e substituídos os textos de três fichas antigas. As 13 fichas foram conferidas visualmente contra o PDF e renderizadas nas variantes normal e estendida.

| Ficha atual | Chave estável | ID | Página 2026 | Ação |
|---|---|---:|---:|---|
| ALEGRIA, NASCEU O SALVADOR | ALEGRIA NASCEU O SALVADOR | 231 | 38 | Nova ficha |
| CANTAI A DEUS | CANTAI A DEUS | 45 | 58 | Reincluída com ID histórico |
| CRISTO É A LUZ | CRISTO E A LUZ | 232 | 72 | Nova ficha |
| SEQUÊNCIA DE CORPUS CHRISTI | SEQUENCIA DE CORPUS CHRISTI | 233 | 176 | Nova ficha |
| ACLAMAÇÕES ÀS ORAÇÕES DOS FIÉIS | ACLAMACOES AS ORACOES DOS FIEIS | 234 | 205 | Nova ficha |
| PREFÁCIO PARA O TEMPO PASCAL | PREFACIO DA PASCOA I | 167 | 230 | Texto anterior substituído |
| PREFÁCIO PARA O ADVENTO E NATAL | PREFACIO DO ADVENTO II | 229 | 231 | Texto anterior substituído |
| SALMODIA PARA O EVANGELHO | SALMODIA PARA O EVANGELHO | 235 | 233 | Nova ficha |
| SALMODIA PARA O ROSÁRIO | SALMODIA PARA O ROSARIO | 236 | 234 | Nova ficha |
| SALMODIA PARA O SALMO RESPONSORIAL | SALMODIA PARA O SALMO RESPONSORIAL | 182 | 235 | Texto anterior substituído |
| SALMODIAS PARA AS LAUDES | SALMODIAS PARA AS LAUDES | 237 | 236 | Nova ficha |
| ONDE TE ESCONDESTE, AMADO | ONDE TE ESCONDESTE AMADO | 238 | 266 | Nova ficha |
| SUBA O ESPOSO AO LENHO DO SEU TÁLAMO | SUBA O ESPOSO AO LENHO DO SEU TALAMO | 239 | 268 | Nova ficha |

O salmo responsorial agora usa o Salmo 63(62), do XXII Domingo do Tempo Comum, Ano A. Os prefácios pascal e de Advento/Natal seguem as redações das páginas 230 e 231. As versões antigas das quatro fichas que já tinham HTML, incluindo Cantai a Deus, foram copiadas para html/legado/ate-2025/normal e estendida.

## Uso da planilha histórica

Cantos.xls contém quatro abas: Cantos, MP3, Stringão e phonegap JSON. A aba Cantos tem 230 entradas preenchidas. Seus IDs coincidem com os do catálogo nos registros em comum; não houve importação de letras antigas sobre o livro novo.

A linha 232 da aba Cantos identifica CANTAI A DEUS com ID 45. Esse ID foi reaproveitado, com texto de 2026 e chave de áudio preservada. PROVAI E VEDE, ID 169 na linha 233, continua fora do JSON: existe na planilha e no Git, mas não foi localizado no livro de 2026. A ESPADA não consta da planilha histórica; seu ID atual foi mantido. A colisão legada de ID 227 não foi renumerada neste lote.

Os nove IDs novos são 231 a 239, sem reutilizar os IDs das entradas retiradas. Não foram criados arquivos de áudio nem presumida a disponibilidade de gravações para as novas fichas.

## Categorias, Índice Litúrgico e extensão

As categorias dos 236 registros coincidem com as quatro seções físicas do livro. Todas as 260 associações do Índice Litúrgico possuem correspondência no catálogo, incluindo as que antes apontavam para cantos ainda não transcritos.

As versões estendidas escrevem as repetições e os refrões completos. Os seis testes verificam, entre outros pontos, as quatro respostas completas do salmo responsorial, os seis refrões de Alegria e da Sequência de Corpus Christi, os quatro de Suba o Esposo e os dois de Onde te escondeste. As indicações FLEXA, ALTA, modelos de salmodia e braçadeira foram preservadas. As cifras retêm menores, acidentes e extensões.

A diagramação é a do HTML monoespaçado do aplicativo. Não é reprodução gráfica do PDF: diagramas gráficos de posições de violão continuam na fonte PDF, enquanto as cifras correspondentes estão transcritas em texto.

## Validação e alcance

- 236 registros e 472 variantes validados; todo base64 coincide com o HTML fonte.
- Inventário ativo/retirado, IDs novos, títulos e paginação conferidos.
- HTMLs das entradas retiradas preservados; versões antigas das fichas substituídas arquivadas.
- Seis testes de integridade e expansão de repetições aprovados.
- Verificadores de classificação/cores e tratamento aprovados.
- Análise Dart sem problemas; geração determinística do JSON verificada.
- A planilha original permanece com o mesmo SHA-256.

Este lote completa a correspondência do inventário com as 236 fichas, mas não certifica integralmente a letra e cada entrada de cifra das 223 fichas reaproveitadas de lotes anteriores. A revisão integral desses conteúdos continua; o histórico de tratamento e as correções confirmadas foram preservados.

Os aplicativos não foram alterados ou publicados. Para exibir a paginação atual, seus consumidores precisarão usar nr_2026. A retirada no JSON não apaga dados salvos no aparelho; a aplicação desse catálogo nos clientes ainda precisa ser validada.

Arquivos de controle: data/edicao_2026/catalogo.json e fichas-revisadas.json. Capturas reais: docs/revisao/evidencias/espelho-2026.
