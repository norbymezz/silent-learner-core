# Silent Learner Core

Núcleo portable para separar cuatro planos:

1. asistente que responde;
2. learner que observa;
3. memoria candidata o aceptada;
4. acción posible o ejecutada bajo permisos.

Silent Learner surgió al intentar construir un agente específico para generar, guardar y posteriormente publicar una imagen diaria en X/Twitter. Ese caso produjo la primera formulación del problema general, pero no limita la identidad del núcleo.

El núcleo no depende estructuralmente de ninguna aplicación concreta. Puede aprender una, muchas o todas las aplicaciones que perciba. Las particularidades de percepción y actuación viven en módulos o adaptadores.

Su horizonte de diseño parte de dos totalidades potenciales:

- la copia perceptiva de todos los eventos accesibles desde la computadora y sus sensores;
- el conjunto de acciones disponibles en el entorno, aunque todavía no se haya decidido cuál ejecutar.

El agente puede no saber qué hacer, pero ya existe dentro de un entorno en el que actuar es posible. Los permisos, la curaduría, la trazabilidad y la reversibilidad controlan el uso de esas capacidades; no eliminan su existencia conceptual.

La formulación completa está en [`docs/conceptual-foundations.md`](docs/conceptual-foundations.md).

## Uso actual del MVP

```bash
python core/run_turn.py --input examples/sample_turn.json
```

El resultado queda en `output/learner_candidate.json`.
