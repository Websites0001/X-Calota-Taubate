# Site do X Calota Taubaté (prévia)

Site de uma página com o cardápio completo do X Calota Taubaté (Praça Santa Terezinha, 159, Centro), para computador e celular.

## Abrir

Dê dois cliques no `index.html`. Precisa de internet só para as fontes e o mapa; as fotos estão na pasta `fotos/`.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `index.html` | A página |
| `css/estilo.css` | Visual. As cores ficam no topo (`--yellow`, `--red`) |
| `js/dados.js` | Loja, horários, taxas, frases e o cardápio inteiro (gerado automaticamente) |
| `js/app.js` | Funcionamento: sacola, adicionais, calculadora, animações, galeria infinita |
| `fotos/cardapio/` | Uma foto por item (do cardápio online da loja) |
| `fotos/local/` | Logo, anúncio da loja e foto de cliente do Google Maps |
| `_coleta/` | Dados brutos coletados e o script que gera o `dados.js` |
| `REVISAR.md` | O que confirmar com o dono antes de publicar |
| `AVALIACAO-SITE-ATUAL.md` | Avaliação do cardápio atual (Brendi), boa para mostrar ao dono |

## Mudar algo

- **Preço, nome ou descrição:** edite direto em `js/dados.js`.
- **Gerar o cardápio de novo:** rode `python gerar_dados.py` dentro de `_coleta`. Isso sobrescreve o `dados.js` (edições feitas à mão nele se perdem).

## O que tem no site

- Abertura com a marca (só na primeira visita)
- Topo com a Calota girando dentro de um anel de texto e selos "28 cm" e "Serve até 4"
- Faixa infinita que acelera e muda de direção com a rolagem
- Carrossel infinito dos mais pedidos (arrasta com impulso e encaixa)
- Calculadora "Quanto sai por pessoa?" com a Calota cortada em fatias
- Cardápio com abas fixas, busca e filtros (Frango, Bacon, Catupiry, Cheddar, Carnes nobres, Até R$ 40)
- Adicionais com quantidade (até 3 por lanche), e preço somando na hora
- Combos com quanto sai a menos que pedir separado
- Sacola com entrega ou retirada, pagamento e troco, e pedido pronto no WhatsApp
- Galeria infinita com as fotos do cardápio
- Horários, taxa por distância, pagamento, mapa e botões de rota, WhatsApp e Instagram
- Tema claro (padrão, amarelo da marca) e escuro
