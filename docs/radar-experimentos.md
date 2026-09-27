# Trilha de radar — propostas experimentais

**Status:** planejamento. Não há hardware radar nem resultados reais neste ZIP.
Radar aqui significa emissão e recepção de ondas eletromagnéticas; a varredura
com HC-SR04 e servo do Lab 03 continua sendo um experimento de sonar.

## Etapa inicial: rastreamento mmWave de 24 GHz

**Candidato de bancada:** Hi-Link HLK-LD2450, conectado por UART a um ESP32.
O fabricante descreve um sensor para rastrear até três alvos em movimento,
fornecendo posições e informações de movimento. Confirmar pinagem, alimentação,
níveis lógicos e protocolo na documentação da unidade adquirida antes de ligar.
Não pressupor que o módulo entregue ecos brutos ou imagem de todos os objetos.

Experimentos propostos para o Lab 06:

1. **Campo de visão:** marcar posições conhecidas no chão e mover uma pessoa
   pelos pontos; registrar detecções, coordenadas relatadas e ausências.
2. **Trajetória:** percorrer a mesma rota em velocidades diferentes; comparar
   coordenadas estimadas, latência aparente e perda de rastreamento.
3. **Múltiplos alvos e oclusão:** repetir com duas ou três pessoas, registrar
   mudanças de identificação, oclusões e possíveis alvos falsos.
4. **Comparação entre modalidades:** registrar simultaneamente a posição de
   um alvo móvel com radar e, onde houver condições equivalentes de visada,
   sonar/LiDAR; comparar cobertura, falhas e precisão. Identificar diferenças
   de campo de visão e de alvo antes de interpretar os números.

Para cada sessão, preservar dados brutos, marcação do ambiente, orientação e
altura do módulo, posição de referência, horário, firmware, número de amostras,
falsas detecções e perdas. Um gráfico XY das trajetórias serve para **alvos
rastreados**, não representa um mapa completo das superfícies da sala.

## Etapa avançada: nuvem de pontos por radar

**Estudo de viabilidade para o Lab 08:** placa de avaliação TI IWR6843ISK,
que oferece acesso a dados de nuvem de pontos via USB, segundo o fabricante.
Pesquisar custo, disponibilidade, ferramentas, formato de saída e campo de
visão antes de definir compra ou metodologia. A comparação planejada é entre
nuvens de pontos de radar e LiDAR 2D em uma mesma cena documentada. Testar
primeiro visualização e cobertura; qualquer proposta de mapeamento/SLAM requer
validação separada da capacidade e qualidade dos dados.

## Fontes técnicas

- [Hi-Link: HLK-LD2450](https://www.hlktech.com/en/Goods-226.html)
- [Hi-Link: descrição de rastreamento do LD2450](https://hlktech.net/index.php?cateid=768&id=1157)
- [Texas Instruments: IWR6843ISK](https://www.ti.com/tool/IWR6843ISK)

