# Formato atual do JSON

Decisão do usuário em 03/11/2026: manter apenas `numero` para paginação,
remover `conteudo` e não manter compatibilidade com os campos das versões antigas.
Este lote está limitado ao JSON e ao seu gerador. O aplicativo é atualizado
em outro chat e não recebeu alterações aqui.

`numero` é uma string com a página da edição 2026, por exemplo `"21"` para
`A CABANA DOS PASTORES`. Seu valor vem de `page` no inventário da edição,
em `data/edicao_2026/catalogo.json`. Não há segunda numeração no JSON emitido.

Foram removidos dos 236 registros e do modelo do gerador:

- `nr_2019`;
- `nr_2026`;
- `conteudo`, incluindo a rotina que gerava o antigo texto de busca.

Permanecem `id`, `titulo`, `html`, `url`, `categoria`, `numero` e as variantes
`html_base64` e `ext_base64`. Os 13 booleanos foram substituídos pela lista
`categorias`. IDs, chaves de áudio, títulos, etapa/cor, ordem do livro e bytes
dos dois HTML foram preservados nesta migração.

O gerador escreve o JSON com quatro espaços de indentação, conservando a
formatação que já estava na cópia local antes desta alteração.

Validação: os 236 valores de `numero` foram comparados ao inventário 2026;
nenhum registro contém os três campos removidos. Os verificadores do catálogo,
da edição, de classificação e de tratamento foram executados, além dos testes
de integridade. A geração continua determinística.

Os relatórios anteriores são históricos: referências a `nr_2026` ou à
preservação da numeração de 2019 descrevem o formato anterior a esta decisão.

## Índice Litúrgico dinâmico

### Consulta de atualizações

`cantos_versao.txt` fica na raiz, ao lado de `cantos.json`, e contém somente
um inteiro decimal positivo seguido de quebra de linha. É a revisão do
catálogo, independente de `edicao` (2026) e da versão do aplicativo.

O app deve consultar esse arquivo na mesma branch usada para baixar o JSON,
comparar o valor com a revisão local e baixar o catálogo quando forem diferentes
ou quando ainda não houver cópia local. Deve salvar a revisão somente depois
de baixar, validar e instalar o JSON com sucesso. Se a consulta falhar, deve
conservar o catálogo local e tentar novamente depois.

O gerador inicia em 1. Se o JSON gerado mudar, incrementa a revisão; se o
conteúdo permanecer igual, conserva o valor. Diferenças CRLF/LF não provocam
incremento. Não editar o JSON gerado manualmente: alterar as fontes e executar
`dart lib/generateJson.dart`. Publicar ambos os arquivos juntos. Não apagar
nem reduzir a revisão já publicada. Um arquivo de versão inválido interrompe
a geração antes de escrever o catálogo.

### Estrutura

O app passa a consumir `cantos.json` de `otaviogrrd/ressucitou_geradorjson`,
substituindo a fonte `ressuscitou_android`. Não há compatibilidade com o
formato anterior. A raiz agora é um objeto:

```json
{
  "edicao": 2026,
  "categorias": [
    {"id": "advento-natal", "nome": "Advento - Natal", "ordem": 1}
  ],
  "cantos": [
    {
      "id": 1,
      "titulo": "A CABANA DOS PASTORES",
      "categoria": 1,
      "numero": "21",
      "categorias": ["pascoa-pentecostes", "comunhao-calice"]
    }
  ]
}
```

O exemplo abrevia as categorias e os demais campos do canto.
O app deve montar o índice usando `nome` e `ordem` da raiz. Ao selecionar
uma categoria, deve filtrar os cantos cuja lista `categorias` contém aquele
`id`. IDs são estáveis e permitem renomear rótulos sem mudar vínculos.
Uma lista vazia significa ausência nos grupos do Índice Litúrgico.

| ID | Nome | Ordem |
|---|---|---:|
| advento-natal | Advento - Natal | 1 |
| quaresma | Quaresma | 2 |
| pascoa-pentecostes | Páscoa - Pentecostes | 3 |
| virgem | Cantos à Virgem | 4 |
| criancas | Cantos para as crianças | 5 |
| entrada | Cantos de entrada | 6 |
| paz-oferendas | Paz - Apresentação das oferendas | 7 |
| fracao-pao | Fração do pão | 8 |
| comunhao-calice | Comunhão com o cálice | 9 |
| final | Canto final | 10 |

`categoria` (singular) continua sendo a etapa/cor: 1 Pré-Catecumenato,
2 Catecumenato, 3 Eleição, 4 Litúrgicos. É independente de `categorias`
(plural), que contém os usos litúrgicos.

As definições vêm de `data/edicao_2026/categorias.json`. `grupoFonte` é
interno ao gerador, associando cada categoria ao grupo transcrito em
`docs/revisao/classificacao-2026.json`; não é emitido no JSON público.
Os vínculos vêm diretamente de `liturgicalIndex`, não dos antigos booleanos.

Em relação a 2019, Advento e Natal foram reunidos, assim como Páscoa e
Pentecostes. Comunhão passou a Comunhão com o cálice, com repertório revisto.
Laudes–Vésperas deixou de existir no Índice Litúrgico de 2026; a categoria
e suas associações históricas não são emitidas. A ficha Salmodias para as
Laudes permanece no catálogo. O histórico está preservado no Git e nos
relatórios anteriores.

Foram removidos `adve`, `laud`, `entr`, `nata`, `quar`, `pasc`, `pent`,
`virg`, `cria`, `cpaz`, `fpao`, `comu` e `cfin` de todos os cantos.

As validações conferem dez categorias, nomes/ordem, ausência dos booleanos
e os 260 vínculos dos 236 cantos contra o índice transcrito. Os testes
rejeitam vínculos desconhecidos, duplicados e o retorno de Laudes–Vésperas.
Amém, amém, amém mantém a página correta 208 e o vínculo com Entrada,
apesar da referência impressa incorreta 207 no índice.
