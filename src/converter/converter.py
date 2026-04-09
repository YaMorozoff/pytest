import argparse
from dataclasses import dataclass
from typing import Dict, Union, Tuple


class NotSameUnits(Exception):
    pass
class WrongUnits(Exception):
    pass

class Unit:
    DISTANCE = "distance"
    WEIGHT = "weight"
    SPEED = "speed"
    TEMPERATURE = "temperature"

UnitMapping = Dict[Unit, Dict[str, Union[float, Tuple[float, float]]]]

unit_values: UnitMapping = {
    Unit.DISTANCE:{
        "mm": 0.01,
        "sm": 0.1,
        "m": 1.0,
        "km": 1000.0,
    },
    Unit.WEIGHT: {
        "mg": 0.1,
        "g": 1.0,
        "kg": 1000.0,
        "t": 1_000_000.0,
    },
    Unit.SPEED: {
        "m/s": 1.0,
        "km/h": 0.2777777778,
    },
    Unit.TEMPERATURE: {
        "c": (1.0, 0.0),
        "f": (5.0/9.0, -32.0 * 5.0/9.0),
        "k": (1.0, -273.15),
    },

}

@dataclass
class ConverterReq:
    value: str
    from_unit: str
    to_unit: str

    def __post_init__(self):
        from_cats = get_current_unit(self.from_unit)
        to_cats = get_current_unit(self.to_unit)
        
        if not from_cats:
            raise WrongUnits(f"Unknown from_unit: {self.from_unit}")
        if not to_cats:
            raise WrongUnits(f"Unknown to_unit: {self.to_unit}")
        if from_cats != to_cats :
            raise NotSameUnits(f"Impossible to convert from {self.from_unit} into {self.to_unit}")


@dataclass
class ConverterRes:
    value: str
    unit: str

    def __str__(self):
       return f"\n\n\nResult value ---> {self.value} {self.unit}\n\n\n"


def get_current_unit(unit):
    cat = [cat for cat, mapping in unit_values.items() if unit in mapping]
    if len(cat) > 0:
        return cat[0]
    return cat

def convert(data:ConverterReq) -> ConverterRes:
    current_cat = get_current_unit(data.from_unit)
    current_cat_values = unit_values[current_cat]
    if current_cat is Unit.TEMPERATURE:
        mul_from, add_from = current_cat_values[data.from_unit] 
        celsius = mul_from * data.value + add_from
        mul_to, add_to = current_cat_values[data.to_unit]
        
        return (celsius - add_to) / mul_to
    factor_from = current_cat_values[data.from_unit]
    factor_to = current_cat_values[data.to_unit]
    value_in_base = float(data.value) * factor_from
    return ConverterRes(value_in_base / factor_to,data.to_unit)

def cli_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="converter",
        description="Converts different values(length, mass, volume, temperature).",
    )
    p.add_argument("value", help="Numeric value for convertation")
    p.add_argument("from_unit", help="Current value unit")
    p.add_argument("to_unit", help="Future value unit")

    return p

def start_converter(args = None):
    parser = cli_parser()
    args = parser.parse_args(args)

    req_data = ConverterReq(args.value,args.from_unit,args.to_unit)
    res = convert(req_data)

    print(res)


