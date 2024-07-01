from dataclasses import dataclass

from model.rivenditore import Rivenditore


@dataclass
class Arco:
    r1: Rivenditore
    r2: Rivenditore
    peso: int