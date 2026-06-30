from __future__ import annotations

import argparse
import json
from pathlib import Path

from learner import observe_turn


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    candidate = observe_turn(data.get('user', ''), data.get('assistant', ''))

    out_dir = Path('output')
    out_dir.mkdir(exist_ok=True)
    (out_dir / 'learner_candidate.json').write_text(
        json.dumps(candidate.to_dict(), indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print('Wrote output/learner_candidate.json')


if __name__ == '__main__':
    main()
