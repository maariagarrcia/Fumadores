# Fumadores
1) EXPLICACIÓN
El problema de los fumadores es un problema clásico en la teoría de la concurrencia y la sincronización, que ilustra los desafíos y soluciones relacionados con la coordinación entre múltiples procesos en un sistema.

Cada fumador debe esperar a tener los ingredientes necesarios para poder armar un cigarrillo. El agente tiene que facilitar la coordinación entre los fumadores asegurándose de que cada uno reciba los ingredientes adecuados en el momento oportuno.

2) PREVENCIÓN DE DEADLOCK
- Intentar adquirir el semaforo de cada uno de lo ingredientes.
- Si uno de los semaforos NO consigue bloquear se hay que
- liberar todos los adquiridios para prevenir el deadlock.
