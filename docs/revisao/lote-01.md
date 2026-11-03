# Lote 01 — migração e retomada local

Data: 03/11/2026. Base do gerador: `cf78dd1`.
Origem da migração: Flutter `124e2207a52e1fadacd75c387308c5efeaeaa70f`.

## Correções migradas à fonte

| Chave HTML | Ajuste | Variantes |
|---|---|---|
| NAO ESTA AQUI RESSUSCITOU | Solo → Sol- sobre “o Crucificado” | normal e estendida |
| VIRGEM DA MARAVILHA | Si → Si- sobre “terra” | normal e estendida |
| CREDO | CEUS → CÉUS; COMUNHAO → COMUNHÃO | normal e estendida |

São oito substituições em seis arquivos. Os trechos de origem ocorreram uma
única vez nos lugares esperados. Espaços, quebras, repetições e demais conteúdo
foram preservados por substituições exatas, sem reformatar os HTML.

As evidências anteriores e as regras do Flutter fundamentam essas correções.
Foram geradas novas capturas locais das duas variantes. A inspeção pontual
dos resultados não significa revisão integral desses três cantos contra 2026.

## Continuação da revisão: RESSUSCITOU

Fonte: Ressuscitou 2026, página física 165 do PDF (numeração contada desde a
primeira página do arquivo). A página inteira foi renderizada e inspecionada,
assim como os HTML normal e estendido antes/depois.

Foram acrescentadas três vírgulas em cada variante:

- “Alegria, alegria, irmãos,”;
- “que se hoje nos amamos,”;
- “Se com ele morremos,”.

A inserção na primeira frase desloca “irmãos” uma coluna. O Sol dessa linha
foi deslocado uma coluna à direita, conservando sua posição relativa à
mesma sílaba. Os demais espaços e linhas foram preservados. As capturas finais
foram conferidas visualmente. O teor das estrofes, a sequência dos acordes
e a ordem dos refrões foram confrontados com a ficha. A estendida mantém
os retornos completos do refrão, sem substituir o texto por BIS.

Os HTML conservam as linhas longas preexistentes, enquanto a ficha quebra
“Graças” e “Alegria” em linhas próprias. Essa diferença de apresentação não
foi transportada automaticamente para o formato funcional do aplicativo.
Este lote conclui a pendência de pontuação; não constitui certificação
de cada ponto de entrada de todos os acordes do canto.

## JSON gerado

O gerador Dart original foi executado. Há alterações semânticas em cinco
registros: os três migrados, `RESSUSCITOU` e
`EIS QUE O NOSSO ESPELHO E O SENHOR`. Este último incorpora os HTML já
modificados no commit de julho de 2025, que ainda não constavam do JSON.
Seus arquivos HTML não foram novamente editados neste lote.

O texto de busca foi regenerado pelo próprio gerador. Mantidos os 229
registros, ordem, IDs, títulos, chaves, categorias e numerações originais.
Não houve inclusão automática de cantos nem alteração dos aplicativos.

## Verificações

- Contrato estrutural dos 229 registros e das duas variantes: aprovado.
- IDs e registros comparados ao JSON anterior: preservados.
- Todos os 458 base64 correspondem exatamente aos HTML fonte.
- Regeneração determinística do JSON: verificada por SHA-256.
- `dart analyze lib`: sem problemas.
- Capturas antes/depois produzidas com Edge headless/Playwright, JavaScript
  desativado e requisições externas bloqueadas.

As verificações não substituem a validação do WebView/transpositor em aparelho.
O Flutter mantém suas regras para os catálogos antigos. Não houve publicação,
push ou merge nesta etapa.
