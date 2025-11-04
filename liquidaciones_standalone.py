"""
🏗️ LIQUIDACIONES STANDALONE - Módulo 100% independiente
Reemplazo completo de lógica MORA A MAYO y COBRANZA ESPECIAL
"""

import pandas as pd
from typing import Set, Dict, List

class LiquidacionesStandalone:
    """
    Módulo COMPLETAMENTE AUTÓNOMO para corrección de liquidaciones
    No depende de ningún otro módulo de la toolbox
    """
    
    def __init__(self):
        self._liquidaciones_mora_mayo = self._cargar_liquidaciones_mora_mayo()
        self._liquidaciones_cobranza_especial = self._cargar_liquidaciones_cobranza_especial()

    def _cargar_liquidaciones_mora_mayo(self) -> Set[str]:
        """Lista completa de códigos MORA A MAYO"""
        return {
            "LIQ002-2021", "LIQ010-2022", "LIQ095-2022", "LIQ122-2022", "LIQ147-2022", 
            "LIQ149-2022", "LIQ188-2022", "LIQ213-2022", "LIQ2211000149", "LIQ221-2022",
            "LIQ2302000043", "LIQ2302000044", "LIQ2303000070", "LIQ2303000082", 
            "LIQ2303000129", "LIQ2303000144", "LIQ2304000013", "LIQ2304000031",
            "LIQ2304000107", "LIQ2304000117", "LIQ2304000123", "LIQ2306000105",
            "LIQ2307000164", "LIQ2308000014", "LIQ2308000077", "LIQ2308000126",
            "LIQ2308000137", "LIQ2308000139", "LIQ2308000189", "LIQ2310000033",
            "LIQ2310000036", "LIQ2310000072", "LIQ2310000082", "LIQ2310000093",
            "LIQ2310000164", "LIQ2310000186", "LIQ2310000192", "LIQ2310000193",
            "LIQ2311000129", "LIQ2311000130", "LIQ2311000131", "LIQ2311000133",
            "LIQ2311000134", "LIQ2311000233", "LIQ2312000022", "LIQ2312000097",
            "LIQ2312000135", "LIQ2312000144", "LIQ2312000145", "LIQ2312000146",
            "LIQ2312000154", "LIQ2312000183", "LIQ2312000197", "LIQ2401000066",
            "LIQ2401000125", "LIQ2401000126", "LIQ2401000132", "LIQ2401000133",
            "LIQ2401000161", "LIQ2401000163", "LIQ2401000164", "LIQ2402000088",
            "LIQ2402000112", "LIQ2403000197", "LIQ2404000017", "LIQ2404000030",
            "LIQ2404000125", "LIQ2404000156", "LIQ385-2022", "LIQ434-2021",
            "LIQ526-2021", "LIQ557-2021", "LIQ583-2021", "LIQ601-2021",
            "LIQ662-2021", "LIQ701-2021", "LIQ003-2022 ME", "LIQ014-2022 ME",
            "LIQ088-2021 ME", "LIQ128-2021 ME", "LIQ189-2022 ME", "LIQ199-2022 ME",
            "LIQ214-2021 ME", "LIQ2209000088", "LIQ2211000078", "LIQ2303000131",
            "LIQ2303000157", "LIQ2304000075", "LIQ2304000081", "LIQ2304000158",
            "LIQ2304000173", "LIQ2306000039", "LIQ2310000047", "LIQ2310000180",
            "LIQ2311000132", "LIQ2311000237", "LIQ2312000147", "LIQ2312000148",
            "LIQ2312000150", "LIQ2312000213", "LIQ2401000056", "LIQ2401000127",
            "LIQ2401000162", "LIQ2401000210", "LIQ2402000184", "LIQ2403000037",
            "LIQ2403000107", "LIQ2403000128", "LIQ2403000153", "LIQ2403000176"
        }

    def _cargar_liquidaciones_cobranza_especial(self) -> Set[str]:
        """Lista completa de códigos COBRANZA ESPECIAL"""
        return {
            "LIQ2302000034", "LIQ2309000157", "LIQ2307000196", "LIQ314-2021",
            "LIQ043-2021 ME", "LIQ023-2020 ME", "LIQ2401000124", "LIQ2305000186",
            "LIQ297-2021", "LIQ034-2021 ME", "LIQ248-2021 ME", "LIQ127-2022",
            "LIQ432-2021", "LIQ138-2021 ME", "LIQ451-2022", "LIQ2401000099",
            "LIQ2312000022", "LIQ2301000063", "LIQ2310000055", "LIQ2307000122",
            "LIQ2302000142", "LIQ2403000021", "LIQ2405000159", "LIQ2405000095",
            "LIQ2302000033", "LIQ2307000195", "LIQ2307000211", "LIQ313-2021-2",
            "LIQ2401000064", "LIQ2305000140", "LIQ296-2021", "LIQ251-2021 ME",
            "LIQ108-2022", "LIQ336-2021", "LIQ093-2021 ME", "LIQ2312000071",
            "LIQ2312000097", "LIQ2212000020", "LIQ2309000172", "LIQ2403000038",
            "LIQ2405000158", "LIQ2211000152", "LIQ2308000058", "LIQ2401000058",
            "LIQ057-2021", "LIQ254-2021 ME", "LIQ029-2022", "LIQ335-2021",
            "LIQ2312000180", "LIQ2210000084", "LIQ2403000063", "LIQ2405000211",
            "LIQ2211000037", "LIQ2308000069", "LIQ2401000042", "LIQ017-2021",
            "LIQ255-2021 ME", "LIQ009-2022", "LIQ2312000235", "LIQ2403000064",
            "LIQ2405000164", "LIQ2211000036", "LIQ2308000235", "LIQ2401000023",
            "LIQ001-2022 ME", "LIQ709-2021", "LIQ2401000021", "LIQ2403000104",
            "LIQ2309000028", "LIQ2312000197", "LIQ011-2022 ME", "LIQ632-2021",
            "LIQ2401000067", "LIQ2403000105", "LIQ2309000059", "LIQ2312000116",
            "LIQ027-2022 ME", "LIQ606-2021", "LIQ2401000107", "LIQ2403000186",
            "LIQ2309000113", "LIQ028-2022 ME", "LIQ600-2021", "LIQ2401000156",
            "LIQ2403000195", "LIQ046-2022 ME", "LIQ576-2021", "LIQ2402000010",
            "LIQ2404000029", "LIQ054-2022 ME", "LIQ2402000046", "LIQ2404000041",
            "LIQ057-2022 ME", "LIQ2402000106", "LIQ2405000223", "LIQ060-2022 ME",
            "LIQ2402000152", "LIQ061-2022 ME", "LIQ062-2022 ME", "LIQ2302000033",
            "LIQ2410000151", "LIQ2410000152", "LIQ2410000153", "LIQ2410000154",
            "LIQ2410000281", "LIQ2410000282", "LIQ2410000319", "LIQ2410000363",
            "LIQ2411000231", "LIQ2411000235", "LIQ2411000268", "LIQ2411000119",
            "LIQ2408000250", "LIQ2411000120", "LIQ2411000236", "LIQ2409000109",
            "LIQ2408000044", "LIQ2410000321", "LIQ2410000337", "LIQ2405000095",
            "LIQ2405000158", "LIQ2405000159", "LIQ2405000164", "LIQ2405000211",
            "LIQ2406000121", "LIQ2406000133", "LIQ2406000138", "LIQ2406000144",
            "LIQ2406000153", "LIQ2406000200", "LIQ2407000008", "LIQ2407000051",
            "LIQ2407000052", "LIQ2411000119", "LIQ2408000250", "LIQ2411000120",
            "LIQ2411000236", "LIQ2409000109", "LIQ2408000044", "LIQ2410000321",
            "LIQ2410000337", "LIQ2405000158", "LIQ2405000159", "LIQ2406000138",
            "LIQ2407000051", "LIQ2407000057", "LIQ2405000215"
        }

    def corregir_liquidaciones(self, datos: List[Dict], fecha_corte: str) -> pd.DataFrame:
        """
        Función PRINCIPAL - Aplica todas las correcciones
        Args:
            datos: Lista de diccionarios con datos de liquidaciones
            fecha_corte: Fecha para cálculo de vencimientos (YYYY-MM-DD)
        Returns:
            DataFrame con datos corregidos listos para Power BI
        """
        df = pd.DataFrame(datos)
        
        # Aplicar lógica completa
        df = self._aplicar_logica_completa(df, fecha_corte)
        
        # Eliminar duplicados
        df = self._eliminar_duplicados(df)
        
        return df

    def _aplicar_logica_completa(self, df: pd.DataFrame, fecha_corte: str) -> pd.DataFrame:
        """Aplica toda la lógica de corrección"""
        result_df = df.copy()
        
        # 1. Marcar liquidaciones especiales
        result_df["Es_Mora_Mayo"] = result_df["CodigoLiquidacion"].isin(self._liquidaciones_mora_mayo)
        result_df["Es_Cobranza_Especial"] = result_df["CodigoLiquidacion"].isin(self._liquidaciones_cobranza_especial)
        
        # 2. Aplicar corrección TipoPago para MORA A MAYO
        result_df["TipoPago_Real"] = result_df.apply(
            lambda row: "MORA A MAYO" if row["Es_Mora_Mayo"] else row.get("TipoPago", ""), 
            axis=1
        )
        
        # 3. Aplicar corrección Estado para COBRANZA ESPECIAL
        if "FechaConfirmado" in result_df.columns:
            fecha_corte_dt = pd.to_datetime(fecha_corte)
            result_df["Estado_Cuenta"] = result_df["FechaConfirmado"].apply(
                lambda x: "VENCIDO" if pd.to_datetime(x) <= fecha_corte_dt else "VIGENTE"
            )
            
            result_df["Estado_Real"] = result_df.apply(
                lambda row: "COBRANZA ESPECIAL" if (
                    row["Estado_Cuenta"] == "VENCIDO" and row["Es_Cobranza_Especial"]
                ) else row["Estado_Cuenta"],
                axis=1
            )
        
        # 4. Detectar y marcar duplicados
        conteo_liquidaciones = result_df["CodigoLiquidacion"].value_counts()
        result_df["Conteo_Ocurrencias"] = result_df["CodigoLiquidacion"].map(conteo_liquidaciones)
        result_df["Es_Duplicado"] = result_df["Conteo_Ocurrencias"] > 1
        
        # 5. Calcular Saldo_Total
        if all(col in result_df.columns for col in ["TipoPago", "NetoConfirmado", "MontoPago"]):
            result_df["Saldo_Total"] = result_df.apply(self._calcular_saldo_total, axis=1)
        
        return result_df

    def _calcular_saldo_total(self, row) -> float:
        """Calcula el saldo total según lógica de Power BI"""
        if row["TipoPago"] == "PAGO PARCIAL":
            return row.get("SaldoDeuda", 0)
        elif row["TipoPago"] == "":
            return row["NetoConfirmado"]
        else:
            return row["NetoConfirmado"] - row.get("MontoPago", 0)

    def _eliminar_duplicados(self, df: pd.DataFrame) -> pd.DataFrame:
        """Elimina duplicados manteniendo registros no problemáticos"""
        # Ordenar: registros problemáticos primero (para eliminarlos)
        df_ordenado = df.sort_values(
            by=["Es_Duplicado", "Es_Mora_Mayo", "Es_Cobranza_Especial"], 
            ascending=[False, False, False]  # True = no problemático primero
        )
        
        # Mantener el primer registro de cada liquidación (el no problemático)
        return df_ordenado.drop_duplicates(subset=["CodigoLiquidacion"], keep='last')

    def generar_reporte(self, datos: List[Dict], fecha_corte: str) -> Dict:
        """Genera reporte de correcciones aplicadas"""
        df = pd.DataFrame(datos)
        df_procesado = self._aplicar_logica_completa(df, fecha_corte)
        
        return {
            'total_original': len(datos),
            'total_procesado': len(df_procesado),
            'duplicados_eliminados': len(datos) - len(df_procesado),
            'mora_mayo_detectadas': df_procesado['Es_Mora_Mayo'].sum(),
            'cobranza_especial_detectadas': df_procesado['Es_Cobranza_Especial'].sum(),
            'duplicados_detectados': df_procesado['Es_Duplicado'].sum()
        }


# FUNCIONES DE CONVENIENCIA PARA USO DIRECTO
def corregir_liquidaciones(datos: List[Dict], fecha_corte: str) -> pd.DataFrame:
    """
    Función principal de conveniencia
    Uso: 
        from liquidaciones_standalone import corregir_liquidaciones
        datos_limpios = corregir_liquidaciones(datos_webservice, "2024-01-31")
    """
    processor = LiquidacionesStandalone()
    return processor.corregir_liquidaciones(datos, fecha_corte)

def obtener_reporte_correccion(datos: List[Dict], fecha_corte: str) -> Dict:
    """Genera reporte de lo que se corrigió"""
    processor = LiquidacionesStandalone()
    return processor.generar_reporte(datos, fecha_corte)