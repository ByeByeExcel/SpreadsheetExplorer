import formulas as fml
import formulas.cell

from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import CellDependencies
from model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService


class ExcelParserService(ISpreadsheetParserService):
    def get_dependencies(self, filename: str) -> CellDependencies:
        wb = fml.ExcelModel().load(filename).finish()
        wb.calculate()
        dsp = wb.dsp

        dependencies = CellDependencies()

        for node in dsp.function_nodes.values():

            if isinstance(node['function'], formulas.cell.RangesAssembler):
                continue  # Skip if the function is a RangesAssembler, as this is not a valid case

            if isinstance(node['inputs'], list):
                continue  # Skip if inputs are a list, as this is not a valid case

            input_ranges_as_string: list[str] = list(node['inputs'].keys())
            output_ranges_as_string: list[str] = node['outputs']

            input_ranges: list[CellAddress] = []
            input_cells: list[CellAddress] = []

            for input_range_as_string in input_ranges_as_string:
                input_cells_as_string = self._get_individual_cells_from_range(input_range_as_string, dsp)

                input_range: CellAddress = CellAddress.from_excel_ref(input_range_as_string)
                input_ranges.append(input_range)

                for input_cell_as_string in input_cells_as_string:
                    input_cell: CellAddress = CellAddress.from_excel_ref(input_cell_as_string)
                    input_cells.append(input_cell)

            for output_as_string in output_ranges_as_string:
                output: CellAddress = CellAddress.from_excel_ref(output_as_string)
                if output not in dependencies.precedents:
                    dependencies.precedents[output] = set()
                dependencies.precedents[output].update(input_cells)

                for input_cell in input_cells:
                    if input_cell not in dependencies.dependents:
                        dependencies.dependents[input_cell] = set()
                    dependencies.dependents[input_cell].add(output)

                for input_range in input_ranges:
                    if input_range not in dependencies.dependents:
                        dependencies.dependents[input_range] = set()
                    dependencies.dependents[input_range].add(output)

        return dependencies

    @staticmethod
    def _get_individual_cells_from_range(input_range: str, dsp) -> list[str]:
        if dsp.function_nodes.get("=" + input_range) is not None:
            return dsp.function_nodes.get("=" + input_range)['function'].inputs.keys()
        else:
            return [input_range]
