from project_utils.datasource import get_latest_rates_dict


class Converter:
    @staticmethod
    def run_conversion(source: str, target: str, value: float) -> float:
        currencies = get_latest_rates_dict()
        source_to_dolar_ratio = currencies[source]['value']
        dolar_to_target_ratio = currencies[target]['value'] ** -1
        return value * source_to_dolar_ratio * dolar_to_target_ratio
