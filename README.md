# Silent Learner Core

Núcleo portable para separar tres capas:

1. asistente que responde;
2. learner que observa;
3. curador humano que decide qué memoria queda.

Este proyecto no ejecuta publicaciones. Sirve como base general para otros agentes.

## Uso

```bash
python core/run_turn.py --input examples/sample_turn.json
```

El resultado queda en `output/learner_candidate.json`.
