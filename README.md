# lidar-sonar-lab

Laboratório de **mapeamento e monitoramento de ambientes com sonar, LiDAR e radar**,
unindo eletrônica embarcada (Arduino Mega 2560, STM32 e ESP32) com práticas de
**Observabilidade e DevOps** (MQTT, séries temporais, Grafana, alertas, CI, etc).
O radar de micro-ondas mede alvos por ondas eletromagnéticas; a varredura
ultrassônica com servo permanece identificada como sonar.

> Status: 🟢 Lab 01 em andamento

[![CI](https://github.com/itamarsb/lidar-sonar-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/itamarsb/lidar-sonar-lab/actions/workflows/ci.yml)

## Por que este projeto

Sensores de distância são a base de robótica, drones e aviônica
(altímetros, anticolisão ou mapeamento). Aqui cada sensor é tratado como uma
**fonte de telemetria**: os dados são medidos, validados em bancada
(osciloscópio e multímetro), analisados estatisticamente e, nas fases seguintes,
enviados a um pipeline de monitoramento com dashboards e alertas.

## Arquitetura alvo

```mermaid
flowchart LR
  subgraph Borda
    S1[HC-SR04 sonar] --> MCU[Mega 2560 / STM32 / ESP32]
    S2[LiDAR ponto / 2D] --> MCU
    T[LM35 temperatura] --> MCU
    R1[Radar mmWave] --> MCU
  end
  MCU -- Wi-Fi / MQTT --> B[(Mosquitto)]
  B --> TG[Telegraf]
  TG --> DB[(InfluxDB)]
  DB --> G[Grafana: dashboards e alertas]
  S2 -. USB .-> R[ROS 2 + SLAM] --> M[Mapa do ambiente]
```

## Roadmap

| Lab | Tema | Hardware | Status |
|:---:|---|:---:|:---:|
| [01](labs/lab01-sonar-basico/) | Sonar + compensação de temperatura + validação no osciloscópio | Mega 2560, HC-SR04, LM35 | 🟢 em andamento |
| 02 | Sonar com *timer input capture*: `pulseIn()` × Timer4 do Mega × STM32 | Mega 2560, NUCLEO-F303RE | ⚪ planejado |
| 03 | Varredura ultrassônica com servo + telemetria MQTT → Telegraf → InfluxDB → Grafana | ESP32, HC-SR04, servo | ⚪ planejado |
| 04 | LiDAR de ponto (TF-Luna/VL53L1X) em servo — comparação sonar × LiDAR | ESP32, servo | ⚪ planejado |
| 05 | LiDAR 2D com ROS 2 e SLAM; rover controlado por rádio RC | LD19/RPLIDAR, rádio, servos | ⚪ planejado |
| 06 | Radar mmWave: posições e trajetórias de alvos móveis | ESP32 + LD2450 (a adquirir) | ⚪ planejado |
| 07 | Detecção de mudanças no ambiente como eventos de observabilidade | sensores disponíveis | ⚪ planejado |
| 08 | Radar mmWave com nuvem de pontos e comparação com LiDAR 2D | placa de avaliação a definir | ⚪ estudo de viabilidade |

O Lab 06 propõe comparar posição estimada, perda de alvo e latência, registrando
a geometria da sala e a referência usada. O LD2450 fornece alvos rastreados;
**não produz uma nuvem de pontos do ambiente para SLAM**. O Lab 08 depende de
avaliar o hardware e seu custo antes da compra.
[Veja o plano experimental da trilha de radar](docs/radar-experimentos.md).

## Método experimental

Cada lab deve distinguir dados simulados de medições reais e registrar condições
do ensaio, referência independente, número de amostras, leituras inválidas,
erro e limitações do sensor. As conclusões devem refletir os resultados
observados, mesmo quando não confirmarem a hipótese inicial.

## Estrutura

```
labs/      um diretório por lab: firmware, roteiro e resultados.
tools/     scripts Python (coleta serial e análise).
infra/     docker compose (Mosquitto, Telegraf, InfluxDB e Grafana) — a partir do Lab 03.
docs/      imagens, diagramas e decisões de projeto.
.github/   CI: compilação do firmware e lint dos scripts.
```

## Bancada

Arduino Mega 2560 · ESP32 · STM32 NUCLEO-F303RE · osciloscópio USB 6022BL ·
multímetro VC9808 · kits MyLab UNINTER · servos e rádio de aeromodelismo.

## Autor

**Itamar de Sá Britto Júnior** — Engenharia de Computação (UNINTER) · Cloud / DevOps / SRE  
[LinkedIn](https://www.linkedin.com/in/itamar-de-sa-britto-jr/) · [GitHub](https://github.com/itamarsb)

## Licença

MIT


---


## 📈 Repository Metrics


<p align="center">


<a href="https://info.flagcounter.com/Y91w"><img src="https://s01.flagcounter.com/count/Y91w/bg_FFFFFF/txt_000000/border_CCCCCC/columns_8/maxflags_120/viewers_0/labels_1/pageviews_1/flags_0/percent_0/" alt="Flag Counter" border="0"></a>

</p>
