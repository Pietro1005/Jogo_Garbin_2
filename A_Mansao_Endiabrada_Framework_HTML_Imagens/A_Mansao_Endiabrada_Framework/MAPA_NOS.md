# MAPA DE NÓS — A MANSÃO ENDIABRADA

## Fluxo principal
inicio → entrada_mansao → hall

hall → cozinha | biblioteca | banheiro | hall_2
hall_2 → escritorio | escadas | garagem | inventario

escadas → sotao | porao | hall_2
banheiro → jardim
biblioteca → pistas/chave
escritorio → cartão/documentos/fotografias
garagem → gasolina/fusível/machado → fuga de carro
porao → gerador → sala de segurança
sotao → Sarah/chave mestra | fita VHS
seguranca → câmeras | rádio | túnel | VHS
tunel → final túnel

## Eventos globais
Em cenas de exploração, o assassino pode interromper a cena com chance de 20%.
O evento sorteia entre aparição, passos, distância, respiração, máscara,
assassino na sala/segurança e encontro direto.

## Perseguição
perseguicao → esquerda | direita | esconder
esquerda → hall/jardim/combate
direita → cozinha/sotao/dano
esconder → hall

## Combate
combate → faca | machado | correr | esconder
faca → perseguição
machado → hall

## Finais
- fim_fuga: chave enferrujada + portão
- fim_carro: gasolina + fusível + garagem
- fim_tunel: chave mestra + sala de segurança
- fim_policia: rádio + pedido de socorro
- fim_secreto: diário + fita + cartão de segurança + chave mestra
- fim_morte: vida chega a 0
- fim_preso: rota de fuga perdida / decisão de final sem pistas

## Estado
vida
inventario
pontos
assassino_alertado
gerador_ligado
sobrevivente_salvo
radio_ajuda
fita_assistida
cena_anterior
