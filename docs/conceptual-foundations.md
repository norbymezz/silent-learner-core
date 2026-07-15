# Fundamentos conceptuales de Silent Learner

## Origen

Silent Learner no nació como una abstracción aislada. Emergió al intentar construir un agente específico para generar, guardar y posteriormente publicar una imagen diaria en X/Twitter.

Ese caso no fue simplemente otro contexto de uso: produjo la primera formulación del problema general. El núcleo actual conserva esa genealogía, pero no queda subordinado a aquella aplicación.

## Generalidad del agente

Silent Learner no debe definirse diciendo que «no conoce ninguna aplicación concreta». Puede llegar a conocer una, muchas o todas las aplicaciones que perciba.

La separación correcta es otra:

- el núcleo no depende estructuralmente de ninguna aplicación particular;
- las particularidades de captura y actuación se implementan mediante módulos o adaptadores;
- el conocimiento aprendido sobre una aplicación puede incorporarse a su memoria sin convertir esa aplicación en parte constitutiva del núcleo.

Por lo tanto, X/Twitter, GitHub, ChatGPT, un proyecto técnico o cualquier otro entorno son dominios aprendibles, no límites de identidad.

## Horizonte perceptivo: copia potencialmente total

El punto de partida no es una lista reducida de fuentes admitidas. El horizonte perceptivo es, en principio, la totalidad de los eventos observables por la computadora y por los sensores conectados a ella.

Esto comprende, entre otros:

- teclado, mouse y otros dispositivos de entrada;
- audio, imagen y video;
- eventos de ventanas, procesos y aplicaciones;
- archivos, portapapeles, red y registros del sistema;
- secuencias temporales, superposiciones e interrupciones entre eventos.

Los adaptadores no determinan qué puede percibir el agente. Sólo convierten cada procedencia a una representación común, conservando la procedencia, el tiempo y el grado de fidelidad como metadatos.

La aspiración de diseño es una **copia perceptiva potencialmente total** del entorno accesible. En una implementación concreta esa copia será necesariamente parcial, limitada por permisos, hardware, costo y decisiones de privacidad, pero el núcleo no debe imponer una reducción conceptual previa.

## Horizonte de acción

El universo de acciones tampoco debe reducirse a las acciones ya elegidas para una tarea particular.

El agente se ejecuta dentro de un entorno que contiene un conjunto de acciones posibles. Ese conjunto debe estar representado desde el inicio como capacidades o *affordances* disponibles, aunque el agente todavía no sepa cuál ejecutar, cuándo ni con qué finalidad.

En ese sentido:

> El agente puede no saber qué hacer, pero ya existe dentro de un mundo en el que actuar es posible.

La voluntad operativa mínima no es una orden concreta, sino la disponibilidad para seleccionar, aprender y componer acciones sobre el entorno.

La seguridad no consiste en negar ese universo, sino en controlar su acceso mediante permisos, niveles de autonomía, validación humana, trazabilidad y reversibilidad.

## Percepción, aprendizaje y acción

El núcleo distingue al menos cuatro planos:

1. **Evento percibido:** registro temporal de algo ocurrido.
2. **Interpretación:** hipótesis acerca de su significado.
3. **Memoria candidata o aceptada:** conocimiento extraído de la experiencia.
4. **Acción posible o ejecutada:** transformación del entorno con autorización explícita o política definida.

Esta separación permite que el sistema observe sin actuar, aprenda sin consolidar automáticamente y conozca una capacidad sin tener permiso para usarla.

## Identidad y agentes con el mismo prompt

El prompt no determina por sí solo la identidad efectiva de un agente.

Dos agentes inicializados con el mismo prompt pueden divergir por:

- la historia de eventos que percibieron;
- la memoria aceptada o rechazada;
- el orden y simultaneidad de sus percepciones;
- los módulos disponibles;
- los permisos y acciones accesibles;
- su estado interno acumulado.

El prompt fija condiciones iniciales y reglas, pero la perspectiva concreta emerge de la trayectoria perceptiva y operativa.

## Consecuencia arquitectónica

Silent Learner es un núcleo general con horizonte perceptivo y operativo abierto. Los módulos y adaptadores conectan ese núcleo con fuentes y acciones concretas; no definen el límite de lo que el agente puede llegar a aprender.

Los proyectos particulares —incluido el alargue modular desplazable— son contextos de trabajo separados. Pueden modificar la experiencia y la memoria del agente, pero no deben confundirse con su identidad ni con su arquitectura basal.
