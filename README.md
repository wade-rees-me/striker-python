# Striker Python Simulator

The **Striker Python Simulator** is a high-performance, command-line Blackjack simulation tool implemented in Python.

## Features

- Simulates hundreds of millions of hands
- Supports multiple betting strategies
- Supports multiple deck configurations
- CLI argument-based configuration
- Outputs logs of simulation runs

## Strategies

- `--mimic` — mimic real players
- `--linear` — linear bet ramp
- `--polynomial` — polynomial bet ramp
- `--neural` — neural net approximation
- `--basic` — basic strategy only (no counting)
- `--high-low` — classic Hi-Lo count-based strategy
- `--wong` — conservative Hi-Lo with Wong out rules

## Deck Options

- `--single-deck` — one deck (1D)
- `--double-deck` — two decks (2D)
- `--six-shoe` — six-deck shoe (6D)

## Basic Usage

```bash
python striker_python.py --mimic --single-deck --number-of-hands 100000000
```

The above runs a mimic strategy against a single deck using 100 million hands.

## CLI Arguments

| Flag                | Description                          |
|---------------------|--------------------------------------|
| `--mimic`           | Use mimic strategy                   |
| `--linear`          | Use linear strategy                  |
| `--polynomial`      | Use polynomial strategy              |
| `--neural`          | Use neural net strategy              |
| `--basic`           | Use basic strategy                   |
| `--high-low`        | Use high-low strategy                |
| `--wong`            | Use wong strategy                    |
| `--single-deck`     | Use single-deck game                 |
| `--double-deck`     | Use double-deck game                 |
| `--six-shoe`        | Use six-deck shoe                    |
| `--number-of-hands` | Number of hands to simulate (int)    |

## Simulation Output

- Logs are stored by date in `~/Striker/Simulations/YYYY/MM/DD/`
- Each run creates a timestamped log file with configuration details and simulation output.

## Running All Combinations

To simulate all strategy/deck combinations:

```bash
make run-all
```

You can also run individual combinations with:

```bash
make run-high-low-six-shoe
```

Or all decks for one strategy:

```bash
make run-neural
```

## Requirements

- Python 3.8+
- `argparse` (standard library)

## Example

```bash
python striker_python.py --high-low --six-shoe --number-of-hands 250000000
```

This will simulate 250 million hands using the Hi-Lo strategy on a 6-deck shoe

---

© 2025 Striker Simulators – Python Edition

