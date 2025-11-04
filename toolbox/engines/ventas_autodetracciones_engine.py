"""
⚙️ Ventas Autodetracciones Engine V2
MIGRADO DE PANDAS A POLARS PARA MEJOR PERFORMANCE
"""

import polars as pl
import asyncio
from io import BytesIO
from xlsxwriter import Workbook

try:
    from ..core.base_engine import BaseEngine
except ImportError:
    raise ImportError("No se pudieron importar las dependencias de Referidos Engine V2")


class VentasAutodetraccionesEngine(BaseEngine):
    """
    Motor que contiene TODA la lógica de VentasAutodetraccionesCalcular V1
    """

    def __init__(self):
        super().__init__()

    async def generar_excel_autodetraccion(
        self, tipo_cambio_df: pl.DataFrame, comprobantes_file: BytesIO, hasta: str
    ) -> BytesIO:
        """
        Genera el Excel con la información filtrada por el mes indicado en 'hasta'.
        Se espera un valor en formato 'YYYY-MM'.

        Args:
            tipo_cambio_df: DataFrame con tipos de cambio
            comprobantes_file: BytesIO con el archivo Excel de comprobantes
            hasta: Fecha en formato 'YYYY-MM'
        """
        # Leer Excel (.xls) desde BytesIO usando Polars - SINTAXIS MODERNA CORREGIDA
        comprobantes_df = await asyncio.to_thread(
            pl.read_excel,
            comprobantes_file,
            sheet_id=1,  # Primera hoja (1-indexed)
            engine="calamine",  # Mejor para archivos .xls
            read_options={"header_row": 2},  # drop_empty_rows=True,
            drop_empty_cols=True,
            infer_schema_length=1000,  # Limitar inferencia para mejor rendimiento
        )

        # Copia del DataFrame de comprobantes para no alterar el original (clone en Polars moderna)
        df = comprobantes_df.clone()
        # Convertir la columna "Fecha Emisión " a datetime usando Polars moderna
        df = df.with_columns(
            [
                pl.col("Fecha Emisión ").str.strptime(
                    pl.Date, format="%d/%m/%Y", strict=False
                )
            ]
        )
        # Filtrar únicamente por el año y mes indicados (hasta) - sintaxis moderna
        df = df.filter(pl.col("Fecha Emisión ").dt.strftime("%Y-%m") == hasta)

        # Procesamiento usando Polars para mejor performance:
        estado_invalido = []

        # Seleccionar columnas y filtrar estados válidos (sintaxis moderna)
        sistema = (
            df.filter(~pl.col("Estado Doc.Tributario").is_in(estado_invalido))
            .select(
                [
                    "Estado Doc.Tributario",
                    "Fecha Emisión ",
                    "Tipo Documento",
                    "Serie-Número ",
                    "Ruc Cliente",
                    "Cliente",
                    "Op.Gravada",
                    "Op. No Gravada",
                    "IGV",
                    "Importe Total",
                    "Moneda",
                ]
            )
            .fill_null(0)
        )

        # Agregar columna FUENTE y procesar campos numéricos - COPIADO EXACTO DE V1
        sistema = sistema.with_columns([pl.lit("Sistema").alias("FUENTE")])

        # Limpiar y convertir campos numéricos EXACTAMENTE como V1
        sistema = sistema.with_columns(
            [
                pl.col("Op.Gravada")
                .cast(pl.String)
                .str.replace_all(",", "")
                .cast(pl.Float64)
                .fill_null(0),
                pl.col("Op. No Gravada")
                .cast(pl.String)
                .str.replace_all(",", "")
                .cast(pl.Float64)
                .fill_null(0),
                # También asegurar que Importe Total sea numérico
                pl.col("Importe Total")
                .cast(pl.String)
                .str.replace_all(",", "")
                .cast(pl.Float64)
                .fill_null(0),
            ]
        )

        # Calcular VALOR VENTA (sintaxis moderna)
        sistema = sistema.with_columns(
            [(pl.col("Op.Gravada") + pl.col("Op. No Gravada")).alias("VALOR VENTA")]
        )

        # Aplicar multiplicador -1 para notas de crédito - COPIADO EXACTO DE V1
        sistema = sistema.with_columns(
            [
                pl.when(pl.col("Tipo Documento") == "Nota de crédito")
                .then(pl.col("VALOR VENTA") * -1)
                .otherwise(pl.col("VALOR VENTA"))
                .alias("VALOR VENTA"),
                pl.when(pl.col("Tipo Documento") == "Nota de crédito")
                .then(pl.col("Importe Total") * -1)
                .otherwise(pl.col("Importe Total"))
                .alias("Importe Total"),
            ]
        )

        # Eliminar columnas intermedias
        sistema = sistema.drop(["Op.Gravada", "Op. No Gravada"])

        # Renombrar columnas usando Polars
        sistema = sistema.rename(
            {
                "Fecha Emisión ": "FECHA EMISION",
                "Tipo Documento": "TIPO COMPROBANTE",
                "Serie-Número ": "COMPROBANTE",
                "Ruc Cliente": "DOCUMENTO",
                "Cliente": "RAZON SOCIAL",
                "Importe Total": "IMPORTE",
                "Moneda": "MONEDA",
            }
        )

        combined_df = sistema

        # Reemplazar valores de moneda y ordenar (sintaxis moderna)
        combined_df = combined_df.with_columns(
            [
                pl.col("MONEDA").map_elements(
                    lambda x: {"Sol": "PEN", "US Dolar": "USD"}.get(x, x),
                    return_dtype=pl.String,
                ),
            ]
        ).sort("FECHA EMISION")

        # Formatear fechas como string (sintaxis moderna)
        combined_df = combined_df.with_columns(
            [pl.col("FECHA EMISION").dt.strftime("%Y-%m-%d")]
        )
        print(combined_df)
        print(tipo_cambio_df)
        # Hacer join con tipo_cambio_df y asegurar tipos correctos
        combined_df = combined_df.join(
            tipo_cambio_df,
            left_on="FECHA EMISION",
            right_on="TipoCambioFecha",
            how="left",
        )

        print(combined_df)

        # Asegurar que TipoCambioVenta sea numérico después del join
        combined_df = combined_df.with_columns(
            [pl.col("TipoCambioVenta").cast(pl.Float64).fill_null(1.0)]
        )

        # Convertir a numérico y limpiar columnas - COPIADO EXACTO DE V1
        combined_df = combined_df.with_columns(
            [
                pl.col("VALOR VENTA").cast(pl.Float64).fill_null(0),
                pl.col("IMPORTE").cast(pl.Float64).fill_null(0),
                # IGV: limpiar comas y convertir a numérico EXACTAMENTE como V1
                pl.col("IGV")
                .cast(pl.String)
                .str.replace_all(",", "")
                .cast(pl.Float64)
                .fill_null(0),
            ]
        )

        # Calcular valores en soles - COPIADO EXACTO DE V1
        combined_df = combined_df.with_columns(
            [
                pl.when(pl.col("MONEDA") == "USD")
                .then(pl.col("VALOR VENTA") * pl.col("TipoCambioVenta"))
                .otherwise(pl.col("VALOR VENTA"))
                .alias("VALOR VENTA a soles"),
                pl.when(pl.col("MONEDA") == "USD")
                .then(pl.col("IMPORTE") * pl.col("TipoCambioVenta"))
                .otherwise(pl.col("IMPORTE"))
                .alias("IMPORTE a soles"),
            ]
        )

        # Calcular IGV a soles - COPIADO EXACTO DE V1 (usando np.select equivalente)
        combined_df = combined_df.with_columns(
            [
                pl.when(
                    (pl.col("MONEDA") == "PEN")
                    & (pl.col("TIPO COMPROBANTE") == "Nota de crédito")
                )
                .then(pl.col("IGV") * -1)
                .when(
                    (pl.col("MONEDA") == "USD")
                    & (pl.col("TIPO COMPROBANTE") != "Nota de crédito")
                )
                .then(pl.col("IGV") * pl.col("TipoCambioVenta"))
                .when(
                    (pl.col("MONEDA") == "USD")
                    & (pl.col("TIPO COMPROBANTE") == "Nota de crédito")
                )
                .then(pl.col("IGV") * pl.col("TipoCambioVenta") * -1)
                .otherwise(pl.col("IGV"))
                .alias("IGV a soles")
            ]
        )

        # Asegurar que IGV sea numérico - FINAL DE LÓGICA V1
        combined_df = combined_df.with_columns(
            [pl.col("IGV").cast(pl.Float64).fill_null(0)]
        )

        # Calcular detracción: filtrar IGV > 0 e IMPORTE a soles > 700 - COPIADO EXACTO DE V1
        detraction = combined_df.filter(
            (pl.col("IGV") > 0) & (pl.col("IMPORTE a soles") > 700)
        ).with_columns(
            [(pl.col("IMPORTE a soles") * 0.12).alias("AUTO-DETRACTION a soles")]
        )

        # Generar Excel en memoria de forma asíncrona
        excel_buffer = BytesIO()
        await asyncio.to_thread(
            self._escribir_excel, combined_df, detraction, excel_buffer
        )
        excel_buffer.seek(0)
        return excel_buffer

    def _escribir_excel(
        self,
        registro_ventas: pl.DataFrame,
        autodetraccion: pl.DataFrame,
        buffer: BytesIO,
    ):
        """
        MÉTODO COMPLETAMENTE POLARS: Sin pandas, usando xlsxwriter nativo
        Polars puro con múltiples hojas Excel
        """
        # xlsxwriter puede trabajar directamente con BytesIO
        with Workbook(buffer, {"in_memory": True}) as workbook:
            # Escribir primera hoja: Registro de ventas
            registro_ventas.write_excel(
                workbook=workbook,
                worksheet="Registro de ventas",
                # table_style="Table Style Medium 9",  # Estilo simple y limpio
                autofit=True,  # Ajustar ancho automáticamente
                include_header=True,
                autofilter=True,  # Agregar filtros automáticos
            )

            # Escribir segunda hoja: Autodetracción
            autodetraccion.write_excel(
                workbook=workbook,
                worksheet="Autodetracción",
                # table_style="Table Style Medium 9",
                autofit=True,
                include_header=True,
                autofilter=True,
            )
