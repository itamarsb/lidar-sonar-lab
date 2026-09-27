# Lab 01 — Sonar HC-SR04 com compensação de temperatura

**Objetivo:** medir distância com o HC-SR04, validar o sinal no osciloscópio e
mostrar, com dados, quanto a temperatura afeta a medição.

**Tempo estimado:** 2 a 3 horas · **Placa:** Arduino Mega 2560

## 1. Material

| Item | Origem |
|:---:|:---:|
| Arduino Mega 2560 + cabo USB | seu acervo |
| Sensor ultrassônico HC-SR04 | seus sensores |
| Sensor de temperatura LM35 | kit MyLab Thomas Edison |
| Protoboard 840 furos e jumpers | kit MyLab |
| Osciloscópio USB 6022BL | kit MyLab |
| Multímetro VC9808 | kit MyLab |
| Trena ou régua e um anteparo plano (caixa de papelão, livro) | casa |

## 2. Teoria em 1 minuto

O HC-SR04 emite um pulso de 40 kHz quando recebe um pulso de 10 µs no **TRIG**.
O pino **ECHO** fica em nível alto pelo tempo de ida e volta do som:

```
distância = (tempo_echo × velocidade_do_som) / 2
```

A maioria dos tutoriais usa 343 m/s fixos, mas a velocidade do som no ar depende
da temperatura:

```
c ≈ 331,3 + 0,606 × T   (m/s, T em °C)
```

| Temperatura | c (m/s) | Erro a 2 m usando 343 m/s fixo |
|---|---|---|
| 5 °C (inverno em Rio Grande) | 334,3 | ≈ +5,2 cm |
| 20 °C | 343,4 | ≈ 0 |
| 35 °C (verão) | 352,5 | ≈ −5,4 cm |

Esse é o ponto do lab: **provar com medições** que a compensação melhora o resultado.

## 3. Montagem

```
              Arduino Mega 2560
            ┌───────────────────┐
 HC-SR04    │                   │      LM35 (face plana para você)
 VCC  ──────┤ 5V            5V  ├────── pino 1 (+Vs)
 TRIG ──────┤ D22           A0  ├────── pino 2 (Vout)
 ECHO ──────┤ D49           GND ├────── pino 3 (GND)
 GND  ──────┤ GND               │
            └───────────────────┘
```

D22 e D49 ficam no conector duplo da lateral direita do Mega (o número está
impresso ao lado de cada pino).

**Por que D49 no ECHO?** É o pino **ICP4**, a entrada de *input capture* do
Timer4 do ATmega2560. Neste lab usamos `pulseIn()`, mas no Lab 02 o mesmo pino
permite medir o eco por hardware, com resolução de 0,5 µs e sem depender do
laço do programa, sem precisar refazer a fiação.

Dicas:
- Confira a pinagem do LM35 no datasheet antes de ligar: invertido, ele esquenta muito rápido.
- Use o multímetro no pino Vout do LM35: deve dar ~10 mV por °C (ex.: 250 mV a 25 °C).
- Mantenha o LM35 perto do caminho do som, não encostado no regulador do Arduino.

## 4. Gravar o firmware

1. Abra `firmware/lab01_sonar/lab01_sonar.ino` na Arduino IDE.
2. Em **Ferramentas → Placa**, escolha **Arduino Mega or Mega 2560** (processador ATmega2560) e a porta.
   Se a placa for um clone com chip CH340 e não aparecer nenhuma porta, instale o driver CH340.
3. Faça o upload e abra o Monitor Serial a **115200 baud**.

Você verá linhas assim:

```
ms,echo_us,temp_c,c_ms,dist_fixa_cm,dist_comp_cm
1500,2915,24.63,346.23,49.99,50.46
```

## 5. Roteiro no osciloscópio (6022BL)

| Canal | Ponta em | Configuração sugerida |
|---|---|---|
| CH1 | TRIG (D22) | 2 V/div, trigger em borda de subida no CH1 |
| CH2 | ECHO (D49) | 2 V/div |

Base de tempo: comece em **500 µs/div** e ajuste.

Medições para registrar (tire print de cada uma e salve em `resultados/`):
1. **Largura do pulso TRIG**: deve estar perto de 10 µs (use 5 µs/div para ver).
2. **Atraso entre TRIG e subida do ECHO**: é o tempo em que o sensor emite a rajada de 40 kHz.
3. **Largura do pulso ECHO** com o anteparo a 50 cm: compare com o `echo_us` impresso na serial.
   A diferença entre os dois é o erro do `pulseIn()`.
4. **Sem anteparo** (apontado para o teto longe ou espaço aberto): observe o ECHO no timeout.

## 6. Coleta de dados

Instale as ferramentas uma vez:

```bash
pip install -r tools/requirements.txt
```

Posicione o anteparo em cada distância, meça com a trena e rode (troque a porta):

```bash
python tools/serial_logger.py --porta COM3 --ref 20  --segundos 30
python tools/serial_logger.py --porta COM3 --ref 50  --segundos 30
python tools/serial_logger.py --porta COM3 --ref 100 --segundos 30
python tools/serial_logger.py --porta COM3 --ref 150 --segundos 30
python tools/serial_logger.py --porta COM3 --ref 200 --segundos 30
```

No Windows a porta aparece como `COMx` no Gerenciador de Dispositivos. No Linux costuma ser `/dev/ttyUSB0`
(clones com CH340) ou `/dev/ttyACM0` (Mega original).

Depois gere a análise:

```bash
python tools/analisar.py
```

Isso cria `resultados/resumo.md` (tabela) e `resultados/erro_por_distancia.png` (gráfico).

**Desafio extra:** repita uma distância em um horário frio (manhã) e em um quente
(tarde), ou perto de um aquecedor, e compare as colunas fixa e compensada.

## 7. Experimentos de limitação do sonar

Anote o que acontece (vão ser a base da comparação com o LiDAR no Lab 04):

- [ ] Anteparo inclinado a 30° e 45°
- [ ] Superfície macia (almofada, toalha)
- [ ] Objeto estreito (cabo de vassoura) a 1 m
- [ ] Vidro ou espelho
- [ ] Menor distância confiável (abaixo de ~2 cm)
- [ ] Maior distância confiável no seu ambiente

## 8. Entregáveis para o repositório

- [ ] Foto da montagem (`docs/img/lab01-montagem.jpg`)
- [ ] Prints do osciloscópio (TRIG, ECHO)
- [ ] `resultados/medicoes.csv`, `resumo.md` e `erro_por_distancia.png`
- [ ] Seção "Conclusões" abaixo preenchida com seus números

## 9. Conclusões

> Preencha após as medições: erro médio com e sem compensação, desvio padrão,
> alcance útil observado e o que o osciloscópio mostrou sobre o `pulseIn()`.

## Próximo lab

**Lab 02:** *input capture* por hardware, primeiro no Timer4 do próprio Mega
(pino D49) e depois na NUCLEO-F303RE, comparando a precisão com o `pulseIn()`.
